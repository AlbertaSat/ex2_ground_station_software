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
 * @file test_flatsat_aurora.py
 * @author Daniel Sacro
 * @date 2022-03-22
'''

'''Please note that many of the ground station commands and housekeeping variables needed in this file do not yet exist at the time of last edit'''
import time
import numpy as np

import sys
import os
from testLib import testLib as test
sys.path.append("./src")
from groundStation import groundStation

import numpy as np

opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())

test = test() #call to initialize local test class

# TODO - Automate the remaining steps in the OBC Firmware Update test - 1, 3-8
def testFirmwareUpdate():
    # 1) Develop a new payload firmware image. Ensure that this image has a different version ID than the currently flashed image

    # 2) Ensure OBC, UHF, EPS, and payload are turned on (Doesn't have to be automated)

    # 3) Retrieve the current payload firmware version ID and display it on the ground station CLI
    # To pass test, version ID should be that of the current working firmware image

    # 4) Send the new firmware image over UHF to the OBC. The new image should have identical functionality to the one being
    # replaced, but with a unique firmware version ID number

    # 5) Command the OBC to reprogram the payload

    # 6) Retrieve the current payload firmware version ID and display it on the ground station CLI
    # To pass test, version ID should be different from the one in step 3

    # 7) Repeat steps 4 and 5, but with a new firmware image having a unique firmware version ID number and incorrect CRC bits

    # 8) Repeat step 6
    # To pass test, version ID should be the same as the one from step 6

    # PASS CONDITION: The version ID displayed in step 3 is that of the current working firmware image
    #                 The version ID displayed in step 6 is the ID of the new updated firmware image, which is different from step 3's ID
    #                 The version ID displayed in step 8 is the same ID as the one from step 6
    return True

# TODO - Automate the remaining steps in the EPS Ping Watchdog test - 2-4
def test_EPS_pingWatchdog():
    testPassed = "Pass"
    # 1) Ensure OBC, UHF, EPS, Charon, S Band, and NIM are turned on (Doesn't need to be automated)

    # 2) Ensure that the OBC is operating in such a way that it will respond to ping requests of CSP ID 1

    # 3) Configure an EPS ping watchdog to check CSP ID 1 every 5 mins and toggle EPS output 6 for 10 seconds if it times out

    # 4) Enable OBC to check NIM's operating status every 5 min by verifying the that the firmware version number can be read.
    # OBC will command EPS to reset power channel 3 and 10 simultaneously for 10 seconds if the verification fails

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

    # 6) Disconnect UART connection between NIM and the OBC
    input("\nPlease disconnect the UART connection between NIM and the OBC. Press enter to resume tests.\n") 

    # 7) Repeat step 5:
    for j in range(36): 
        server, port, toSend = gs.getInput('eps.cli.general_telemetry')
        response = gs.transaction(server, port, toSend)

        for val in test.expected_EPS_HK:
            # To pass test, all active power channels have output state = 1 except channel 10, which should be 0
            colour = '\033[0m' #white
            if val in pchannels:
                if (response[val] == 0) and (val != 'pchannel10'):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                elif (response[val] == 1) and (val == 'pchannel10'):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                else:
                    colour = '\033[92m' #green
            print(colour + str(val) + ": " + str(response[val]))
            
        time.sleep(10)

    # 8) Reconnect  UART connection between NIM and the OBC
    input("\nPlease Reconnect the UART connection between NIM and the OBC. Press enter to resume tests.\n")  

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - EPS PING WATCHDOG TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: During step 5, Output State = 1 for all active power channels at all times
    #                 During step 7, Output State = 1 for all active power channels except channel 10, which should be 0
    return True

# TODO - Automate the remaining steps in the Full Payload Functionality test - 2-6
def testFullPayloadFunctionality():
    # 1) Ensure that the OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware installed (Doesn't have to be automated)

    # 2) Upload 2 test images to the payload. Select the first image to be displayed during the next image capture

    # 3) Take a picture using the payload's camera and save it as a file on the OBC

    # 4) Switch the image displayed on the screen to the second image, and take a picture using the payload's camera and save it as a file on the OBC

    # 5) Send a command to downlink both OBC picture files over UHF

    # 6) Send a command to downlink both OBC picture files over S Band

    # PASS CONDITION: Both pictures are received uncorrupted at the ground staiton PC and show the correct test images to displayed on the payload
    #                 screen with the background being the test area.
    #                 The images received over S Band and UHF are identical. 
    return True

def testAllCommandsToOBC():
    # TODO - Finish function implementation
    print("\n---------- FIRMWARE UPDATE TEST ----------\n")
    testFirmwareUpdate()

    print("\n---------- OBC HOUSEKEEPING TEST ----------\n")
    test.testHousekeeping(1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0)

    # TODO - Finish function implementation
    print("\n---------- EPS PING WATCHDOG TEST ----------\n")
    test_EPS_pingWatchdog()

    # TODO - Finish function implementation
    print("\n---------- FULL PAYLOAD FUNCTIONALITY TEST ----------\n")
    testFullPayloadFunctionality()

    test.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
