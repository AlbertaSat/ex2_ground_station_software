from CSPHandler import getCSPHandler
from interactiveHandler import interactiveHandler
from inputHandler import inputHandler
from system import GroundNodes
from system import SatelliteNodes

class groundStation:
    def __init__(self, opts):
        keyfile = open(opts.hkeyfile, "r")
        hkey = keyfile.read().strip()
        if opts.u:
            self.networkManager = getCSPHandler(GroundNodes.GND.value, opts.interface, opts.device, hkey, "UHF")
        else:
            self.networkManager = getCSPHandler(GroundNodes.GND.value, opts.interface, opts.device, hkey)

        keyfile.close()
        self.interactive = interactiveHandler()
        self.inputHandler = inputHandler()
        self.satellite = opts.satellite

    def run(self):
        raise NotImplementedError("groundStation.run() must be overwritten by derived class")

    def set_satellite(self, name):
        if name not in SatelliteNodes.__members__.keys():
            raise ValueError("Satellite \'{}\' not in {}".format(name, str(self.apps.keys())))
        else:
            self.satellite = name;