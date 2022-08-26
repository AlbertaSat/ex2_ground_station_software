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
 * @file updater.py
 * @author Robert Taylor
 * @date 2022-07-21
'''

from groundStation import GroundStation
from options import optionsFactory
import binascii
import os

from inputParser import InputParser
from receiveParser import ReceiveParser
from system import services
from enum import Enum

class updater_failuretype(Enum): # Same values as updater program on satellite
    UPDATE_NOFAIL = 0
    UPDATE_GENERICFAILURE = 1
    UPDATE_INVALIDADDR = 2
    UPDATE_NOINIT = 3
    UPDATE_ERASEFAILED = 4
    UPDATE_WRITEFAILED = 5
    UPDATE_OUTOFORDER = 6
    UPDATE_CRCMISMATCH = 7
    UPDATE_VERIFYFAILED = 8
    UPDATE_NOSUBSERVICE = 9

class updater(GroundStation):
    #TODO: Better object orientation, maybe a common class with FTP?
    def __init__(self, opts):
        super(updater, self).__init__(opts)
        self.services = services
        self.inParse = InputParser()
        self.receiveParse = ReceiveParser()
        self.blocksize = opts.blocksize
        if self.blocksize % 32 != 0:
            raise ValueError("Blocksize must be a multiple of 32")
        self.setFile(opts.file)
        self.doresume = opts.resume
        self.address = opts.address
        self.skip = 0
        self.current_block = 0
        self.total_blocks = 0

    def setFile(self, filename):
        print(filename)
        self.filename = filename
        self.file = open(self.filename, "rb")
        self.filesize = os.path.getsize(self.filename)
        if self.filesize == 0:
            raise ValueError("File size is null")
        self.file_crc = self._crc(self.file.read())

        self.file.seek(0)

    def run(self):
        self._init_update()
        self._send_update()

    def _transaction(self, command : dict):
        #TODO: This should share an interface with ftp
        dest = command["dst"]
        dport = command['dport']
        data = command['args']
        try:
            self.networkManager.send(dest, dport, data)
            response = self.networkManager.receive(dest, dport, 10000)
            return self.receiveParse.parseReturnValue(dest, dport, response)
        except Exception as e:
            print(e)
            exit(1)

    def _crc(self, data):
        if data is None:
            return 0
        return binascii.crc_hqx(data, 0)

    def _get_resume_packet(self):
        command = self.inParse.parseInput("{}.updater.GET_PROGRESS()".format(self.satellite))
        return command

    def _get_init_packet(self):
        command = self.inParse.parseInput("{}.updater.INITIALIZE_UPDATE({},{},{})".format(self.satellite, self.address, self.filesize, self.file_crc))
        return command

    def _get_block_update_packet(self, data):
        #TODO: Simplify this
        subservice = self.services.get('UPDATER').get('subservice').get('PROGRAM_BLOCK').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(self.address.to_bytes(4, byteorder='big'))
        out.extend(len(data).to_bytes(2, byteorder='big'))
        out.extend(self._crc(data).to_bytes(2, byteorder='big'))
        out.extend(data)

        command = self.inParse.parseInput("{}.updater.PROGRAM_BLOCK({},{})".format(self.satellite, self.address, len(data)))
        command['args'] = out
        return command

    def _init_update(self):
        if self.doresume:
            self._setResume()
        else:
            init_packet = self._get_init_packet()
            data = self._transaction(init_packet)
            if data['err'] < 0:
                err = data['err']
                if err == -updater_failuretype.UPDATE_INVALIDADDR:
                    raise Exception("Invalid application address")
                elif err == -updater_failuretype.UPDATE_ERASEFAILED:
                    raise Exception("Satellite failed to erase flash")
                else:
                    raise Exception("Unknown init error {}".format(err))
        self.total_blocks = self.filesize // self.blocksize
        self.current_block = self.skip // self.blocksize
    def _sendblock(self, data):
        update_packet = self._get_block_update_packet(data)
        data = self._transaction(update_packet)
        return data['err']

    def _resync(self):
        self._setResume()
        self.total_blocks = self.filesize // self.blocksize
        self.current_block = self.skip // self.blocksize

    def _setResume(self):
        resume_packet = self._get_resume_packet()
        data = self._transaction(resume_packet);
        if data['err'] < 0:
            err = data['err']
            if err == -updater_failuretype.UPDATE_NOINIT:
                raise Exception("Cannot resume, no update in progress")
            else:
                raise Exception("Unknown resume error {}".format(err))
        d = data
        if self.file_crc != d['crc'] :
            raise Exception("Crc of input file differs from CRC of file the satellite is expecting")
        self.address = int(d['next_addr'])
        self.skip = int(d['next_addr'] - d['start_addr']);
        print("Skip: {}".format(self.skip))
        self.file.seek(self.skip) # move the filepointer ahead by the size already sent

    def _send_update(self):
        b = bytearray()
        while True:
            b = self.file.read(self.blocksize)
            if len(b) == 0:
                break
            print("Sending block {}/{}".format(self.current_block, self.total_blocks));
            err = self._sendblock(b)
            if err < 0:
                if err == -updater_failuretype.UPDATE_NOINIT:
                    raise Exception("No update in progress")
                elif err == -updater_failuretype.UPDATE_OUTOFORDER:
                    self._resync()
                    continue
                elif err == -updater_failuretype.UPDATE_CRCMISMATCH:
                    self.file.seek(-self.blocksize, 1)
                    continue # Keep trying until CRC is successful
                elif err == -updater_failuretype.UPDATE_WRITEFAILED:
                    raise Exception("Satellite failed to write to flash")
                else:
                    raise Exception("Unknown block update error {}".format(err))
            self.current_block += 1;
            self.address += len(b)
        return True
    
if __name__ == "__main__":
    opts = optionsFactory("updater")
    updaterRunner =  updater(opts.getOptions())
    updaterRunner.run()