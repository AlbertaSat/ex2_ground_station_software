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
        self.interactive = InteractiveHandler()
        self.inputHandler = InputHandler()
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