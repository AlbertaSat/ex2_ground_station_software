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
        self.received = list()
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
        missingBlocks = []
        blocksReceived = [x.getBlockNum() for x in self.received]
        for i in range(self.totalBlocks):
            if i not in blocksReceived:
                missingBlocks.append(i)
        return missingBlocks
    
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

        if opts.outfile:
            self.outfile = opts.outfile
        else:
            self.outfile = self.infile

        self.blocksize = 512 # There's really no reason to change it..

        if (opts.sband):
            self.dest_addr = GroundNodes.SBAND.value
        else:
            self.dest_addr = GroundNodes.GND.value

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
        response = self.networkManager.receive(self.satelliteAddr, self.destPort, 1000)
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
        with open(".ftpTransactions/{}.pickle".format(reqID), "rb") as f:
            return pickle.loads(f.read())

    def makeNewDownloadTransaction(self, infile, outfile):
        size_packet = self._get_file_size_packet()
        try:
            data = self._transaction(size_packet)
        except:
            raise ValueError("No response from file size packet")

        if data['err'] < 0:
            raise ValueError("error {} from file size packet".format(data['err']))
        
        filesize = int(data['size'])
        req_id = randint(1,1652982075)
        total_blocks = filesize // self.blocksize
        if total_blocks % self.blocksize > 0:
            total_blocks += 1

        return ftpTransaction(req_id, total_blocks, infile, outfile)

    def run(self):
        print("Requesting file {} from satellite".format(self.infile))
        self._do_get_request()

    def shutdown(self, arg1, arg2):
        if not os.path.exists(".ftpTransactions"):
            os.mkdir(".ftpTransactions")
        with open(".ftpTransactions/{}.pickle".format(self.currentTransaction.getReqID()), "wb") as dumpfile:
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
            numToSearch = self.burst_size if self.burst_size < len(missingBlocks) else len(missingBlocks)

            for i in range(1, numToSearch):
                if (missingBlocks[i] == missingBlocks[i - 1] + 1):
                    numToRequest += 1
                else:
                    break
                
            download_packet = self._get_burst_download_packet(req_id, skip, numToRequest)
            self.networkManager.send(self.satelliteAddr, self.destPort, download_packet)
            self._receive_burst()
        self.currentTransaction.end()
        myfilename = ".ftpTransactions/{}.pickle".format(self.currentTransaction.getReqID())
        if os.path.exists(myfilename):
            os.remove(myfilename)

    def _receive_burst(self):
        received = 0
        while True:
            packet = self.networkManager.receive(self.satelliteAddr, self.destPort, 10000)
            data = self.receiveParse.parseReturnValue(self.satelliteAddr, self.destPort, packet)
            # I know it's not good to hardcode the byte I want like this
            # but there's too much legacy so it won't change
            if packet[0] == self.services.get("FTP_COMMAND").get('subservice').get('FTP_DATA_PACKET').get('subPort'):
                ftpData = FTPData(data['req_id'], data['blocknum'], data['data'])
                try:
                    self.currentTransaction.receiveData(ftpData)
                    print("Received block {}/{}".format(ftpData.getBlockNum(), self.currentTransaction.getTotalBlocks()))
                except Exception as e:
                    print(e)
                    continue
            else:
                # Received service reply (final packet of burst download)
                return data

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
    def __init__(self,opts):
        super().__init__(opts)

    def run(self):
        self._do_post_request()

    def _do_post_request(self):
        with open(self.infile, "rb") as f:
            filesize = os.path.getsize(self.infile)
            req_id = randint(0, 1653514975);
            print("Sending file {} to satellite".format(self.infile))
            packet = self._get_start_upload_packet(req_id, filesize);
            data = self._transaction(packet)
            if (data is None):
                print("Did not receive response from upload start packet")
                return
            if data['err'] < 0:
                print("error {} from upload start packet".format(data['err']))
            done = False
            count = 0
            while not done:
                print("Sending packet {}/{}".format(count, int(filesize/self.blocksize)))
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
        out.extend(bytes(self.outfile.encode("ascii")))
        out.extend(int(0).to_bytes(1, byteorder='big'))
        return out


def ftpFactory(opts):
    if opts.get and opts.post:
        raise ValueError("Cannot post and get a file at the same time")
    if not opts.get and not opts.post:
        raise ValueError("Must get or post a file")

    if opts.get:
        return ftpGetter(opts)
    elif opts.post:
        return ftpSender(opts)

if __name__ == "__main__":
    opts = optionsFactory("ftp")
    ftpRunner =  ftpFactory(opts.getOptions())
    signal.signal(signal.SIGINT, ftpRunner.shutdown)
    try:
        ftpRunner.run()
    except Exception as e:
        print(e)
        ftpRunner.shutdown(None, None)
