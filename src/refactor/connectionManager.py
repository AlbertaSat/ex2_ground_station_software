import time
import libcsp_py3 as libcsp
from collections import defaultdict

class connectionManager:
    def __init__(self):
        self.server_connection = defaultdict(dict)
        self.rdp_timeout = 10000
    def getConn(self, server, port):
        # TODO: This is bad
        current = time.time()
        timeout = self.rdp_timeout / 1000
        if server not in self.server_connection or port not in self.server_connection[
                server] or self.server_connection[server][port]['time initialized'] + timeout <= current:
            if server in self.server_connection and port in self.server_connection[
                    server] and self.server_connection[server][port]['time initialized'] + timeout <= current:
                libcsp.close(self.server_connection[server][port]['conn'])
            try:
                if server == 4:
                    conn = libcsp.connect(libcsp.CSP_PRIO_NORM, server, port, 1000, libcsp.CSP_O_CRC32)
                else:
                    conn = libcsp.connect(libcsp.CSP_PRIO_NORM, server, port, 1000000000, libcsp.CSP_SO_HMACREQ | libcsp.CSP_SO_CRC32REQ)
            except Exception as e:
                print(e)
                return None

            self.server_connection[server][port] = {
                'conn': conn,
                'time initialized': time.time()
            }

        return self.server_connection[server][port]['conn']