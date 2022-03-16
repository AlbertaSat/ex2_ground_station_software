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
 * @file test_core_comp.py
 * @author Daniel Sacro
 * @date 2022-3-10
'''
import time
import numpy as np
from testLib import testLib as test
from groundStation import groundStation

opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())

test = test() #call to initialize local test class

# TODO - Automate the remaining steps in the EPS test - 2, 3, 4, 10, 12
def test_EPS_pingWatchdog():
    testPassed = "Pass"
    # 1) Ensure OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware installed (Doesn't have to be automated)

    # 2) Ensure that the OBC is operating in such a way that it will respond to ping requests of CSP ID 1

    # 3) Configure an EPS ping watchdog to check CSP ID 1 every 5 mins and toggle EPS output 6 for 10 seconds if it times out

    # 4) Enable OBC to check UHF operating status every 5 min by verifying the software version. OBC will command EPS to reset power channel 8 for 10 seconds if verification fails

    # TODO "pchannelX" (where X = a num from 1-9) doesn't exist yet. The name is just a placeholder, so replace them with the right HK names
    pchannels = ['pchannel1', 'pchannel2', 'pchannel3', 'pchannel4', 'pchannel5', 'pchannel6', 'pchannel7', 'pchannel8','pchannel9']

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

    # 6) Disconnect UART connection between UHF and OBC
    input("\nPlease disconnect the UART connection between the UHF and OBC. Press enter to resume tests.\n") 

    # 7) Repeat step 5:
    for j in range(36): 
        server, port, toSend = gs.getInput('eps.cli.general_telemetry')
        response = gs.transaction(server, port, toSend)

        for val in test.expected_EPS_HK:
            # To pass test, all active power channels have output state = 1 except channel 8, which should be 0
            colour = '\033[0m' #white
            if val in pchannels:
                if (response[val] == 0) and (val != 'pchannel8'):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                elif (response[val] == 1) and (val == 'pchannel8'):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                else:
                    colour = '\033[92m' #green
            print(colour + str(val) + ": " + str(response[val]))
            
        time.sleep(10)

    # 8) Reconnect UART connection between UHF and OBC
    input("\nPlease Reconnect the UART connection between the UHF and OBC. Press enter to resume tests.\n")  

    # 9) Wait 30 seconds
    time.sleep(30) 

    # 10) Tell OBC to stop responding to ping requests

    # 11) Repeat step 5:
    for k in range(36): 
        server, port, toSend = gs.getInput('eps.cli.general_telemetry')
        response = gs.transaction(server, port, toSend)

        for val in test.expected_EPS_HK:
            # To pass test, all active power channels have output state = 1 except channels 6 and 9, which should both be 0
            colour = '\033[0m' #white
            if val in pchannels:
                if (response[val] == 0) and (val != 'pchannel6') and (val != 'pchannel9'):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                elif (response[val] == 1) and (val == 'pchannel6' or val == 'pchannel9'):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                else:
                    colour = '\033[92m' #green
            print(colour + str(val) + ": " + str(response[val]))

        time.sleep(10)

    # 12) Disable EPS ping watchdog and UHF verification check

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - EPS PING WATCHDOG TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: During step 5, Output State = 1 for all active power channels at all times
    #                 During step 7, Output State = 1 for all active power channels except channel 8, which should be 0
    #                 During step 11, Output State = 1 for all active power channels except channels 6 and 9, which should both equal 0
    return True

def test_GS_pingWatchdog():
    testPassed = "Pass"
    # 1) Ensure OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware installed (Doesn't have to be automated)

    # 2) Gather all EPS HK info
    server, port, toSend = gs.getInput('eps.cli.general_telemetry')
    response = gs.transaction(server, port, toSend)

    # 3) Display data on ground station CLI
    for val in test.expected_EPS_HK:
        # To pass test, ground station WDT remaining time is < 86300 seconds
        colour = '\033[0m' #white
        if (val == 'gs_wdt_time_left_s'):
            if (response['gs_wdt_time_left_s'] >= 86300):
                testPassed = "Fail"
                colour = '\033[91m' #red
            else:
                colour = '\033[92m' #green
        print(colour + str(val) + ": " + str(response[val]))

    # 4) Reset the ground station watchdog timer
    server, port, toSend = gs.getInput('eps.ground_station_wdt.reset')
    response = gs.transaction(server, port, toSend)

    # 5) Repeat steps 2 & 3 within 100 seconds of step 4
    server, port, toSend = gs.getInput('eps.cli.general_telemetry')
    response = gs.transaction(server, port, toSend)

    for val in test.expected_EPS_HK:
        # To pass test, ground station WDT remaining time is > 86300 seconds
        colour = '\033[0m' #white
        if (val == 'gs_wdt_time_left_s'):
            if (response['gs_wdt_time_left_s'] <= 86300):
                testPassed = "Fail"
                colour = '\033[91m' #red
            else:
                colour = '\033[92m' #green
        print(colour + str(val) + ": " + str(response[val]))

    # Take note of the test's result
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - GROUND STATION PING WATCHDOG TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: Ground Station WDT Remaining Time displayed in step 3 is less than 86300 seconds
    #                 Ground Station WDT Remaining Time displayed in step 5 is greater than 86300 seconds
    return True 

# TODO - Automate the remaining steps in the OBC Firmware Update test - 3, 4, 6
def test_OBC_firmwareUpdate():
    testPassed = "Pass"
    goldenImage_ID = 1 # TODO - Replace the current value here with the actual golden image version ID

    # 1) Ensure OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware installed (Doesn't have to be automated)

    # 2) Retrieve the current firmware version ID and display it on the ground station CLI
    server, port, toSend = gs.getInput('OBC.housekeeping.get_hk(1, 0, 0)')
    response = gs.transaction(server, port, toSend)
    currentVersion = response['OBC_software_ver']
    print("Current firmware/software version ID: " + str(currentVersion))
    # To pass test, current version should NOT be the "golden" image
    if (currentVersion == goldenImage_ID):
        testPassed = "Fail"

    # 3) Reset the OBC into a mode in which the working firmware image can be updated

    # 4) Update the working firmware image by uploading a new image
    # New image should have identical functionality to the one being replaced, but with a unique firmware version ID

    # 5) Repeat step 2
    server, port, toSend = gs.getInput('OBC.housekeeping.get_hk(1, 0, 0)')
    response = gs.transaction(server, port, toSend)
    lastVersion = currentVersion
    currentVersion = response['OBC_software_ver']
    print("Current firmware/software version ID: " + str(currentVersion))
    # To pass test, current version should be different than the version retrieved in step 2
    if (currentVersion == lastVersion):
        testPassed = "Fail"

    # 6) Repeat steps 3 & 4, but with a new firmware image having a unique version ID number and incorrect CRC bits

    # 7) Repeat step 2
    server, port, toSend = gs.getInput('OBC.housekeeping.get_hk(1, 0, 0)')
    response = gs.transaction(server, port, toSend)
    lastVersion = currentVersion
    currentVersion = response['OBC_software_ver']
    print("Current firmware/software version ID: " + str(currentVersion))
    # To pass test, current version should be the same as the version retrieved in step 5
    if (currentVersion != lastVersion):
        testPassed = "Fail"

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - OBC FIRMWARE UPDATE TEST ' + testPassed + '\n\n' + '\033[0m')
    
    # PASS CONDITION: Firmware version ID displayed in step 2 is the current working firmware image, not the "golden" image
    #                 Firmware version ID displayed in step 5 is the new updated firmware image, which is different than the one in step 2
    #                 Firmware version ID displayed in step 7, is the same as the ID from step 5
    return True

# TODO - Automate the remaining steps in the OBC Golden Firmware Update test - 3
def test_OBC_goldenFirmwareUpdate():
    testPassed = "Pass"
    goldenImage_ID = 1 # TODO - Replace the current value here with the actual golden image version ID

    # 1) Ensure OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware installed (Doesn't have to be automated)

    # 2) Retrieve the current firmware version ID and display it on the ground station CLI
    server, port, toSend = gs.getInput('OBC.housekeeping.get_hk(1, 0, 0)')
    response = gs.transaction(server, port, toSend)
    currentVersion = response['OBC_software_ver']
    print("Current firmware/software version ID: " + str(currentVersion))
    # To pass test, current version should NOT be the "golden" image
    if (currentVersion == goldenImage_ID):
        testPassed = "Fail"

    # 3) Reset the OBC and have it boot the "golden" firmware image

    # 4) Repeat step 2
    server, port, toSend = gs.getInput('OBC.housekeeping.get_hk(1, 0, 0)')
    response = gs.transaction(server, port, toSend)
    currentVersion = response['OBC_software_ver']
    print("Current firmware/software version ID: " + str(currentVersion))
    # To pass test, current version should be the "golden" image
    if (currentVersion != goldenImage_ID):
        testPassed = "Fail"

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - OBC GOLDEN FIRMWARE UPDATE TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: Firmware version ID displayed in step 2 is the current working firmware image, not the "golden" image
    #                 Firmware version ID displayed in step 4 is the current "golden" image
    return True

def testAllCommandsToOBC():
    print("\n---------- OBC SYSTEM-WIDE HOUSEKEEPING TEST ----------\n")
    test.testHousekeeping(1, 1, 1, 0, 0, 0, 0, 0, 0)

    # TODO  - Finish function implementation
    print("\n---------- EPS PING WATCHDOG TEST ----------\n")
    test_EPS_pingWatchdog()

    print("\n---------- GROUND STATION PING WATCHDOG TEST ----------\n")
    test_GS_pingWatchdog()

    # TODO  - Finish function implementation
    print("\n---------- OBC FIRMWARE UPDATE TEST ----------\n")
    test_OBC_firmwareUpdate()

    # TODO  - Finish function implementation
    print("\n---------- OBC GOLDEN FIRMWARE UPDATE TEST ----------\n")
    test_OBC_goldenFirmwareUpdate()

    
    test.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
