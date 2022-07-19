from multiprocessing.sharedctypes import Value
import libcsp_py3 as libcsp
from packetMaker import packetMaker
from packetBreaker import packetBreaker
from connectionManager import connectionManager
import serial
from system import SatelliteNodes

def getCSPHandler(addr, interface, device, hmacKey, protocol = None):
    if protocol is None:
        return CSPHandler(addr, interface, device, hmacKey)
    elif protocol == "UHF":
        return UHF_CSPHandler(addr, interface, device, hmacKey)
    else:
        raise ValueError("Protocol {} does not exist for CSP handlers".format(protocol))

class CSPHandler:

    #TODO: maybe a factory pattern here?

    # 'addr' groundstation's address
    # 'interface' interface to use
    # 'device' device file interface is to write to
    # 'hmacKey' key to use for HMAC authentication
    def __init__(self, addr, interface, device, hmacKey):
        self.packetBuilder = packetMaker()
        self.packetExtractor = packetBreaker()
        self.connectionManager = connectionManager()

        self.myAddr = addr;
        self.numberOfBuffers = 100
        self.bufferSize = 1024 #This is max size of an incoming packet
        libcsp.init(self.myAddr, 'GroundStation', 'model', '1.2.3', self.numberOfBuffers, self.bufferSize)
        libcsp.hmac_set_key(hmacKey, len(hmacKey))

        self.interfaceName = ""
        if interface == 'uart':
            self.ser = self.__uart__(device)
        elif interface == 'uhf':
            self.__sdr__(device, libcsp.SDR_UHF_9600_BAUD)
        elif interface == 'sband':
            raise NotImplementedError("Sband support not yet implemented")
    
        stringBuild = ""
        for node in SatelliteNodes:
            stringBuild = stringBuild + " {} {} ".format(node.value, self.interfaceName)
        libcsp.rtable_load(stringBuild)

        libcsp.route_start_task()


    def send(self, server, port, buf : bytearray):
        packet = self.packetBuilder.makePacket(buf)
        conn = self.connectionManager.getConn(server,port)
        libcsp.send(conn, packet)
        libcsp.buffer_free(packet)

    def receive(self, server, port, timeout):
        conn = self.connectionManager.getConn(server,port)
        packet = libcsp.read(conn, timeout)
        data = None
        if packet is not None:
            data = self.packetExtractor.breakPacket(packet)
            libcsp.buffer_free(packet)
        return data

    def __uart__(self, device):
        """ initialize uart interface """
        ser = serial.Serial(device,
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=2,
        timeout=1)

        libcsp.kiss_init(device, ser.baudrate, 512, 'uart')
        self.interfaceName = "uart"

    def __sdr__(self, device, uhf_baudrate):
        """ Initialize SDR interface """
        libcsp.sdr_init(device, 115200, uhf_baudrate, "UHF")
        self.interfaceName = "UHF"


class UHF_CSPHandler(CSPHandler):
    def __init__(self, addr, interface, device, hmacKey):
        # This probably violates some essential law of programming
        # but this whole module is *different* so... Yeah
        from uTransceiver import uTransceiver
        if interface != "sdr":
            raise ValueError("UHF CSP handler works only with sdr interface")
        self.uTrns = uTransceiver()
        super().__init__(addr, interface, device, hmacKey)

    def send(self, server, port, buf : bytearray):
        self.uTrns.handlePipeMode()
        super().send(server, port, buf)