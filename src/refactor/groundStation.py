from CSPHandler import CSPHandler
from interactiveHandler import interactiveHandler
from inputHandler import inputHandler
from system import GroundNodes

class groundStation:
    def __init__(self, opts):
        keyfile = open(opts.hkeyfile, "r")
        hkey = keyfile.read().strip()
        self.networkManager = CSPHandler(GroundNodes.GND.value, opts.interface, opts.device, hkey)
        keyfile.close()
        self.interactive = interactiveHandler()
        self.inputHandler = inputHandler()
        self.satellite = opts.satellite

    def run(self):
        raise NotImplementedError("groundStation.run() must be overwritten by derived class")