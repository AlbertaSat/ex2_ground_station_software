'''
 * Copyright (C) 2023  University of Alberta
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
 * @file receiveNVoices.py
 * @author Ron Unrau
 * @date 2023-02-23
'''

import libcsp_py3 as libcsp
import socket

class ReceiveNorthernVoices:
    def __init__(self, networkManager):
        self.csp = networkManager
        # Note: NV broadcasts on port 24
        self.sock = self.csp.listen(24)
        self.conn = None

    def receiveFile(self, name: str, wait):
        print("accepting transmission to file {}".format(name))
        if self.conn is None:
            self.conn = self.csp.accept(self.sock, wait)
        if self.conn is None:
            print("no connection after {} seconds".format(wait))
            return 0

        bs = 512
        cnt = 0
        while bs == 512:
            pkt = self.csp.read(self.conn, 10000)
            if pkt is None:
                print("read timed out")
                break
            data = bytearray(libcsp.packet_get_data(pkt))
            bs = int.from_bytes(data[0:2], byteorder='big')
            cnt += bs
            print("bs {} cnt {}".format(bs, cnt))
            with open("nv.c2", 'ab+') as f:
                f.write(data[4:])

        print("received {} bytes".format(cnt))
        return cnt

    def receiveStream(self, port, wait):
        print("streaming transmission to tcp port {}".format(port))
        if self.conn is None:
            self.conn = self.csp.accept(self.sock, wait)
        if self.conn is None:
            print("no connection after {} seconds".format(wait))
            return 0

        # buffer the entire transmission into a single bytearray
        bs = 512
        buf = bytearray()
        while bs == 512:
            pkt = self.csp.read(self.conn, 10000)
            if pkt is None:
                print("read timed out");
                break
            data = bytearray(libcsp.packet_get_data(pkt))
            bs = int.from_bytes(data[0:2], byteorder='big')
            pktnum = int.from_bytes(data[2:4], byteorder='big')
            print("bs {} pktnum {}".format(bs, pktnum))
            buf.extend(data[4:])

        print("received {} bytes".format(len(buf)))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", port))
        sent = 0
        while sent < len(buf):
            rc = s.send(buf[sent:])
            if rc == 0:
                print("connection lost")
                break
            sent = sent + rc

        return len(buf)

    def close(self):
        if self.conn:
            self.csp.close(self.conn)
        self.conn = None
