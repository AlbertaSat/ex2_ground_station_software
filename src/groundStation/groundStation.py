'''
 * Copyright (C) 2020  University of Alberta
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
 * @file groundStation.py
 * @author Andrew Rooney, Hugh Bagan, Haoran Qi
 * @date 2020-08-26
'''

'''
Build required code from satelliteSim/libcsp:
Start zmqproxy (only one instance)
$ ./build/zmqproxy

Run client against server using:
LD_LIBRARY_PATH=../SatelliteSim/libcsp/build PYTHONPATH=../SatelliteSim/libcsp/build python3 src/groundStation.py -I <zmq|uart>
'''


import argparse
import sys
import time
import signal
import socket
import os
import re
from collections import defaultdict

# if __name__ == '__main__':
# We're running this file directly, not as a module.
from groundStation.commandParser import CommandParser
from groundStation.system import SystemValues
import libcsp_py3 as libcsp
# else:
#     # We're importing this file as a module to use in the website
#     from ex2_ground_station_software.src.system import SystemValues
#     import libcsp.build.libcsp_py3 as libcsp

vals = SystemValues()
apps = vals.APP_DICT


class groundStation(object):
    ''' Constructor '''
    def __init__(self, opts):
        self.myAddr = apps['GND']
        self.parser = CommandParser()
        self.server_connection = defaultdict(dict)
        libcsp.init(self.myAddr, 'host', 'model', '1.2.3', 100, 300)
        if opts.interface == 'zmq':
            self.__zmq__(self.myAddr)
        elif opts.interface == 'uart':
            self.__uart__(opts.device)
        libcsp.route_start_task()
        time.sleep(0.2)  # allow router task startup
        self.rdp_timeout = 5000  # 10 seconds
        libcsp.rdp_set_opt(4, self.rdp_timeout, 1000, 1, 250, 2)

    ''' Private Methods '''

    def __zmq__(self, addr):
        libcsp.zmqhub_init(addr, 'localhost')
        libcsp.rtable_load('0/0 ZMQHUB')

    def __uart__(self, device):
        libcsp.kiss_init(device, 9600, 512, 'uart')
        libcsp.rtable_set(1, 0, 'uart', libcsp.CSP_NO_VIA_ADDRESS)

    def __connectionManager__(self, server, port):
        current = time.time()
        timeout = self.rdp_timeout / 1000
        if server not in self.server_connection or port not in self.server_connection[
                server] or self.server_connection[server][port]['time of birth'] + timeout <= current:
            if server in self.server_connection and port in self.server_connection[
                    server] and self.server_connection[server][port]['time of birth'] + timeout <= current:
                libcsp.close(self.server_connection[server][port]['conn'])

            try:
                conn = libcsp.connect(
                    libcsp.CSP_PRIO_NORM, server, port, 1000, libcsp.CSP_O_RDP)
            except Exception as e:
                print(e)
                return None

            self.server_connection[server][port] = {
                'conn': conn,
                'time of birth': time.time()
            }

        return self.server_connection[server][port]['conn']

    ''' Public Methods '''

    def getInput(self, prompt=None, inVal=None):
        if inVal is not None:
            try:
                command = self.parser.parseInputValue(inVal)
            except Exception as e:
                print(e + '\n')
                return
        elif prompt is not None:
            inStr = input(prompt)
            try:
                command = self.parser.parseInputValue(inStr)
            except Exception as e:
                print(e + '\n')
                return
        else:
            print('invalid call to getInput')
            return

        if command is None:
            print('Error: Command was not parsed')
            return

        toSend = libcsp.buffer_get(len(command['args']))
        if len(command['args']) > 0:
            libcsp.packet_set_data(toSend, command['args'])
        return command['dst'], command['dport'], toSend

    def transaction(self, server, port, buf):
        conn = self.__connectionManager__(server, port)
        if conn is None:
            print('Error: Could not connection')
            return {}
        libcsp.send(conn, buf)
        libcsp.buffer_free(buf)
        packet = libcsp.read(conn, 10000)
        if packet is None:
            print('packet is None; no more packets')
            return

        data = bytearray(libcsp.packet_get_data(packet))
        length = libcsp.packet_get_length(packet)
        rxData = self.parser.parseReturnValue(
            libcsp.conn_dst(conn),
            libcsp.conn_src(conn),
            libcsp.conn_sport(conn),
            data,
            length)

        if rxData is None:
            print('ERROR: bad response data')
        return rxData

    def receive(self):
        parser = CommandParser()

        # if sock not in locals():
        sock = libcsp.socket()
        libcsp.bind(sock, libcsp.CSP_ANY)
        libcsp.listen(sock, 5)
        # Exit the loop gracefully (ie. CTRL+C)
        if flag.exit():
            print('Exiting receiving loop')
            flag.reset()
            return

        # wait for incoming connection
        while True:
            print('WAIT FOR CONNECTION ... (CTRL+C to stop)')

            conn = libcsp.accept(sock, 1000)  # or libcsp.CSP_MAX_TIMEOUT
            if not conn:
                continue

            print(
                'connection: source=%i:%i, dest=%i:%i' %
                (libcsp.conn_src(conn),
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
                rxData = parser.parseReturnValue(
                    libcsp.conn_src(conn),
                    libcsp.conn_dst(conn),
                    libcsp.conn_dport(conn),
                    data,
                    length)
                if rxData is None:
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
        p.terminate()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.state = True

    def reset(self):
        self.state = False
        signal.signal(signal.SIGINT, self.flip_true)

    def exit(self):
        return self.state


class options(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Parses command.')

    def getOptions(self):
        self.parser = argparse.ArgumentParser(description='Parses command.')
        self.parser.add_argument(
            '-I',
            '--interface',
            type=str,
            default='zmq',
            help='CSP interface to use')

        self.parser.add_argument(
            '-d',
            '--device',
            type=str,
            default='/dev/ttyUSB0',
            help='External device file')
        return self.parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    opts = options()
    csp = groundStation(opts.getOptions())

    while True:
        try:
            server, port, toSend = csp.getInput(prompt='to send: ')
            csp.transaction(server, port, toSend)
            # receive()
        except Exception as e:
            print(e)
