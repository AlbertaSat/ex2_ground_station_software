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
        self.rawdata = self.s.recv(10000)
        beacon_ID = 99
        beacon_port = 1
        payload_offset = 16
        packet_num_offset = 4
        decoded_data = base64.b64decode(self.rawdata)
        decoded_data = bytearray(decoded_data)
        if decoded_data[packet_num_offset] == 1:
            decoded_data[:0] = (1).to_bytes(1,'big')
            self.beacon = self.parser.parseReturnValue(beacon_ID, beacon_port, decoded_data)
            self.unpack_switch_status()
        elif decoded_data[packet_num_offset] == 2:
            decoded_data[:0] = (2).to_bytes(1,'big')
            self.beacon = self.parser.parseReturnValue(beacon_ID, beacon_port, decoded_data)
        else:
            self.beacon = None

        return self.beacon

    def unpack_switch_status(self)
        switches = ['Starboard Panel Switch', '2U Payload Switch', 'Port Panel Switch' \
                    'UHF Nadir Switch', 'UHF Starboard Switch', 'UHF Zenith Switch', \
                    'UHF Port Switch', 'DFGM Switch']

        shift_bits = 0
        for switch in switches:
            status = self.beacon['switch_stat'] >> shift_bits) & 1
            shift_bits += 1
            self.beacon.update({switch: status})


if __name__ == '__main__':
    decoder = beaconDecoder()
    while True:
        beacon = decoder.run()
        print("----------Beacon Received:----------")
        if beacon:
            for key, value in beacon.items():
                print("{} : {}".format(key, value))
        else:
            print('Received beacon with invalid packet number...')
        print("")
