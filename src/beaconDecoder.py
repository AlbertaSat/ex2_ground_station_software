import socket
import numpy as np
import base64
from receiveParser import ReceiveParser
import argparse

parser = argparse.ArgumentParser(prog='beaconDecoder.py', description='Receive beacons from the satellites.')
parser.add_argument('-d', '--debug', action='store_true', help="print debug output")
args = parser.parse_args()

class beaconDecoder:

    def __init__(self):
        self.rxport = 4322
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect(("127.0.0.1", self.rxport))
        except:
            print("Unable to connect to GNURadio. Is it running?")
            exit()
        self.parser = ReceiveParser()

  
    def run(self):
        self.rawdata = self.s.recv(10000)
        beacon_ID = 99
        beacon_port = 1
        payload_offset = 16
        packet_num_offset = 4

        # Check if socket is still open
        try:
            self.s.send(bytes("You good bro?", 'utf-8'))
        except:
            print("Socket connection to GNURadio closed")
            exit()

        if bytes("Hello, world!", 'utf-8') in self.rawdata:
            print("Default EnduroSat Beacon Received")
            return
        
        if args.debug:
            print(self.rawdata)

        try:
            decoded_data = base64.b64decode(self.rawdata[payload_offset:])
            decoded_data = bytearray(decoded_data)
            print("Base 64 beacon decode success!")
        except:
            print("Base 64 beacon decode failed :(")
            return
        
        try:
            if decoded_data[packet_num_offset] == 1:
                decoded_data[:0] = (1).to_bytes(1,'big')
                return self.parser.parseReturnValue(beacon_ID, beacon_port, decoded_data)
            elif decoded_data[packet_num_offset] == 2:
                decoded_data[:0] = (2).to_bytes(1,'big')
                return self.parser.parseReturnValue(beacon_ID, beacon_port, decoded_data)
            else:
                print("Invalid beacon packet number")
                return None
        except:
            print("Unable to parse packet data")
            return None

if __name__ == '__main__':
    decoder = beaconDecoder()
    while True:
        beacon = decoder.run() 
        if beacon:
            print("----------Beacon Received:----------")
            for key, value in beacon.items():
                print("{} : {}".format(key, value)) 
