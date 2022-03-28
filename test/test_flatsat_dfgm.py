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
 * @file test_flatsat_dfgm.py
 * @author Daniel Sacro
 * @date 2022-03-18
'''

'''Please note that many of the ground station commands and housekeeping variables needed in this file do not yet exist at the time of last edit'''
'''Also please note that processing for 10 Hz DFGM data is not implemented into the DFGM software. It was decided that 1 Hz and 100 Hz data
would be more than enough data.'''

import time
import sys
from testLib import testLib as test
from os import path
sys.path.append("./src")
from groundStation import groundStation

import numpy as np

opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())

test = test() #call to initialize local test class

# TODO - Automate the remaining steps in the DFGM Data Acquisition and S Band Downlink test - 3, 4
def test_DFGM_dataAcquisitionAndSBandDownlink():
    testPassed = "Pass"
    # 1) Ensure that the OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware installed (Doesn't have to be automated)

    # 2) Turn the DFGM on for 10 seconds and have the OBC process the data output by the DFGM into 1 Hz, 10 Hz, and 100 Hz data. Store them as separate
    # files on the SD card. This data will just be used for testing, and will consist of background magnetic signatures
    server, port, toSend = gs.getInput('obc.dfgm.dfgm_run(10)')
    response = gs.transaction(server, port, toSend)
    if (response['err'] != 0):
        testPassed = "Fail"
    time.sleep(11)

    # 3) Downlink a 1 Hz DFGM data file over the S-Band connection, and save it to the personal computer

    # 4) Repeat step 3 for the 10 Hz and 100 Hz DFGM data

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - DFGM DATA ACQUISITION AND SBAND DOWNLINK TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: The data packet should be visible on the ground station computer and able to open and read within 5 seconds of downlink
    #                 All DFGM data magnitude and direction is within +/- 10% of expected magnetic field at the time, position, and orientation of the test,
    #                 with an expected level of noise and interference present
    #                 Each frequency of DFGM data type corresponds to a different data file, so the data on each type of packet should be different from each other
    return True

# TODO - Automate the remaining steps in the DFGM Data Acquisition and UHF Downlink test - 3, 4
def test_DFGM_dataAcquisitionAnd_UHF_Downlink():
    testPassed = "Pass"
    # 1) Ensure that the OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware installed (Doesn't have to be automated)

    # 2) Turn the DFGM on for 10 seconds and have the OBC process the data output by the DFGM into 1 Hz, 10 Hz, and 100 Hz data. Store them as separate
    # files on the SD card
    server, port, toSend = gs.getInput('obc.dfgm.dfgm_run(10)')
    response = gs.transaction(server, port, toSend)
    if (response['err'] != 0):
        testPassed = "Fail"
    time.sleep(11)

    # 3) Downlink a 1 Hz DFGM data file over the UHF connection, and save it to the personal computer

    # 4) Repeat step 3 for 10 Hz and 100 Hz DFGM data

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - DFGM DATA ACQUISITION AND UHF DOWNLINK TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: The data packet should be visible on the ground station computer and able to open and read within 5 seconds of downlink
    #                 The packet should not be empty, and should contain data that corresponds to a magnetic field reading of the immediate area
    #                 Each frequency of DFGM data type corresponds to a different data file, so the data on each type of packet should be different from each other
    return True

def testAllCommandsToOBC():
    print("\n---------- OBC SYSTEM-WIDE HOUSEKEEPING TEST ----------\n")
    test.testHousekeeping(1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0)

    # TODO - Finish function implementation
    print("\n---------- DFGM DATA ACQUISITION AND SBAND DOWNLINK TEST ----------\n")
    test_DFGM_dataAcquisitionAndSBandDownlink()

    # TODO - Finish function implementation
    print("\n---------- DFGM DATA ACQUISITION AND SBAND DOWNLINK TEST ----------\n")
    test_DFGM_dataAcquisitionAnd_UHF_Downlink()

    test.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
