import socket
import numpy as np
import base64
from receiveParser import ReceiveParser

class beaconDecoder:

    def __init__(self):
        self.rxport = 4322
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", self.rxport))
        self.parser = ReceiveParser()
    
    def run(self):
        while True:
            self.rawdata = self.s.recv(10000)
            print("----------Beacon Received:----------")
            beacon_ID = 99
            beacon_port = 1
            payload_offset = 16
            packet_num_offset = 4
            decoded_data = base64.b64decode(self.rawdata)
            decoded_data = bytearray(decoded_data)
            if decoded_data[packet_num_offset] == 1:
                decoded_data[:0] = (1).to_bytes(1,'big')
                ret = self.parser.parseReturnValue(beacon_ID, beacon_port, decoded_data)
            elif decoded_data[packet_num_offset] == 2:
                decoded_data[:0] = (2).to_bytes(1,'big')
                ret = self.parser.parseReturnValue(beacon_ID, beacon_port, decoded_data)
            else:
                print('Received beacon with invalid packet number: ' + str(decoded_data[packet_num_offset]))          
            if ret:
                for key, value in ret.items():
                    print("{} : {}".format(key, value))
                print("")


if __name__ == '__main__':
    decoder = beaconDecoder()
    decoder.run()   
