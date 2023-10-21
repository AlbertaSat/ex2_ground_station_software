'''
 * Copyright (C) 2022  University of Alberta
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
'''
'''
 * @file ftp.py
 * @author Robert Taylor
 * @date 2022-07-22
'''

from groundStation import GroundStation
from options import optionsFactory
from system import GroundNodes, services
import os
from random import randint
from receiveParser import ReceiveParser
from system import services
import signal
import pickle

class FTPData():
    # Stores a single data transaction
    def __init__(self, reqId : int, blocknum : int, data : bytearray):
        self.reqId = reqId
        self.blocknum = blocknum
        self.data = data

    def getData(self):
        return self.data

    def getReqId(self):
        return self.reqId

    def getBlockNum(self):
        return self.blocknum

    def getDataLen(self):
        return len(self.data)

    def __lt__(self, other):
        return self.blocknum < other.blocknum

    def __gt__(self, other):
        return self.blocknum > other.blocknum

    def __le__(self, other):
        return self.blocknum <= other.blocknum

    def __ge__(self, other):
        return self.blocknum >= other.blocknum

    def __eq__(self, other):
        return self.blocknum == other.blocknum

    def __ne__(self, other):
        return self.blocknum != other.blocknum

class ftpTransaction():
    def __init__(self, reqID, totalBlocks : int, inFileName, outFileName):
        self.reqID = reqID
        self.received = []
        self.totalBlocks = totalBlocks
        self.inputFileName = inFileName
        self.outputFileName = outFileName

    def receiveData(self, data : FTPData):
        if (data.getReqId() != self.reqID):
            raise ValueError("Block given does not match my ID!")
        if data not in self.received:
            self.received.append(data)
            self.received.sort()

    def isDone(self):
        return len(self.received) == self.totalBlocks # true if finished

    def end(self):
        out = bytearray()
        for block in self.received:
            out.extend(block.getData())
        with open(self.outputFileName, "wb") as f:
            f.write(out)

    def getReqID(self):
        return self.reqID

    def listMissing(self):
        blocksReceived = [x.getBlockNum() for x in self.received]
        return [i for i in range(self.totalBlocks) if i not in blocksReceived]
    
    def getTotalBlocks(self):
        return self.totalBlocks

class ftp(GroundStation):
    def __init__(self, opts):
        super(ftp, self).__init__(opts)
        self.services = services
        self.receiveParse = ReceiveParser()
        self.operation = ''
        self.infile = opts.get if opts.get != '' else opts.post
        self.outfile = ''
        self.skip = opts.skip

        self.outfile = opts.outfile or self.infile # if no outfile is given, use infile
        self.blocksize = 512 # There's really no reason to change it..

        nodeType = "UHF"
        # finds first instance of UHF node in GroundNodes and gets its address
        addr = next((i[2] for i in GroundNodes if i[1] == nodeType), 0)
        self.dest_addr = addr

        self.destPort = self.services.get("FTP_COMMAND").get("port")

    def shutdown(self):
        exit(0)

    def run(self):
        raise ValueError("Not doing get or post request? What is my purpose?")

    def setOutfile(self, file):
        self.outfile = file

    def setInfile(self, file):
        self.infile = file

    def _transaction(self, data):
        self.networkManager.send(self.satelliteAddr, self.destPort, data)
        response = self.networkManager.receive(self.satelliteAddr, self.destPort, 10000)
        return self.receiveParse.parseReturnValue(self.satelliteAddr, self.destPort, response)

class ftpGetter(ftp):
    def __init__(self, opts):
        super().__init__(opts)
        self.use_sband = opts.sband
        self.burst_size = opts.burst_size
        self.currentTransaction = None
        if opts.resume == 0:
            self.currentTransaction = self.makeNewDownloadTransaction(self.infile, self.outfile)
        else :
            self.currentTransaction = self.resumeDownloadTransaction(opts.resume)

    def resumeDownloadTransaction(self, reqID : int):
        with open(f".ftpTransactions/{reqID}.pickle", "rb") as f:
            return pickle.loads(f.read())

    def makeNewDownloadTransaction(self, infile, outfile):
        size_packet = self._get_file_size_packet()
        try:
            data = self._transaction(size_packet)
        except:
            raise ValueError("No response from file size packet")

        if data['err'] < 0:
            raise ValueError(f"error {data['err']} from file size packet")

        filesize = int(data['size'])
        req_id = randint(1,1652982075)
        total_blocks = filesize // self.blocksize
        if total_blocks % self.blocksize > 0:
            total_blocks += 1

        return ftpTransaction(req_id, total_blocks, infile, outfile)

    def run(self):
        print(f"Requesting file {self.infile} from satellite")
        self._do_get_request()

    def shutdown(self):
        if not os.path.exists(".ftpTransactions"):
            os.mkdir(".ftpTransactions")
        with open(f".ftpTransactions/{self.currentTransaction.getReqID()}.pickle", "wb") as dumpfile:
            pickle.dump(self.currentTransaction, dumpfile)
        super().shutdown()

    def _do_get_request(self):
        received = 0
        burst_size = self.burst_size
        req_id = self.currentTransaction.getReqID()
        while not self.currentTransaction.isDone():
            missingBlocks = self.currentTransaction.listMissing()
            skip = missingBlocks[0]
            numToRequest = 1
            numToSearch = min(self.burst_size, len(missingBlocks))

            for i in range(1, numToSearch):
                if (missingBlocks[i] == missingBlocks[i - 1] + 1):
                    numToRequest += 1
                else:
                    break

            download_packet = self._get_burst_download_packet(req_id, skip, numToRequest)
            self.networkManager.send(self.satelliteAddr, self.destPort, download_packet)
            self._receive_burst()
        self.currentTransaction.end()
        myfilename = f".ftpTransactions/{self.currentTransaction.getReqID()}.pickle"
        if os.path.exists(myfilename):
            os.remove(myfilename)

    def _receive_burst(self):
        received = 0
        while True:
            packet = self.networkManager.receive(self.satelliteAddr, self.destPort, 10000)
            data = self.receiveParse.parseReturnValue(self.satelliteAddr, self.destPort, packet)
            if packet[0] != self.services.get("FTP_COMMAND").get('subservice').get(
                'FTP_DATA_PACKET'
            ).get('subPort'):
                # Received service reply (final packet of burst download)
                return data
            ftpData = FTPData(data['req_id'], data['blocknum'], data['data'])
            try:
                self.currentTransaction.receiveData(ftpData)
                print(
                    f"Received block {ftpData.getBlockNum()}/{self.currentTransaction.getTotalBlocks()}"
                )
            except Exception as e:
                print(e)

    def _get_burst_download_packet(self, req_id, skip, count):     
            subservice = self.services.get('FTP_COMMAND').get('subservice').get('REQUEST_BURST_DOWNLOAD').get('subPort')
            out = bytearray()
            out.extend(subservice.to_bytes(1, byteorder='big'))
            out.extend(req_id.to_bytes(4, byteorder='big'))
            out.extend(self.blocksize.to_bytes(4, byteorder='big'))
            out.extend(int(skip).to_bytes(4, byteorder='big'))
            out.extend(int(count).to_bytes(4, byteorder='big'))
            out.extend(int(self.use_sband).to_bytes(4, byteorder='big'))
            out.extend(bytes(self.infile.encode("ascii")))
            out.extend(int(0).to_bytes(1, byteorder='big'))
            return out

    def _get_file_size_packet(self):
        subservice = self.services.get('FTP_COMMAND').get('subservice').get('GET_FILE_SIZE').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(bytes(self.infile.encode("ascii")))
        out.extend(int(0).to_bytes(1, byteorder='big'))
        return out

class ftpSender(ftp):
    def __init__(self, opts):
        super().__init__(opts)

    def run(self):
        self._do_post_request()

    def _do_post_request(self):
        with open(self.infile, "rb") as f:
            filesize = os.path.getsize(self.infile)
            req_id = randint(0, 1653514975) # 1653514975 is the max value of a 32 bit int
            count = 0
            if self.skip != 0:
                # Note: // is the floor, or integer divide operator
                skip_blks = self.skip // self.blocksize
                count = skip_blks
                self.skip = skip_blks * self.blocksize
                f.seek(self.skip)  # skip is in bytes

            print(f"Sending file {self.infile} size {filesize} offset {self.skip} to satellite")
            packet = self._get_start_upload_packet(req_id, filesize)
            data = self._transaction(packet)
            if (data is None):
                print("Did not receive response from upload start packet")
                return
            if data['err'] < 0:
                print(f"error {data['err']} from upload start packet")
            done = False
            while not done:
                print(f"Sending packet {count}/{int(filesize / self.blocksize)}")
                data = f.read(self.blocksize)
                packet = self._get_data_upload_packet(req_id, data, count)
                count += 1
                resp = self._transaction(packet)
                if (resp is None):
                    print("Did not receive response from upload data packet")
                    done = True
                    continue
                if resp['err'] != 0:
                    print("error from upload data packet")
                    done = True
                    continue

                if len(data) < self.blocksize:
                    done = True

    def _get_data_upload_packet(self, req_id, data, count):
        subservice = self.services.get('FTP_COMMAND').get('subservice').get('FTP_UPLOAD_PACKET').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(req_id.to_bytes(4, byteorder='big'))
        out.extend(count.to_bytes(4, byteorder='big'))
        out.extend(len(data).to_bytes(4, byteorder='big'))
        out.extend(bytearray(data))
        return out

    def _get_start_upload_packet(self, req_id, filesize):
        subservice = self.services.get('FTP_COMMAND').get('subservice').get('FTP_START_UPLOAD').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(req_id.to_bytes(4, byteorder='big'))
        out.extend(filesize.to_bytes(8, byteorder='big'))
        out.extend(self.blocksize.to_bytes(4, byteorder='big'))
        out.extend(self.skip.to_bytes(8, byteorder='big'))
        out.extend(bytes(self.outfile.encode("ascii")))
        out.extend(int(0).to_bytes(1, byteorder='big'))
        return out


def ftpFactory(opts):
    if opts.get and opts.post:
        raise ValueError("Cannot post and get a file at the same time")
    if opts.get or opts.post:
        return ftpGetter(opts) if opts.get else ftpSender(opts)
    else:
        raise ValueError("Must get or post a file")

if __name__ == "__main__":
    opts = optionsFactory("ftp")
    ftpRunner =  ftpFactory(opts.getOptions())
    signal.signal(signal.SIGINT, ftpRunner.shutdown)
    try:
        ftpRunner.run()
    except Exception as e:
        print(e)
        ftpRunner.shutdown()
