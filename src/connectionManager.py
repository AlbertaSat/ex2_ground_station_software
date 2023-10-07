"""
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
"""
"""
 * @file connectionManager.py
 * @author Robert Taylor
 * @date 2022-07-21
"""

import time
import libcsp_py3 as libcsp
from collections import defaultdict


class ConnectionManager:
    def __init__(self):
        self.server_connection = defaultdict(dict)

    def getConn(self, server, port):
        if (
            server not in self.server_connection
            or port not in self.server_connection[server]
        ):
            try:
                if server in (4, 5, 6):
                    conn = libcsp.connect(
                        libcsp.CSP_PRIO_NORM, server, port, 1000, libcsp.CSP_O_CRC32
                    )
                else:
                    conn = libcsp.connect(
                        libcsp.CSP_PRIO_NORM,
                        server,
                        port,
                        1000000000,
                        libcsp.CSP_SO_HMACREQ
                        | libcsp.CSP_SO_CRC32REQ
                        | libcsp.CSP_SO_XTEAREQ,
                    )
            except Exception as e:
                print(e)
                return None

            self.server_connection[server][port] = conn
        return self.server_connection[server][port]
