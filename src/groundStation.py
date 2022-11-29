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
    def __init__(self, opts):
        hkeyfile = open(opts.hkeyfile, "rb")
        hkey = hkeyfile.read()
        xkeyfile = open(opts.xkeyfile, "rb")
        xkey = xkeyfile.read()
        addr = 0
        nodeType = "UHF"
        for i in GroundNodes:
            if i[1] == nodeType:
                addr = i[2]
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
        satelliteAddr = 0
        satelliteName = ''
        for i in SatelliteNodes:
            if i[1] == name:
                satelliteAddr = i[2]
                satelliteName = i[1]
        if satelliteAddr == 0:
            raise Exception("Invalid satellite {}".format(name))
        self.satelliteAddr = satelliteAddr
        self.satellite = satelliteName
