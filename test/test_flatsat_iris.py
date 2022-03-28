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
 * @file test_flatsat_iris.py
 * @author Daniel Sacro
 * @date 2022-03-18
'''

'''Please note that many of the ground station commands and housekeeping variables needed in this file do not yet exist at the time of last edit'''

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

# TODO - Automate the remainings steps in the S-Band Downlink Uncompressed Test - 3-5
def test_sBandDownlinkUncompressed():
    # 1) Ensure OBC, S-Band transceiver, EPS, and electra are turned on, and that the OBC and Electra have the most up-to-date firmware installed, 
    # including Electra image acquisition parameters (Doesn't have to be automated)

    # 2) Establish [TBC test target set up, with lenses] in front of the Electra image sensor under test (Doesn't have to be automated)

    # 3) Command the OBC to deliver an imaging command to electra to acquire a SQUARE image file

    # 4) Command the OBC to instruct Electra to deliver the image file from Electra SDRAM uncompressed to the OBC for storage on the OBC SD card

    # 5) Command a downlink of the uncompressed image file from the OBC SD card via S-Band

    # PASS CONDITION: The uncompressed image file sent over S-Band is received and image characteristics meet the success criteria of Iris
    #                 component image testing. 
    return True

# TODO - Automate the remainings steps in the UHF Downlink Uncompressed Test - 3-5
def test_UHF_downlinkUncompressed():
    # 1) Attach Electra to the OBC and to the EPS via Charon. Attach UHF and associated components. Ensure that the OBC, UHF transceiver, EPS
    # and Electra are turned on, and than the OBC and Electra have the most up-to-date firmware installed, including Electra image acquisition
    # parameters (Doesn't have to be automated)

    # 2) Establish [TBC test target set up, with lenses] in front of the Electra image sensor under test (Doesn't have to be automated)

    # 3) Command the OBC to deliver an imaging command to Electra to acquire an image file

    # 4) Command the OBC to instruct Electra to deliver the image file from Electra SDRAM uncompressed to the OBC for storage on the OBC SD card

    # 5) Command a downlink of the uncompressed image file from the OBC SD card via UHF

    # PASS CONDITION: The uncompressed image file sent over UHF is received and image characterisitics meet the success criteria of Iris
    #                 component image testing    
    return True

# TODO - Automate the remainings steps in the S-Band Downlink Compressed Test - 3-7
def test_sBandDownlinkCompressed():
    # 1) Attach Electra to the OBC and to the EPS via Charon. Attach UHF and associated components. Ensure that the OBC, UHF transceiver, EPS
    # and Electra are turned on, and than the OBC and Electra have the most up-to-date firmware installed, including Electra image acquisition
    # parameters (Doesn't have to be automated)

    # 2) Establish [TBC test target set up, with lenses] in front of the Electra image sensor under test (Doesn't have to be automated)

    # 3) Command the OBC to deliever an imaging command to Electra to acquire an image file

    # 4) Command the OBC to instruct Electra to compress the image file and return it to Electra SDRAM

    # 5) Command the OBC to instruct Electra to deliver the compressed image file from Electra SDRAM to the OBC for storage on the OBC SD card

    # 6) Command a downlink of the compressed image file from the OBC SD card via S-Band

    # 7) Decompress the image on the ground station

    # PASS CONDITION: The compressed image file sent over S-Band is received and image characteristics meet the success criteria of Iris 
    #                 component image testing
    return True

# TODO - Automate the remainings steps in the UHF Downlink Compressed Test - 3-6
def test_UHF_downlinkCompressed():
    # 1) Attach Electra to the OBC and to the EPS via Charon. Attach UHF and associated components. Ensure that the OBC, UHF transceiver, EPS
    # and Electra are turned on, and than the OBC and Electra have the most up-to-date firmware installed, including Electra image acquisition
    # parameters (Doesn't have to be automated)

    # 2) Establish [TBC test target set up, with lenses] in front of the Electra image sensor under test (Doesn't have to be automated)

    # 3) Command the OBC to deliever an imaging command to Electra to acquire an image file

    # 4) Command the OBC to instruct Electra to compress the image file and return it to Electra SDRAM

    # 5) Command the OBC to instruct Electra to deliver the compressed image file from Electra SDRAM to the OBC for storage on the OBC SD card

    # 6) Command a downlink of the compressed image file from the OBC SD card via UHF

    # PASS CONDITION: The compressed image file sent over UHF is received and image characteristics meet the success criteria of Iris 
    #                 component image testing
    return True

# TODO - Automate the remainings steps in the S-Band Downlink Test - 3-8
def test_irisFirmwareUpdate():
    # 1) Develop a new Electra FPGA program. Ensure that this image has a different firmware version number than the currently flashed Electra image

    # 2) Ensure that the OBC, UHF, EPS, and Electra are turned on, and that the OBC has the most up-to-date firmware installed

    # 3) Retrieve the current firmware version ID of Electra and display it on the ground station CLI

    # 4) Send the new Electra FPGA configuration over UHF to the OBC. This new image should have identical functionality to the one being replaced,
    # but with a unique firmware version ID number

    # 5) Command the OBC to reprogram Electra

    # 6) Repeat step 3
    
    # To pass test, the current version ID must be different from the last version ID

    # 7) Repeat step 4 and 5, but with a new firmware image having a unique firmware version ID number and incorrect CRC bits

    # 8) Repeat step 3

    # To pass test, the current

    # PASS CONDITION: The version ID displayed during step 3 is that of the current working firmware image
    #                 The version ID displayed during step 6 is the ID of the new, updated firmware image, which is different from the one in step 3
    #                 The version ID displayed during step 8 is the same ID as the one from step 6
    return True

# TODO - Automate the remaining steps in the EPS Ping Watchdog test - 2-4
def test_EPS_pingWatchdog():
    testPassed = "Pass"
    # 1) Ensure OBC, UHF, EPS, Charon, Sband, and Iris are turned on (Doesn't have to be automated)

    # 2) Ensure that the OBC is operating in such a way that it will respond to ping requests of CSP ID 1

    # 3) Configure an EPS and OBC ping watchdogs to check CSP ID 1 every 5 mins and toggle EPS output 6 for 10 seconds if it times out

    # 4) Enable OBC to check Iris' operating status every 5 min by verifying that the firmwar version number can be read. 
    # OBC will command EPS to reset power channel 3 and 10 simultaneously for 10 seconds if verification fails

    # TODO "pchannelX" (where X = a num from 1-9) doesn't exist yet. The name is just a placeholder, so replace them with the right HK names
    pchannels = ['pchannel1', 'pchannel2', 'pchannel3', 'pchannel4', 'pchannel5', 'pchannel6', 'pchannel7', 'pchannel8','pchannel9', 'pchannel10']

    # 5) Repeat the following every 10 seconds for 6 minutes:
    for i in range(36): 
        # Gather all EPS HK info
        server, port, toSend = gs.getInput('eps.cli.general_telemetry')
        response = gs.transaction(server, port, toSend)
        
        # Display data on ground station CLI
        for val in test.expected_EPS_HK:
            # To pass test, all active power channels have output state = 1
            colour = '\033[0m' #white
            if val in pchannels:
                if (response[val] == 0):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                else:
                    colour = '\033[92m' #green
            print(colour + str(val) + ": " + str(response[val]))

        time.sleep(10)

    # 6) Disconnect CAN connection between Iris and OBC
    input("\nPlease disconnect the CAN connection between Iris and the OBC. Press enter to resume tests.\n") 

    # 7) Repeat step 5:
    for j in range(36): 
        server, port, toSend = gs.getInput('eps.cli.general_telemetry')
        response = gs.transaction(server, port, toSend)

        for val in test.expected_EPS_HK:
            # To pass test, all active power channels have output state = 1 except channels 3 and 10, which should be 0
            colour = '\033[0m' #white
            if val in pchannels:
                if (response[val] == 0) and (val != 'pchannel3') and (val != 'pchannel10'):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                elif (response[val] == 1) and (val == 'pchannel3' or val == 'pchannel10'):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                else:
                    colour = '\033[92m' #green
            print(colour + str(val) + ": " + str(response[val]))
            
        time.sleep(10)

    # 8) Reconnect CAN connection between Iris and OBC
    input("\nPlease Reconnect the CAN connection between the Iris and the OBC. Press enter to resume tests.\n")  

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - EPS PING WATCHDOG TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: During step 5, Output State = 1 for all active power channels at all times
    #                 During step 7, Output State = 1 for all active power channels except channels 3 and 10, which should both be 0
    return True

def testAllCommandsToOBC():
    print("\n---------- OBC SYSTEM-WIDE HOUSEKEEPING TEST ----------\n")
    test.testHousekeeping(1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0)

    # TODO - Finish function implementation
    print("\n---------- DATA ACQUISITION TO FILE AND DOWNLINK OVER S-BAND (UNCOMPRESSED) TEST ----------\n")
    test_sBandDownlinkUncompressed()

    # TODO - Finish function implementation
    print("\n---------- DATA ACQUISITION TO FILE AND DOWNLINK OVER UHF (UNCOMPRESSED) TEST ----------\n")
    test_UHF_downlinkUncompressed()

    # TODO - Finish function implementation
    print("\n---------- DATA ACQUISITION TO FILE AND DOWNLINK OVER S-BAND (COMPRESSED) TEST ----------\n")
    test_sBandDownlinkCompressed()

    # TODO - Finish function implementation
    print("\n---------- DATA ACQUISITION TO FILE AND DOWNLINK OVER UHF (COMPRESSED) TEST ----------\n")
    test_UHF_downlinkCompressed()
    
    # TODO - Finish function implementation
    print("\n---------- IRIS FIRMWARE OVER UHF UPDATE TEST ----------\n")
    test_irisFirmwareUpdate()

    # TODO - Finish function implementation
    print("\n---------- EPS PING WATCHDOG TEST ----------\n")
    test_EPS_pingWatchdog()

    test.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
