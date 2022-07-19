import libcsp_py3 as libcsp

class packetBreaker:
    def __init__(self):
        pass
    def breakPacket(self, packet):
        data = bytearray(libcsp.packet_get_data(packet))
        return data