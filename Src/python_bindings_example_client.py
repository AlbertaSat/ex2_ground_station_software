#!/usr/bin/python3

# Build required code:
# $ ./examples/buildall.py
#
# Start zmqproxy (only one instance)
# $ ./build/zmqproxy
#
# Run client against server using ZMQ:
# $ LD_LIBRARY_PATH=build PYTHONPATH=build python3 examples/python_bindings_example_client.py -z localhost
#

import os, re
import time
import sys
import argparse
from system import SystemValues
import libcsp_py3 as libcsp

sys = SystemValues()
apps = sys.APP_DICT

class CSP(object):
    def __init__(self):
        libcsp.init(apps["GND"], "host", "model", "1.2.3", 10, 300)
        libcsp.zmqhub_init(apps["GND"], 'localhost')
        libcsp.rtable_load("0/0 ZMQHUB")
        libcsp.route_start_task()
        time.sleep(0.2)  # allow router task startup
        print("CMP ident:", libcsp.cmp_ident(apps["DEMO"]))
        print("Ping: %d mS" % libcsp.ping(apps["DEMO"]))

    def getInput(self, prompt):
        inStr = input(prompt)

        cmdVec = re.split("\.|\(", inStr)
        server = apps[cmdVec[0]]
        data = cmdVec[-1]

        b = bytearray()
        b.extend(map(ord, data))
        toSend = libcsp.buffer_get(32)
        libcsp.packet_set_data(toSend, b)
        return toSend, server, 3

    def send(self, server, port, buf):
        libcsp.sendto(0, server, port, 1, libcsp.CSP_O_NONE, buf, 1000)
        libcsp.buffer_free(buf)

if __name__ == "__main__":
    csp = CSP()
    while True:
        toSend, server, port = csp.getInput("to send:")
        csp.send(server, port, toSend);
