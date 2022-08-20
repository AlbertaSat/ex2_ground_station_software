'''
 * Copyright (C) 2022  University of Alberta
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
 * @file CSPHandler.py
 * @author Robert Taylor
 * @date 2022-07-21
'''

import libcsp_py3 as libcsp
import packetUtils
from connectionManager import ConnectionManager
import serial
from system import SatelliteNodes

def getCSPHandler(addr, interface, device, hmacKey, protocol = None, useFec = False):
    if protocol is None:
        return CSPHandler(addr, interface, device, hmacKey, useFec)
    elif protocol == "UHF":
        return UHF_CSPHandler(addr, interface, device, hmacKey, useFec)
    else:
        raise ValueError("Protocol {} does not exist for CSP handlers".format(protocol))

class CSPHandler(object):
    __instance = None
    def __new__(cls, addr, interface, device, hmacKey, useFec):
        if cls.__instance is None:
            cls.__instance = super(CSPHandler, cls).__new__(cls)
        return cls.__instance

    # 'addr' groundstation's address
    # 'interface' interface to use
    # 'device' device file interface is to write to
    # 'hmacKey' key to use for HMAC authentication
    def __init__(self, addr, interface, device, hmacKey, useFec):
        self.connectionManager = ConnectionManager()
        self.usingFec = useFec
        self.myAddr = addr;
        self.numberOfBuffers = 100
        self.bufferSize = 1024 #This is max size of an incoming packet
        libcsp.init(self.myAddr, 'GroundStation', 'model', '1.2.3', self.numberOfBuffers, self.bufferSize)
        libcsp.hmac_set_key(hmacKey, len(hmacKey))

        self.interfaceName = ""
        if interface == 'uart':
            self.ser = self._uart(device)
        elif interface == 'uhf' or interface == "sdr":
            self._uhf(device, libcsp.SDR_UHF_9600_BAUD)
        elif interface == 'sband':
            self._sband()
        elif interface == 'dummy':
            self.interfaceName = "dummy"
            return # Skip libcsp initialization when using dummy responses
        else:
            raise ValueError("Interface {} does not exist".format(interface))


        stringBuild = ""
        for node in SatelliteNodes:
            stringBuild = stringBuild + " {} {}, ".format(node.value, self.interfaceName)
        libcsp.rtable_load(stringBuild)

        libcsp.route_start_task()

    def send(self, server, port, buf : bytearray):
        packet = packetUtils.makePacket(buf)
        conn = self.connectionManager.getConn(server,port)
        libcsp.send(conn, packet)
        libcsp.buffer_free(packet)

    def receive(self, server, port, timeout):
        conn = self.connectionManager.getConn(server,port)
        packet = libcsp.read(conn, timeout)
        data = None
        if packet is None:
            raise Exception("No packet received after {} seconds".format(timeout // 1000))
        data = packetUtils.breakPacket(packet)
        libcsp.buffer_free(packet)
        return data

    def _uart(self, device):
        """ initialize uart interface """
        ser = serial.Serial(device,
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=2,
        timeout=1)

        libcsp.kiss_init(device, ser.baudrate, 512, 'uart')
        self.interfaceName = "uart"

    def _uhf(self, device, uhf_baudrate):
        """ Initialize SDR interface """
        libcsp.uhf_init(device, 115200, uhf_baudrate, "UHF", self.usingFec)
        self.interfaceName = "UHF"
    def _sband(self):
        self.interfaceName = "S-BAND"
        libcsp.sband_init(self.usingFec)


class UHF_CSPHandler(CSPHandler):
    def __init__(self, addr, interface, device, hmacKey, useFec):
        # This probably violates some essential law of programming
        # but this whole module is *different* so... Yeah
        from uTransceiver import uTransceiver
        if interface != "sdr":
            raise ValueError("UHF CSP handler works only with sdr interface")
        self.uTrns = uTransceiver()
        super().__init__(addr, interface, device, hmacKey, useFec)


    def send(self, server, port, buf : bytearray):
        self.uTrns.handlePipeMode()
        super().send(server, port, buf)
