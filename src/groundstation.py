#!/usr/bin/python3

# Build required code from satelliteSim/libcsp:
# Start zmqproxy (only one instance)
# $ ./build/zmqproxy
#
# Run client against server using ZMQ:
# LD_LIBRARY_PATH=../SatelliteSim/libcsp/build PYTHONPATH=../SatelliteSim/libcsp/build python3 Src/groundStation.py -I zmq

import os, re
import socket
import signal
import time
import sys
import argparse


vals = SystemValues()
apps = vals.APP_DICT


class Csp(object):
    def __init__(self, opts):
        self.myAddr = apps['GND']
        self.parser = CommandParser()

        libcsp.init(self.myAddr, 'host', 'model', '1.2.3', 10, 300)
        if opts.interface == 'zmq':
            self.__zmq__(self.myAddr)
        elif opts.interface == 'uart':
            self.__uart__()
        libcsp.route_start_task()
        time.sleep(0.2)  # allow router task startup

    def __zmq__(self, addr):
        libcsp.zmqhub_init(addr, 'localhost')
        libcsp.rtable_load('0/0 ZMQHUB')

    def __uart__(self):
        libcsp.kiss_init('/dev/ttyUSB0', 9600, 512, 'uart')
        libcsp.rtable_set(1, 0, 'uart', libcsp.CSP_NO_VIA_ADDRESS)

    def getInput(self, prompt=None, inVal=None):
        if inVal is not None:
            command = self.parser(inVal)
        elif prompt is not None:
            inStr = input(prompt)
            command = self.parser.parseInputValue(inStr)
        else:
            raise Exception('invalid call to getInput')

        if command == None:
            raise Exception('Error parsing command')

        print('CMP ident:', libcsp.cmp_ident(command['dst']))
        print('Ping: %d mS' % libcsp.ping(command['dst']))
        toSend = libcsp.buffer_get(len(command['args']))
        libcsp.packet_set_data(toSend, command['args'])
        return toSend, command['dst'], command['dport']

    def send(self, server, port, buf):
        print('SENDING THE PACKET\n')
        print(server)
        print(port)
        libcsp.sendto(0, server, port, 1, libcsp.CSP_O_NONE, buf, 1000)
        libcsp.buffer_free(buf)

    def receive(self):
        libcsp.listen(sock, 5)
        while True:
            # Exit the loop gracefully (ie. CTRL+C)
            if flag.exit():
                print('Exiting receiving loop')
                flag.reset()
                return

            # wait for incoming connection
            print('WAIT FOR CONNECTION ... (CTRL+C to stop)')
            conn = libcsp.accept(sock, 1000) # or libcsp.CSP_MAX_TIMEOUT
            if not conn:
                continue

            print ('connection: source=%i:%i, dest=%i:%i' % (libcsp.conn_src(conn),
                                                             libcsp.conn_sport(conn),
                                                             libcsp.conn_dst(conn),
                                                             libcsp.conn_dport(conn)))
            while True:
                # Read all packets on the connection
                packet = libcsp.read(conn, 100)
                if packet is None:
                    print('packet is None; no more packets')
                    break
                # print the packet's data
                data = bytearray(libcsp.packet_get_data(packet))
                length = libcsp.packet_get_length(packet)
                print(length)
                print(data)
                rxData = self.parser.parseReturnValue(libcsp.conn_src(conn), libcsp.conn_dst(conn), libcsp.conn_dport(conn), data, length)
                if rxData == None:
                    print('ERROR: bad response data')
                print(rxData)


class GracefulExiter():
    '''
    Allows us to exit while loops with CTRL+C.
    (When we cannot get a connection for some reason.)
    By Esben Folger Thomas https://stackoverflow.com/a/57649638
    '''
    def __init__(self):
        self.state = False
        signal.signal(signal.SIGINT, self.flip_true)
    def flip_true(self, signum, frame):
        print('exit flag set to True (repeat to exit now)')
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.state = True
    def reset(self):
        self.state = False
        signal.signal(signal.SIGINT, self.flip_true)
    def exit(self):
        return self.state


def getOptions():
    parser = argparse.ArgumentParser(description='Parses command.')
    parser.add_argument('-I', '--interface', type=str, default='zmq', help='CSP interface to use')
    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    opts = getOptions()
    csp = Csp(opts)
    flag = GracefulExiter()

    sock = libcsp.socket()
    libcsp.bind(sock, libcsp.CSP_ANY)

    while True:
        try:
            toSend, server, port = csp.getInput(prompt='to send: ')
            csp.send(server, port, toSend);
            csp.receive()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # We're running this file directly, not as a module.
    from commandParser import CommandParser
    from system import SystemValues
    import libcsp_py3 as libcsp
else:
    # We're importing this file as a module to use in the website
    from ex2_ground_station_software.src.system import SystemValues
    import libcsp.build.libcsp_py3 as libcsp
