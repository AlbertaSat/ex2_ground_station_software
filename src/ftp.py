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

#TODO: not a fan of the level of object orientation here. FTP is responsible for too much
#TODO: The naming conventions here are... interesting

class ftpDownloader():
    def __init__(self):
        self.req_id = 0
        self.missedBlocks = []
        self.burstSize = 100
        self.fileSize = 0
        self.seek = 0 #highest block received
        self.data = bytearray() # data array received
    def turnTheCrank(self):
        # Starting with missed blocks, try to receive up to burstSize packets
        # Returns whether the file is received
        return len(self.data) == self.fileSize

class ftp(GroundStation):
    def __init__(self, opts):
        super(ftp, self).__init__(opts)
        self.services = services
        self.receiveParse = ReceiveParser()
        self.operation = ''
        self.infile = ''
        self.outfile = ''
        if opts.get and opts.post:
            raise ValueError("Cannot post and get a file at the same time")
        if not opts.get and not opts.post:
            raise ValueError("Must get or post a file")
        
        if opts.get:
            self.operation = "get"
            self.infile = opts.get
        elif opts.post:
            self.operation = "post"
            self.infile = opts.post

        if opts.outfile:
            self.outfile = opts.outfile
        else:
            self.outfile = self.infile

        self.blocksize = 512 # There's really no reason to change it..

        self.burst_size = opts.burst_size
        if (opts.sband):
            self.dest_addr = GroundNodes.SBAND.value
        else:
            self.dest_addr = GroundNodes.GND.value

        self.destPort = self.services.get("FTP_COMMAND").get("port")

    def run(self):
        if self.operation == "get":
            self._do_get_request()
        elif self.operation == "post":
            self._do_post_request()
        else:
            raise ValueError("Not doing get or post request? What is my purpose?")

    def setOperation(self, op):
        if op == "get":
            self.operation = op
        elif op == "post":
            self.operation = op
        else:
            raise ValueError("Invalid operation {}".format(op))

    def setOutfile(self, file):
        self.outfile = file

    def setInfile(self, file):
        self.infile = file

    def _transaction(self, data):
        self.networkManager.send(self.satelliteAddr, self.destPort, data)
        response = self.networkManager.receive(self.satelliteAddr, self.destPort, 10000)
        return self.receiveParse.parseReturnValue(self.destPort, response)


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

    def _get_file_size_packet(self):
        subservice = self.services.get('FTP_COMMAND').get('subservice').get('GET_FILE_SIZE').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(bytes(self.infile.encode("ascii")))
        out.extend(int(0).to_bytes(1, byteorder='big'))
        return out

    def _get_burst_download_packet(self, req_id, skip, count):     
        subservice = self.services.get('FTP_COMMAND').get('subservice').get('REQUEST_BURST_DOWNLOAD').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(req_id.to_bytes(4, byteorder='big'))
        out.extend(self.blocksize.to_bytes(4, byteorder='big'))
        out.extend(int(skip).to_bytes(4, byteorder='big'))
        out.extend(int(count).to_bytes(4, byteorder='big'))
        out.extend(int(self.dest_addr).to_bytes(4, byteorder='big'))
        out.extend(bytes(self.infile.encode("ascii")))
        out.extend(int(0).to_bytes(1, byteorder='big'))
        return out

    def _receive_burst(self, req_id, skip, count):
        if not os.path.exists(self.outfile):
            mode = "wb"
        else :
            mode = "ab"
        with open(self.outfile, mode) as f:
            f.seek(skip * self.blocksize)
            blockcount = 0;
            missing_blocks = list()
            received = 0
            while True:
                packet = self.networkManager.receive(self.satelliteAddr, self.destPort, 10000)
                data = self.receiveParse.parseReturnValue(self.destPort, packet)
                # I know it's not good to hardcode the byte I want like this
                # but there's too much legacy so it won't change
                if packet[0] == self.services.get("FTP_COMMAND").get('subservice').get('FTP_DATA_PACKET').get('subPort'):
                    if data['blocknum'] != blockcount:
                        missing_blocks.append(blockcount)
                        print("missed block {}".format(blockcount))
                        f.write(bytes("\0" * self.blocksize, 'ascii'))
                    f.write(data['data'])
                    blockcount += 1
                    received += data['size']
                    print("Received block {} of {}".format(data['blocknum'] + 1, int(count)))

                else:
                    # Received service reply (final packet of burst download)
                    return data, missing_blocks, received

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
            if data['err'] != 0:
                print("error from upload start packet")
                return
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

    def _do_get_request(self):
        print("Requesting file {} from satellite".format(self.infile))
        size_packet = self._get_file_size_packet()
        data = self._transaction(size_packet)
        if (data is None):
            print("Did not receive response from file size packet")
            return
        if data['err'] != 0:
            print("error from file size packet")
            return
        if os.path.exists(self.outfile):
            os.remove(self.outfile)
        req_id = randint(0,1652982075)
        file_size = data['size']
        received = 0
        burst_size = self.burst_size;
        while (received < file_size):
            download_packet = self._get_burst_download_packet(req_id, int(received/self.blocksize), burst_size)
            self.networkManager.send(self.satelliteAddr, self.destPort, download_packet)
            # TODO: implement missing blocks retry
            reply, missing_blocks, bytes = self._receive_burst(req_id, int(received/self.blocksize), burst_size)
            received += bytes
            print("Received {} of {} bytes".format(received, file_size))


if __name__ == "__main__":
    opts = optionsFactory("ftp")
    ftpRunner =  ftp(opts.getOptions())
    try:
        ftpRunner.run()
    except Exception as e:
        print(e)
        exit(1)