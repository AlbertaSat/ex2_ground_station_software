from CSPHandler import getCSPHandler
from interactiveHandler import interactiveHandler
from inputHandler import inputHandler
from system import GroundNodes
from system import SatelliteNodes

class groundStation:
    def __init__(self, opts):
        keyfile = open(opts.hkeyfile, "r")
        hkey = keyfile.read().strip()
        try:
            if opts.u:
                self.networkManager = getCSPHandler(GroundNodes.GND.value, opts.interface, opts.device, hkey, "UHF")
            else:
                self.networkManager = getCSPHandler(GroundNodes.GND.value, opts.interface, opts.device, hkey)
        except Exception as e:
            print(e)
            exit(1)

        keyfile.close()
        self.interactive = interactiveHandler()
        self.inputHandler = inputHandler()
        self.setSatellite(opts.satellite)

    def run(self):
        raise NotImplementedError("groundStation.run() must be overwritten by derived class")

    def setSatellite(self, name):
        satelliteAddr = 0
        satelliteName = ''
        for i in SatelliteNodes.__members__.values():
            if i.name == name:
                satelliteAddr = i.value
                satelliteName = i.name
        if satelliteAddr == 0:
            raise Exception("Invalid satellite {}".format(name))
        self.satelliteAddr = satelliteAddr
        self.satellite = satelliteName