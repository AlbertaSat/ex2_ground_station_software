
import time
import os
from groundStation.groundStation import groundStation, options
from groundStation.system import SystemValues
import libcsp_py3 as libcsp

def crc16(data : bytearray, offset , length):
    return 0x3019
    if data is None or offset < 0 or offset > len(data)- 1 and offset+length > len(data):
        return 0
    crc = 0
    for i in range(0, length):
        crc ^= data[offset + i] << 8
        for j in range(0,8):
            if (crc & 0x8000) > 0:
                crc =(crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xFFFF

class updater(groundStation):
    def __init__(self, opts):
        super(updater, self).__init__(opts)
        self.blocksize = opts.blocksize
        if self.blocksize % 32 != 0:
            raise ValueError("Blocksize must be a multiple of 32")
        self.filename = opts.file
        self.address = opts.address
        self.file = open(self.filename, "rb");
        self.filesize = os.path.getsize(self.filename)
        if self.filesize == 0:
            raise ValueError("File size is null")
        print("crc start")
        self.file_crc = self.crc(self.file.read())
        print("Crc done")
        self.file.seek(0)

    
    def crc(self, data):
        return crc16(data, 0, len(data))

    def transaction(self, buf):
        """ Execute CSP transaction - send and receive on one RDP connection and
        return parsed packet """
        conn = self.get_conn();
        if conn is None:
            print('Error: Could not connection')
            return False
        if conn is None:
            print('Error: Could not connection')
            return {}
        libcsp.send(conn, buf)
        libcsp.buffer_free(buf)
        rxDataList = []
        packet = libcsp.read(conn, 10000)
        if packet is None:
            print('Did not receive response')
            return None
        return bytearray(libcsp.packet_get_data(packet))


    def get_conn(self):
        server = self.vals.APP_DICT.get('OBC')
        port = self.vals.SERVICES.get('UPDATER').get('port')
        return self.__connectionManager__(server,port)

    def get_init_packet(self):
        server, port, toSend = self.getInput(None, inVal="obc.updater.INITIALIZE_UPDATE({},{},{})".format(self.address, self.filesize, self.file_crc))
        return toSend

    def get_block_update_packet(self, data):
        subservice = self.vals.SERVICES.get('UPDATER').get('subservice').get('PROGRAM_BLOCK').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(self.address.to_bytes(4, byteorder='big'))
        out.extend(len(data).to_bytes(2, byteorder='big'))
        out.extend(data)
        print(out)
        toSend = libcsp.buffer_get(len(out))
        libcsp.packet_set_data(toSend, out)
        return toSend

    def send_update(self):

        init_packet = self.get_init_packet()
        data = self.transaction(init_packet)
        if (data is None):
            print("Could not initialize connection")
            return False
        if data[1] == -1:
            print("Error response from init packet")
            return False

        b = bytearray()
        while True:
            b = self.file.read(self.blocksize)
            if len(b) == 0:
                return True
            update_packet = self.get_block_update_packet(b)
            data = self.transaction(update_packet)
            print(data[1])
            if data[1] == 255:
                print("Error response from data packet")
                return False
            self.address += len(b)
        return True



class update_options(options):
    def __init__(self):
        super().__init__();

    def getOptions(self):
        self.parser.add_argument(
            '-f',
            '--file',
            type=str,
            help='Binary to upload')
        self.parser.add_argument(
            '-b',
            '--blocksize',
            type=int,
            default='512',
            help='Number of bytes to send at a time')
        self.parser.add_argument(
            '-a',
            '--address',
            type=lambda x: int(x,0),
            default='0x00200000',
            help='address to flash update on OBC')

        return super().getOptions();


    