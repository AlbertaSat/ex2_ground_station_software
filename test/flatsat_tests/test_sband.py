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
 * @file test_sband.py
 * @author Daniel Sacro
 * @date 2022-3-10
'''
import time
import numpy as np
from testLib import testLib as test

test = test() #call to initialize local test class

# TODO - Automate the remainings steps in the S-Band Downlink Test - 2 & 3
def test_sBandDownlink():
    # 1) Ensure that the OBC, UHF, EPS, and S-Band are turned on, and that the OBC has the most up-to-date firmware (doesn't need to be automated)

    # 2) Gather all system-wide housekeeping information and save it to the OBC SD card
    server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
    response = gs.transaction(server, port, toSend)

    # 3) Downlink the housekeeping information file over the S-Band connection and display all HK info on the ground station CLI

    # PASS CONDITION: Ground station CLI is able to successfully show the data outlined in the pass criteria of the previous test (system-wide HK test)
    return True

# TODO - Automate the remaining steps in the EPS test - 2, 3, 4
def test_EPS_pingWatchdog():
    testPassed = "Pass"
    # 1) Ensure OBC, UHF, EPS, Charon, and S-Band are turned on (Doesn't have to be automated)

    # 2) Ensure that the OBC is operating in such a way that it will respond to ping requests of CSP ID 1

    # 3) Configure an EPS and OBC ping watchdogs to check CSP ID 1 every 5 mins and toggle EPS output 6 for 10 seconds if it times out

    # 4) Enable OBC to check S-Band's operating status every 5 min by verifying the software version. OBC will toggle SBAND ENABLE once for 10 seconds if verification fails

    # TODO "pchannelX" (where X = a num from 1-9) doesn't exist yet. The name is just a placeholder, so replace them with the right HK names
    pchannels = ['pchannel1', 'pchannel2', 'pchannel3', 'pchannel4', 'pchannel5', 'pchannel6', 'pchannel7', 'pchannel8','pchannel9']
    AOcurOutputs = ['AOcurOutput1_mA', 'AOcurOutput2_mA']

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

    # 6) Disconnect UART connection between S-Band and OBC
    input("\nPlease disconnect the UART connection between S-Band and the OBC. Press enter to resume tests.\n") 

    # 7) Repeat step 5:
    for j in range(36): 
        server, port, toSend = gs.getInput('eps.cli.general_telemetry')
        response = gs.transaction(server, port, toSend)

        for val in test.expected_EPS_HK:
            # To pass test, all active power channels have output state = 1, AND 5V0_AO > 5 mA
            colour = '\033[0m' #white
            if val in pchannels:
                if (response[val] == 0):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                else:
                    colour = '\033[92m' #green
            elif val in AOcurOutputs:
                if (response[val] <= 5):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                else:
                    colour = '\033[92m' #green

            print(colour + str(val) + ": " + str(response[val]))
            
        time.sleep(10)

    # 8) Reconnect UART connection between S-Band and OBC
    input("\nPlease Reconnect the UART connection between S-Band and the OBC. Press enter to resume tests.\n")  

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - EPS PING WATCHDOG TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: During step 5, Output State = 1 for all active power channels at all times
    #                 During step 7, Output State = 1 for all active power channels at all times, AND 5V0_AO is > 5mA
    return True

def testAllCommandsToOBC():
    print("\n---------- OBC SYSTEM-WIDE HOUSEKEEPING TEST ----------\n")
    test.testHousekeeping(1, 1, 1, 1, 1, 1, 0, 0, 0)

    # TODO  - Finish function implementation
    print("\n---------- DOWNLINK HOUSEKEEPING OVER S-BAND TEST ----------\n")
    test_sBandDownlink()

    # TODO  - Finish function implementation
    print("\n---------- EPS PING WATCHDOG TEST ----------\n")
    test_EPS_pingWatchdog()

    test.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
