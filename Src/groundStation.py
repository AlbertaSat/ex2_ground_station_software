#!/usr/bin/python3

# Build required code from satelliteSim/libcsp:
# Start zmqproxy (only one instance)
# $ ./build/zmqproxy
#
# Run client against server using ZMQ:
# LD_LIBRARY_PATH=../ex2_on_board_computer/libcsp/build PYTHONPATH=../ex2_on_board_computer/libcsp/build python3 Src/groundStation.py -I zmq


import os, re
import time
import sys
import argparse
from system import SystemValues
import libcsp_py3 as libcsp


vals = SystemValues()
apps = vals.APP_DICT
services = vals.SERVICES


class Csp(object):
    def __init__(self, opts):
        self.myAddr = apps["GND"]
        libcsp.init(self.myAddr, "host", "model", "1.2.3", 10, 300)
        if opts.interface == "zmq":
            self.__zmq__(self.myAddr)
        libcsp.route_start_task()
        time.sleep(0.2)  # allow router task startup
        print("CMP ident:", libcsp.cmp_ident(apps["DEMO"]))
        print("Ping: %d mS" % libcsp.ping(apps["DEMO"]))

    def __zmq__(self, addr):
        libcsp.zmqhub_init(addr, 'localhost')
        libcsp.rtable_load("0/0 ZMQHUB")

    def getInput(self, prompt):
        sanitizeRegex = re.compile("^[\)]") # Maybe change this to do more input sanitization
        inStr = input(prompt)
        cmdVec = re.split("\.|\(", inStr)

        # command format: <service_provider>.<service>.(<args>)
        try:
            app, service, sub, arg = [x.upper() for x in cmdVec]
        except:
            print("BAD FORMAT\n<service_provider>.<service>.<subservice>(<args>)")
            return 0
        server = apps[app]
        port = services[service]['port']
        subservice = services[service]['subservice'][sub]
        args =  [int(x) for x in (p for p in arg if not sanitizeRegex.match(p))]
        # data = map(ord, args)
        print([subservice, *args])
        b = bytearray([subservice, *args]) # convert it to something CSP can read
        # b.extend(data)
        print(b)
        toSend = libcsp.buffer_get(32)
        libcsp.packet_set_data(toSend, b)
        return toSend, server, port

    def send(self, server, port, buf):
        libcsp.sendto(0, server, port, 1, libcsp.CSP_O_NONE, buf, 1000)
        libcsp.buffer_free(buf)


def getOptions():
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-I", "--interface", type=str, default="zmq", help="CSP interface to use")
    return parser.parse_args(sys.argv[1:])


if __name__ == "__main__":
    opts = getOptions()
    csp = Csp(opts)

    while True:
        # try:
        toSend, server, port = csp.getInput("to send:")
        csp.send(server, port, toSend);
        # except:
        #     print("Could not send")
