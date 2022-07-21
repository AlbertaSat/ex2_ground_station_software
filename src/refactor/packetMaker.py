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
 * @file packetMaker.py
 * @author Robert Taylor
 * @date 2022-09-21
'''

import libcsp_py3 as libcsp

class packetMaker:
    def __init__(self):
        pass
    def makePacket(self, data : bytearray):
        packet = libcsp.buffer_get(len(data))
        if len(data) > 0:
            libcsp.packet_set_data(packet, data)
            return packet
        # TODO: use exceptions
        return None