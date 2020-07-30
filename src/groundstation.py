#!/usr/bin/python3

# Build required code from satelliteSim/libcsp:
# Start zmqproxy (only one instance)
# $ ./build/zmqproxy
#
# Run client against server using ZMQ:
# LD_LIBRARY_PATH=../SatelliteSim/libcsp/build PYTHONPATH=../SatelliteSim/libcsp/build python3 Src/groundStation.py -I zmq


import os, re
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
global flag

class Csp(object):
    def __init__(self, opts):
        self.myAddr = apps["GND"]
        libcsp.init(self.myAddr, "host", "model", "1.2.3", 10, 300)
        if opts.interface == "zmq":
            self.__zmq__(self.myAddr)
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
        inStr = inStr.replace(")", "") # Trim the trailing bracket
        cmdVec = re.split("\.|\(|\)", inStr)
        print("cmdVec:",cmdVec)

        # command format: <service_provider>.<service>.(<args>)
        try:
            app, service, sub, arg = [x.upper() for x in cmdVec]
        except:
            raise Exception("BAD FORMAT\n<service_provider>.<service>.<subservice>(<args>)")

        if app not in apps:
            raise Exception("Invalid Application")
        if service not in services:
            raise Exception("Invalid Service")
        if sub not in services[service]['subservice']:
            raise Exception("Invalid Subservice")

        server = apps[app]
        port = services[service]['port']
        subservice = services[service]['subservice'][sub]
        arg = int(arg).to_bytes(4, 'little')
        # data = map(ord, args)
        print([subservice, arg])
        b = bytearray([subservice]) # convert it to something CSP can read
        b.extend(arg)
        print(b)

        print("CMP ident:", libcsp.cmp_ident(server))
        print("Ping: %d mS" % libcsp.ping(server))
        toSend = libcsp.buffer_get(32)
        libcsp.packet_set_data(toSend, b)
        return toSend, server, port

    def send(self, server, port, buf):
        libcsp.sendto(0, server, port, 1, libcsp.CSP_O_NONE, buf, 1000)
        libcsp.buffer_free(buf)
        print("THE PACKET HAS BEEN SENT")

    def receive(self):
        sock = libcsp.socket()
        libcsp.bind(sock, libcsp.CSP_ANY)
        libcsp.listen(sock, 5)
        while True:
            if flag == 1:
                break
            # wait for incoming connection
            print("WAIT FOR CONNECTION ...")
            conn = libcsp.accept(sock, libcsp.CSP_MAX_TIMEOUT)
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
                    break

                if libcsp.conn_dport(conn) == 1:
                    # print request
                    print("CONN DPORT: ")
                    print(libcsp.conn_dport(conn))
                    data = bytearray(libcsp.packet_get_data(packet))
                    length = libcsp.packet_get_length(packet)
                    print ("got packet, len=" + str(length) + ", data=" + ''.join('{:02xf}'.format(x) for x in data))
                    flag = 1
                    break
                else:
                    # pass request on to service handler
                    libcsp.service_handler(conn, packet)
                break

def getOptions():
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-I", "--interface", type=str, default="zmq", help="CSP interface to use")
    return parser.parse_args(sys.argv[1:])


if __name__ == "__main__":
    opts = getOptions()
    csp = Csp(opts)

    while True:
        try:
            toSend, server, port = csp.getInput(prompt="to send: ")
            csp.send(server, port, toSend)
            csp.receive()
        except Exception as e:
            print(e)
