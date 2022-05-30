from groundStation.groundStation import groundStation, options
from groundStation.system import SystemValues
import libcsp_py3 as libcsp
from random import randint
import os

class ftp(groundStation):
    def __init__(self, opts):
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

        super(ftp, self).__init__(opts)

    def transaction(self, buf):
        """ Execute CSP transaction - send and receive on one RDP connection and
        return parsed packet """
        conn = self.get_command_conn();
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
        rxDataList = []
        data = bytearray(libcsp.packet_get_data(packet))
        length = libcsp.packet_get_length(packet)
        rxDataList.append(self.parser.parseReturnValue(
            libcsp.conn_dst(conn),
            libcsp.conn_src(conn),
            libcsp.conn_sport(conn),
            data,
            length))
        return rxDataList

    def get_command_conn(self):
        server = self.vals.APP_DICT.get(self.satellite)
        port = self.vals.SERVICES.get('FTP_COMMAND').get('port')
        return self.__connectionManager__(server,port)

    def get_file_size_packet(self):
        subservice = self.vals.SERVICES.get('FTP_COMMAND').get('subservice').get('GET_FILE_SIZE').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(bytes(self.infile.encode("ascii")))
        out.extend(int(0).to_bytes(1, byteorder='big'))
        toSend = libcsp.buffer_get(len(out))
        libcsp.packet_set_data(toSend, out)
        return toSend

    def get_burst_download_packet(self, req_id, skip, count):     
        subservice = self.vals.SERVICES.get('FTP_COMMAND').get('subservice').get('REQUEST_BURST_DOWNLOAD').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(req_id.to_bytes(4, byteorder='big'))
        out.extend(self.blocksize.to_bytes(4, byteorder='big'))
        out.extend(int(skip).to_bytes(4, byteorder='big'))
        out.extend(int(count).to_bytes(4, byteorder='big'))
        out.extend(bytes(self.infile.encode("ascii")))
        out.extend(int(0).to_bytes(1, byteorder='big'))
        toSend = libcsp.buffer_get(len(out))
        libcsp.packet_set_data(toSend, out)
        return toSend

    def receive_burst(self, req_id, skip, count):
        conn = self.get_command_conn()
        if not os.path.exists(self.outfile):
            mode = "wb"
        else :
            mode = "ab"
        f = open(self.outfile, mode)
        f.seek(skip * self.blocksize)
        blockcount = 0;
        missing_blocks = list()
        received = 0
        while True:
            packet = libcsp.read(conn, 10000)
            if packet is None:
                print('Did not receive response')
                f.close()
                return None
            rxDataList = []
            data = bytearray(libcsp.packet_get_data(packet))
            length = libcsp.packet_get_length(packet)
            rxDataList.append(self.parser.parseReturnValue(
                libcsp.conn_dst(conn),
                libcsp.conn_src(conn),
                libcsp.conn_sport(conn),
                data,
                length))
            # I know it's not good to hardcode the byte I want like this
            # but there's too much legacy so it won't change
            if data[0] == self.vals.SERVICES.get("FTP_COMMAND").get('subservice').get('FTP_DATA_PACKET').get('subPort'):
                if rxDataList[0]['blocknum'] != blockcount:
                    missing_blocks.append(blockcount)
                    print("missed block {}".format(blockcount))
                    f.write(bytes("\0" * self.blocksize, 'ascii'))
                f.write(rxDataList[0]['data'])
                blockcount += 1
                received += rxDataList[0]['size']
                print("Received block {} of {}".format(rxDataList[0]['blocknum'] + 1, int(count)))

            else:
                # Received service reply (final packet of burst download)
                f.close()
                return rxDataList, missing_blocks, received
        f.close()

    def do_get_request(self):
        print("Requesting file {} from satellite".format(self.infile))
        size_packet = self.get_file_size_packet()
        data = self.transaction(size_packet)
        if (data is None):
            print("Did not receive response from file size packet")
            return
        if data[0]['err'] != 0:
            print("error from file size packet")
            return
        if os.path.exists(self.outfile):
            os.remove(self.outfile)
        req_id = randint(0,1652982075)
        file_size = data[0]['size']
        received = 0
        burst_size = self.burst_size;
        while (received < file_size):
            download_packet = self.get_burst_download_packet(req_id, int(received/self.blocksize), burst_size)
            conn = self.get_command_conn();
            if conn is None:
                print('Error: Could not get connection')
                return
            print("Sending new burst request")
            libcsp.send(conn, download_packet)
            libcsp.buffer_free(download_packet)
            # TODO: implement missing blocks retry
            reply, missing_blocks, bytes = self.receive_burst(req_id, int(received/self.blocksize), burst_size)
            received += bytes
            print("Received {} of {} bytes".format(received, file_size))

    def get_start_upload_packet(self, req_id, filesize):
        subservice = self.vals.SERVICES.get('FTP_COMMAND').get('subservice').get('FTP_START_UPLOAD').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(req_id.to_bytes(4, byteorder='big'))
        out.extend(filesize.to_bytes(8, byteorder='big'))
        out.extend(self.blocksize.to_bytes(4, byteorder='big'))
        out.extend(bytes(self.outfile.encode("ascii")))
        out.extend(int(0).to_bytes(1, byteorder='big'))
        toSend = libcsp.buffer_get(len(out))
        libcsp.packet_set_data(toSend, out)
        return toSend

    def get_data_upload_packet(self, req_id, data, count):
        subservice = self.vals.SERVICES.get('FTP_COMMAND').get('subservice').get('FTP_UPLOAD_PACKET').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(req_id.to_bytes(4, byteorder='big'))
        out.extend(count.to_bytes(4, byteorder='big'))
        out.extend(len(data).to_bytes(4, byteorder='big'))
        out.extend(bytearray(data))
        toSend = libcsp.buffer_get(len(out))
        libcsp.packet_set_data(toSend, out)
        return toSend

    def do_post_request(self):
        f = open(self.infile, "rb")
        filesize = os.path.getsize(self.infile)
        req_id = randint(0, 1653514975);
        print("Sending file {} to satellite".format(self.infile))
        packet = self.get_start_upload_packet(req_id, filesize);
        data = self.transaction(packet)
        if (data is None):
            print("Did not receive response from upload start packet")
            f.close()
            return
        if data[0]['err'] != 0:
            print("error from upload start packet")
            f.close()
            return
        done = False
        count = 0
        while not done:
            print("Sending packet {}/{}".format(count, int(filesize/self.blocksize)))
            data = f.read(self.blocksize)
            packet = self.get_data_upload_packet(req_id, data, count)
            count += 1
            resp = self.transaction(packet)
            if (resp is None):
                print("Did not receive response from upload data packet")
                done = True
                continue
            if resp[0]['err'] != 0:
                print("error from upload data packet")
                done = True
                continue

            if len(data) < self.blocksize:
                done = True
        f.close()

        

    def start_transfer(self):
        if self.operation == "get":
            self.do_get_request()
        elif self.operation == "post":
            self.do_post_request()
        else:
            raise ValueError("Not doing get or post request? What is my purpose?")
        
class ftp_options(options):
    def __init__(self):
        super().__init__();

    def getOptions(self):
        self.parser.add_argument(
            '-g',
            '--get',
            type=str,
            default='',
            help='File to download from satellite')
        self.parser.add_argument(
            '-p',
            '--post',
            type=str,
            default='',
            help='File to upload to satellite')
        self.parser.add_argument(
            '-o',
            '--outfile',
            type=str,
            default='',
            help='Filename to save on target (satellite or ground). Defaults is get or post filename')
        self.parser.add_argument(
            '-b',
            '--burst-size',
            type=int,
            default='100',
            help='Number of packets to receive in a single burst download')
        return super().getOptions();