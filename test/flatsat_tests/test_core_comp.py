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

import numpy as np
from testLib import testLib as test

test = test() #call to initialize local test class

def testAllCommandsToOBC():
    # OBC System-Wide Housekeeping Test
    # Gather all HK data & save as file
    # Downlink and check if data is within range

    # PASS CONDITION: all HK data is within range


    # EPS Ping Watchdog Test
    # Configure an EPS ping watchdog to check CSP ID 1 every 5 mins and toggle EPS output 6 for 10 seconds if it times out
    # Enable OBC to check UHF operating status every 5 min by verifying the software version. OBC will command EPS to reset power channel 8 for 10 seconds if verification fails
    # Repeat the following every 10 seconds for 6 minutes:
        # Gather all EPS HK info and save to file
        # Save it to PC and display all EPS HK info
    # Disconnect UART connection between UHF and OBC, then repeat steps above
    # Reconnect UART connection between UHF and OBC, then wait 30 seconds
    # Tell OBC to stop respnding to ping requests
    # Repeat HK steps
    # Disable EPS ping watchdog

    # PASS CONDITION: During the first 6 minutes of gather HK data, Output State = 1 for all active pwoer channels at all times
    #                 During the second 6 minutes of gathering HK data, Output State = 1 for all active channels except channel 8, which should be 0


    # Ground Station Ping Watchdog Test
    #


    # OBC Firmware Update



    # OBC Golden Firmware Image



    test.send('eps.time_management.get_eps_time')
    test.sendAndExpect('eps.control.single_output_control(10 1 0)', {'err': 0}) #Preferably a channe that does not power a subsystem
    test.send('eps.cli.general_telemetry')
    test.sendAndExpect('eps.control.single_output_control(10 0 0)', {'err': 0})
    test.sendAndExpect('eps.configuration.get_active_config(0 0)', {'err': 0, 'type':0, 'Value': 4})
    test.sendAndExpect('eps.configuration.get_active_config(136 2)', {'err': 0, 'type':2, 'Value': 500}) #Might change though. Just checking another type
    
    test.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
