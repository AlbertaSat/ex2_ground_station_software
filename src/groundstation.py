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
if __name__ == "__main__":
    # We're running this file directly, not as a module.
    from system import SystemValues
    import libcsp_py3 as libcsp
else:
    # We're importing this file as a module to use in the website
    from ex2_ground_station_software.src.system import SystemValues
    import libcsp.build.libcsp_py3 as libcsp


vals = SystemValues()
apps = vals.APP_DICT
services = vals.SERVICES


class Csp(object):
    def __init__(self, opts):
        self.myAddr = apps["GND"]
        libcsp.init(self.myAddr, "host", "model", "1.2.3", 10, 300)
        if opts.interface == "zmq":
            self.__zmq__(self.myAddr)
        elif opts.interface == "uart":
            self.__uart__()
        libcsp.route_start_task()
        time.sleep(0.2)  # allow router task startup

    def __zmq__(self, addr):
        libcsp.zmqhub_init(addr, 'localhost')
        libcsp.rtable_load("0/0 ZMQHUB")

    def __uart__(self):
        libcsp.kiss_init("/dev/ttyUSB0", 9600, 512, "uart")
        libcsp.rtable_set(1, 0, "uart", libcsp.CSP_NO_VIA_ADDRESS)

    def getInput(self, prompt=None, inVal=None):
        sanitizeRegex = re.compile("^[\)]") # Maybe change this to do more input sanitization
        inStr = ""
        if inVal is not None:
            inStr = inVal
        elif prompt is not None:
            inStr = input(prompt)
        else:
            raise Exception("invalid call to getInput")
        cmdVec = re.split("\.|\(|\)", inStr)
        # Use a python slicing notation to edit out the empty strings from the regex
        # (In case no arguments were entered)
        cmdVec[:] = [cmd for cmd in cmdVec if cmd!='']
        print("cmdVec:", cmdVec)

        # command format: <service_provider>.<service>.(<args>)
        try:
            if len(cmdVec) < 4: # no arguments
                app, service, sub = [x.upper() for x in cmdVec]
                arg = None
            else:
                app, service, sub, arg = [x.upper() for x in cmdVec]
        except:
            raise Exception("BAD FORMAT\n<service_provider>.<service>.<subservice>(<args>)")

        if app not in apps:
            raise Exception("Invalid Application")
        if service not in services:
            raise Exception("Invalid Service")
        if sub not in services[service]['subservice']:
            raise Exception("Invalid Subservice")

        if service == "HK":
            if arg not in apps or not arg:
                raise Exception("Invalid HK Argument")
            arg = apps[arg]

        server = apps[app]
        print(server)
        port = services[service]['port']
        subservice = services[service]['subservice'][sub]

        if arg:
            arg = socket.htonl(int(arg)).to_bytes(4, 'little')
        else:
            print("No arguments entered")
        # data = map(ord, args)
        print([subservice, arg])
        b = bytearray([subservice]) # convert it to something CSP can read
        if arg:
            b.extend(arg)
        print(b)

        print("CMP ident:", libcsp.cmp_ident(server))
        print("Ping: %d mS" % libcsp.ping(server))
        toSend = libcsp.buffer_get(32)
        libcsp.packet_set_data(toSend, b)
        return toSend, server, port

    def send(self, server, port, buf):
        print("SENDING THE PACKET\n")
        libcsp.sendto(0, server, port, 1, libcsp.CSP_O_NONE, buf, 1000)
        libcsp.buffer_free(buf)

    def receive(self):
        libcsp.listen(sock, 5)
        while True:
            # Exit the loop gracefully (ie. CTRL+C)
            if flag.exit():
                print("Exiting receiving loop")
                flag.reset()
                return

            # wait for incoming connection
            print("WAIT FOR CONNECTION ... (CTRL+C to stop)")
            conn = libcsp.accept(sock, 1000) # or libcsp.CSP_MAX_TIMEOUT
            if not conn:
                continue

            print ("connection: source=%i:%i, dest=%i:%i" % (libcsp.conn_src(conn),
                                                             libcsp.conn_sport(conn),
                                                             libcsp.conn_dst(conn),
                                                             libcsp.conn_dport(conn)))
            while True:
                # Read all packets on the connection
                packet = libcsp.read(conn, 100)
                if packet is None:
                    print("packet is None; no more packets")
                    break
                # print the packet's data
                data = bytearray(libcsp.packet_get_data(packet))
                length = libcsp.packet_get_length(packet)
                print ("got packet, len=" + str(length) + ", data=" + ''.join('{:02x}'.format(x) for x in data))
                print("data:", data)
                converted_data = int.from_bytes(data, byteorder='little', signed=False)
                print(converted_data)


class GracefulExiter():
    """
    Allows us to exit while loops with CTRL+C.
    (When we cannot get a connection for some reason.)
    By Esben Folger Thomas https://stackoverflow.com/a/57649638
    """
    def __init__(self):
        self.state = False
        signal.signal(signal.SIGINT, self.flip_true)
    def flip_true(self, signum, frame):
        print("exit flag set to True (repeat to exit now)")
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.state = True
    def reset(self):
        self.state = False
        signal.signal(signal.SIGINT, self.flip_true)
    def exit(self):
        return self.state


def getOptions():
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-I", "--interface", type=str, default="zmq", help="CSP interface to use")
    return parser.parse_args(sys.argv[1:])


if __name__ == "__main__":
    opts = getOptions()
    csp = Csp(opts)
    flag = GracefulExiter()

    sock = libcsp.socket()
    libcsp.bind(sock, libcsp.CSP_ANY)

    while True:
        try:
            toSend, server, port = csp.getInput(prompt="to send: ")
            csp.send(server, port, toSend);
            csp.receive()
        except Exception as e:
            print(e)
