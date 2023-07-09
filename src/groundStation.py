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
 * @file groundStation.py
 * @author Robert Taylor
 * @date 2022-07-21
'''

from CSPHandler import getCSPHandler
from interactiveHandler import InteractiveHandler
from inputHandler import InputHandler
from system import GroundNodes
from system import SatelliteNodes

class GroundStation:
    """This is the base class that CLI extends.
    Attributes:
        networkManager: an object that uses the CubeSat Protocol to establish a network connection
        interactive: an object that handles the keyboard input
        inputHandler: an object that logs in the keyboard input
    """
    def __init__(self, opts):
        hkeyfile = open(opts.hkeyfile, "rb")
        hkey = hkeyfile.read()
        xkeyfile = open(opts.xkeyfile, "rb")
        xkey = xkeyfile.read()
        addr = 0
        nodeType = "UHF"
        # GroundNodes = [("GND", "UHF", 16), ("GND", "SBAND", 17), ("GND", "PIPE", 24), ("GND", "BEACON", 99)]
        for i in GroundNodes:
            if i[1] == nodeType:
                addr = i[2]         # Q: so why not just set addr to 16?
                break;
        try:
            if opts.u:
                self.networkManager = getCSPHandler(addr, opts.interface, opts.device, hkey, xkey, "UHF", useFec = opts.fec)
            else:
                self.networkManager = getCSPHandler(addr, opts.interface, opts.device, hkey, xkey, useFec = opts.fec)
        except Exception as e:
            raise
            print(e)
            exit(1)

        self.interactive = InteractiveHandler(opts.interface == "dummy")
        self.inputHandler = InputHandler()
        self.setSatellite(opts.satellite)

    def run(self):
        raise NotImplementedError("groundStation.run() must be overwritten by derived class")

    def setSatellite(self, name):
    """Finds the satellite address by querying the argument name in a list"""
        satelliteAddr = 0
        satelliteName = ''          # A: do we really need this given that's literally the argument?
        # searches within SatelliteNodes such as ("OBC", "EX2", 1), ("OBC", "YKS", 2), ("OBC", "ARS", 3), ("EPS", "EX2_EPS", 4), ("EPS", "YKS_EPS", 6), ("EPS", "ARS_EPS", 5)
        for i in SatelliteNodes:
            if i[1] == name:
                satelliteAddr = i[2]
                satelliteName = i[1]
                # A: can have a break here
        if satelliteAddr == 0:
            raise Exception("Invalid satellite {}".format(name))
        self.satelliteAddr = satelliteAddr      # PEP: these attributes should be defined in init
        self.satellite = satelliteName
