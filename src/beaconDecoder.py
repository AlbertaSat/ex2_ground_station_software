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

  
    def beaconRunDecoder(self):
        self.rawdata = self.s.recv(10000)
        
        if args.debug:
            print(self.rawdata)

        # Check if socket is still open
        if self.rawdata == b'':
            exit()

        # Check for default EnduroSat beacon
        if bytes("Hello, world!", 'utf-8') in self.rawdata:
            print("Default EnduroSat Beacon Received")
            return False
        
        self.beaconBase64Decode()
        return self.beaconParseData()
        
    
    def beaconBase64Decode(self):
        payload_offset = 16

        try:
            self.decoded_data = base64.b64decode(self.rawdata[payload_offset:])
            self.decoded_data = bytearray(self.decoded_data)
            print("Base 64 beacon decode success!")
        except:
            print("Base 64 beacon decode failed :(")
        return None

    def beaconParseData(self):
        packet_num_offset = 4
        beacon_ID = 99
        beacon_port = 1 

        try:
            if self.decoded_data[packet_num_offset] in {1, 2}:
                self.decoded_data[:0] = self.decoded_data[packet_num_offset].to_bytes(1,'big')
                return self.parser.parseReturnValue(beacon_ID, beacon_port, self.decoded_data)
            else:
                print("Invalid beacon packet number")
        except Exception:
            print("Unable to parse packet data")
        return None

if __name__ == '__main__':
    decoder = beaconDecoder()
    while True:
        if beacon := decoder.beaconRunDecoder():
            print("----------Beacon Received:----------")
            for key, value in beacon.items():
                print(f"{key} : {value}") 
