from groundStation import groundStation
from options import optionsFactory
import binascii
import os

from inputParser import inputParser
from receiveParser import receiveParser
from system import services

class updater(groundStation):
    #TODO: Better object orientation, maybe a common class with FTP?
    def __init__(self, opts):
        super(updater, self).__init__(opts)
        self.services = services
        self.inParse = inputParser()
        self.receiveParse = receiveParser()
        self.blocksize = opts.blocksize
        if self.blocksize % 32 != 0:
            raise ValueError("Blocksize must be a multiple of 32")
        self.filename = opts.file
        self.file = open(self.filename, "rb")
        self.filesize = os.path.getsize(self.filename)
        if self.filesize == 0:
            raise ValueError("File size is null")
        if opts.crc == None:
            self.file_crc = self._crc(self.file.read())
        else:
            self.file_crc = opts.crc
        self.file.seek(0)
        self.doresume = opts.resume
        self.address = opts.address

    def run(self):
        self._send_update()

    def _transaction(self, command : dict):
        #TODO: This should share an interface with ftp
        dest = command["dst"]
        dport = command['dport']
        data = command['args']
        self.networkManager.send(dest, dport, data)
        response = self.networkManager.receive(dest, dport, 10000)
        return self.receiveParse.parseReturnValue(dport, response, len(response))

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

    def _send_update(self):
        skip = 0;

        if self.doresume:
            resume_packet = self._get_resume_packet()
            data = self._transaction(resume_packet);
            if (len(data) == 0):
                print("Could not initialize connection")
                return False
            if data['err'] == -1:
                print("Error response from resume packet")
                return False
            d = data
            print(d);
            if self.file_crc != d['crc'] :
                print("Crc of input file differs from CRC of file the satellite is expecting")
                exit(1)
            self.address = int(d['next_addr'])
            skip = int(d['next_addr'] - d['start_addr']);
            print("Skip: {}".format(skip))
            self.file.read(skip) # move the filepointer ahead by the size already sent
        else:
            init_packet = self._get_init_packet()
            data = self._transaction(init_packet)
            if (len(data) == 0):
                print("Could not initialize connection")
                return False
            if data['err'] == -1:
                print("Error response from init packet")
                return False

        b = bytearray()
        total_blocks = self.filesize // self.blocksize;
        current_block = skip // self.blocksize
        while True:
            b = self.file.read(self.blocksize)
            if len(b) == 0:
                break
            update_packet = self._get_block_update_packet(b)
            print("Sending block {}/{}".format(current_block, total_blocks));
            current_block += 1;
            data = self._transaction(update_packet)
            if (len(data) == 0):
                print("Did not receive response from data packet")
                return False
            if data['err'] != 0:
                print("error from data packet")
                return False
            self.address += len(b)
        return True
    
if __name__ == "__main__":
    opts = optionsFactory("updater")
    updaterRunner =  updater(opts.getOptions())
    updaterRunner.run()