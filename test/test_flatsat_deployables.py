'''
 * Copyright (C) 2021  University of Alberta
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
 * @file test_flatsat_deployables.py
 * @author Daniel Sacro
 * @date 2022-03-18
'''

'''Please note that all the tests in this file cannot be automated'''

import time
import numpy as np

from groundstation_tester import Tester
from eps.expected_eps_hk import expected_EPS_HK
from test_full_hk import testSystemWideHK

tester = Tester()

def testAllCommandsToOBC():
    # Commisioning/LEOP Test - Cannot be automated. Requires a visual inspection of the burn wires, a release of physical switches, and watching mechanisms deploy

    # Manual Deployment Test - Cannot be automated. Requires a visual inspection of the burn wires, a release of physical switches, and watching mechanisms deploy

    # Failure to Deploy Test - Cannot be automated. Requires the securing and releasing of physical switches

    tester.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
