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