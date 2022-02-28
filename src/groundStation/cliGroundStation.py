"""
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
"""
"""
 * @file cliGroundStation.py
 * @author Robert Taylor
 * @date 2021-12-21
"""
from groundStation import groundStation
from groundStation.commandParser import cliCommandParser
import libcsp_py3 as libcsp

class cliGroundStation(groundStation.groundStation):
    def __init__(self, opts):
        super().__init__(opts)
        self.parser = cliCommandParser()

    def transaction(self, server, port, buf):
        """ Execute CSP transaction - send and receive on one RDP connection and
        return parsed packet """
        conn = self.__connectionManager__(server, port)
        if conn is None:
            print('Error: Could not connection')
            return
        libcsp.send(conn, buf)
        libcsp.buffer_free(buf)

        while True:
            packet = libcsp.read(conn, 10000)
            if packet is None:
                print('packet is None; no more packets')
                return

            data = bytearray(libcsp.packet_get_data(packet))
            length = libcsp.packet_get_length(packet)
            print("{}".format(data[2:].decode()), end='')
            if data[1] == 0:
                break
        return
        