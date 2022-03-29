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
 * @file functionalTestLib.py
 * @author Daniel Sacro
 * @date 2022-03-24
'''

'''This file serves as an extension of testLib.py and contains tests that are to
be used in any of the scripts for the Full and Partial Functional Test Plan'''

import time
import sys
from testLib import testLib as test
from os import path
sys.path.append("./src")
from groundStation import groundStation

import numpy as np

opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())

class functionalTestLib(object):
    def __init__(self):
        self.test = test()
        pass
    
    def testSystemWide_HK(self, aurora = 0, yukon = 0):
        # Aurora HK and Yukon HK cannot be checked at the same time
        if (aurora + yukon < 2):
            self.test.testHousekeeping(1, 1, 1, 1, 1, 1, 1, 1, aurora, yukon, 1)
        else:
            raise ValueError("One of the argument values must be 0.")
        return True

    # NOTE - Cannot be automated. Requires physical involvment with deployables
    def testSystemWideDeployment(self):
        return True

    # TODO - Automate the remaining steps - 1c, 1f, 1h, and all of a-d, g, and i for steps 4-6
    def run_ADCS_healthCheck(self):
        testPassed = "Pass"
        # 1) Perform the control computer health check
        # 1a) Ensure that the OBC is turned on and has the most up-to-date firmware installed (Note this version down somewhere)

        # 1b) Power on the CubeADCS and wait one second for everything to power on
        input("Please power on the CubeADCS. Press enter to continue.")
        time.sleep(1)

        # 1c) Verify results in Table 2 from the Full and Partial Functional Test Plan
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_bootloader_state")
        response = gs.transaction(server, port, toSend)
        startTime = response['Uptime']
        time.sleep(1)
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_bootloader_state")
        response = gs.transaction(server, port, toSend)
        endTime = response['Uptime']
        # To pass test, uptime should increment every second
        timeDiff = endTime - startTime
        if  (timeDiff < 0 or timeDiff > 2):
            testPassed = "Fail"

        flags = response['Flags_arr']
        flagsArray = str(bin(flags))[2:]
        flagIndex = 0
        # Flags ordered as: sram1, sram2, sram_latch_not_recovered, sram_latch_recovered, sd card error, external_flash_err,
        # internal_flash_err, eeprom_err, bat_boot_reg, comms_radio_err
        expectedFlags = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        for flag in flagsArray:
            if (int(flag) != expectedFlags[flagIndex]):
                testPassed = "Fail"
            flagIndex += 1

        server, port, toSend = gs.getInput("obc.adcs.adcs_get_boot_program_stat")
        response = gs.transaction(server, port, toSend)

        # To pass test, Cause of Reset must be "PowerOnReset" (0) or "SystemReqReset" (8)
        if not (response['Mcu_Reset_Cause'] == 0 or response['Mcu_Reset_Cause'] == 8):
            testPassed = "Fail"

        # To pass test, Boot count must increment
        if (response['Boot_Count'] > 0):
            testPassed = "Fail"

        # To pass test, Boot Cause must be "Unexpected" (0), Boot Program Index must be "RunBootLoader" (2), Firmware version (Major) is 3, and Firmware Version (Minor) is 1
        if (response['Boot_Cause'] != 0 or response['Boot_Idx'] != 2): # TODO - Add in check for Firmware Versions
            testPassed = "Fail"

        server, port, toSend = gs.getInput("obc.adcs.adcs_get_boot_index")
        response = gs.transaction(server, port, toSend)

        # To pass test, Program Index must be "RunInternalFlashProgram" (1)
        if (response['Program_Idx'] != 1):
            testPassed = "Fail"

        # To pass test, Boot Status must be "BootSuccess" (1) or "BootNew" (0)
        if not (response['Boot_Stat'] == 1 or response['Boot_Stat'] == 0):
            testPassed = "Fail"

        server, port, toSend = gs.getInput("obc.adcs.adcs_get_comms_stat")
        response = gs.transaction(server, port, toSend)

        # Comms_Status is uint16 containing information that must be split into 2 uint8 variables
        commsStatus = response['Comms_Status']
        commsStatusArray = str(bin(flags))[2:]
        telecommandCounter = int(commsStatusArray[0:8], 2) # convert uint8 into dec
        telemetryRequestCounter = int(commsStatusArray[8:16], 2) # convert uint8 into dec

        # To pass test, Telecommand Counter should be 0, Telemetry request counter should "increment after every refresh", All remaining communication flags are 0
        # TODO - Add in check for flags. ADCS_get_comms_stat() currently does not return any communication flags at the time of last edit (returns >u2 which is uint16
        # and does not contain any space for flags since both counters are uint8)
        if not (telecommandCounter == 0 and telemetryRequestCounter > 0):
            testPassed = "Fail"
        oldTelemetryRequestCounter = telemetryRequestCounter

        # 1d & 1e) Power off the CubeADCS, and then turn it back on again. Wait at least 5 seconds for everything to power on and the ACP to start
        input("Please power the CubeADCS off and then back on. Press enter to continue.")
        time.sleep(5)

        # 1f) Verify results in Table 3 from the Full and Partial Functional Test Plan
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_acp_loop_stat")
        response = gs.transaction(server, port, toSend)

        # To pass test, time since iteration start should be between 0 and 1000 ms
        if (response['Time'] < 0 or response['Time'] > 1000):
            testPassed = "Fail"

        # To pass test, current execution point should be Idle (1)
        if (response['Execution_point'] != 1):
            testPassed = "Fail"
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_boot_program_stat")
        response = gs.transaction(server, port, toSend)

        # To pass test, Cause of Reset must be "PowerOnReset" (0) or "SystemReqReset" (8), or "Unknown" (15)
        if not (response['Mcu_Reset_Cause'] == 0 or response['Mcu_Reset_Cause'] == 8 or response['Mcu_Reset_Cause'] == 15):
            testPassed = "Fail"

        # To pass test, Boot count must increment
        if (response['Boot_Count'] > 0):
            testPassed = "Fail"

        # To pass test, Boot Cause must be "Unexpected" (0), Boot Program Index must be "RunInternalFlashProgram" (1), Firmware version (Major) is 7,
        # and Firmware Version (Minor) is between 1 and 255
        if (response['Boot_Cause'] != 0 or response['Boot_Idx'] != 1): # TODO - Add in check for Firmware Versions
            testPassed = "Fail"

        server, port, toSend = gs.getInput("obc.adcs.adcs_get_node_identification")
        response = gs.transaction(server, port, toSend)

        # To pass test, Node Type must be 10, Interface Version must be 7, and Runtime should be between 0 and 1000 ms
        if (response['Node_Type'] != 10 or response['Interface_Ver'] != 7 or response['Runtime_Ms'] < 0 or response['Runtime_Ms'] > 1000):
            testPassed = "Fail"

        server, port, toSend = gs.getInput("obc.adcs.adcs_get_boot_index")
        response = gs.transaction(server, port, toSend)

        # To pass test, Program Index must be "RunInternalFlashProgram" (1) and Boot Status must be "BootSuccess" (1)
        if (response['Program_Idx'] != 1 or response['Boot_Stat'] != 1):
            testPassed = "Fail"

        server, port, toSend = gs.getInput("obc.adcs.adcs_get_comms_stat")
        response = gs.transaction(server, port, toSend)

        # Comms_Status is uint16 containing information that must be split into 2 uint8 variables
        commsStatus = response['Comms_Status']
        commsStatusArray = str(bin(flags))[2:]
        telecommandCounter = int(commsStatusArray[0:8], 2) # convert uint8 into dec
        telemetryRequestCounter = int(commsStatusArray[8:16], 2) # convert uint8 into dec

        # To pass test, Telecommand Counter should be 0, Telemetry request counter should "increment after every refresh", All remaining communication flags are 0
        # TODO - Add in check for flags. ADCS_get_comms_stat() currently does not return any communication flags at the time of last edit (returns >u2 which is uint16
        # and does not contain any space for flags since both counters are uint8)
        if not (telecommandCounter == 0 and telemetryRequestCounter > oldTelemetryRequestCounter):
            testPassed = "Fail"
        # oldTelemetryRequestCounter = telemetryRequestCounter # May or may not be needed for other steps in the test
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_unix_t")
        response = gs.transaction(server, port, toSend)
        startTime = response["Unix_t"]
        time.sleep(2)
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_unix_t")
        response = gs.transaction(server, port, toSend)
        endTime = response['Unix_t']

        # To pass test, time should be incrementing
        if (endTime - startTime <= 0):
            testPassed = "Fail"

        server, port, toSend = gs.getInput("obc.adcs.adcs_get_sram_latchup_count")
        response = gs.transaction(server, port, toSend)

        # To pass test, the number of SRAM latchups for both 1 and 2 should be 0
        if (response['Sram1'] != 0 or response['Sram2'] != 0):
            testPassed = "Fail"

        server, port, toSend = gs.getInput("obc.adcs.adcs_get_edac_err_count")
        response = gs.transaction(server, port, toSend)
        
        # To pass test, Single, Double, and Multi SRAM should be 0
        if (response['Single_Sram'] != 0 or response['Double_Sram'] != 0 or response['Multi_Sram'] != 0):
            testPassed = "Fail"
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_power_control")
        response = gs.transaction(server, port, toSend)

        # To pass test, all nodes indicate "PowOff" (0)
        if (response['Control'] != 0):
            testPassed = "Fail"

        # TODO - Add a check for these values. The "adcs_get_current_state" GS command does not exist yet at the time of last edit
        # server, port, toSend = gs.getInput("obc.adcs.adcs_get_current_state")
        # response = gs.transaction(server, port, toSend)
        # To pass test, Attitude Estimation Mode should be "EstNone", Control Mode should be "ConNone", ADCS Run Mode should be "AdcsOff"
        # and all other states should be "No" (0)

        # 1g) Use the command "ADCS_set_enabled_state(1)" to swtich the run mode to "AdcsEnabled"
        server, port, toSend = gs.getInput("obc.adcs.adcs_set_enabled_state(1)")
        response = gs.transaction(server, port, toSend)

        # 1h) Verify results in Table 4 from the Full and Partial Functional Test Plan
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_comms_stat")
        response = gs.transaction(server, port, toSend)

        # Comms_Status is uint16 containing information that must be split into 2 uint8 variables
        commsStatus = response['Comms_Status']
        commsStatusArray = str(bin(flags))[2:]
        telecommandCounter = int(commsStatusArray[0:8], 2) # convert uint8 into dec

        # To pass test, Telecommand Counter should be equal to 1
        if telecommandCounter != 1:
            testPassed = "Fail"

        server, port, toSend = gs.getInput("obc.adcs.adcs_get_execution_times")
        response = gs.transaction(server, port, toSend)

        # To pass test, Time to Perform ADCS Update is between 80-130 ms, Time to Perform Sensor/Act Communication is between 0-6 ms, Time to execute
        # SGP4 Propagator is between 36-56 ms, and Time to Execute IGRF Model is between 40-60 ms
        if (response['Adcs_Update' < 80] or response['Adcs_Update'] > 130):
            testPassed = "Fail"
        
        if (response['Sensor_Comm' < 0] or response['Sensor_Comm'] > 6):
            testPassed = "Fail"

        if (response['Sgp4_propag' < 36] or response['Sgp4_propag'] > 56):
            testPassed = "Fail"

        if (response['Igrf_model' < 40] or response['Igrf_model'] > 60):
            testPassed = "Fail"
        
        # TODO - Add a check for these values. The "adcs_get_current_state" GS command does not exist yet at the time of last edit
        # server, port, toSend = gs.getInput("obc.adcs.adcs_get_current_state")
        # response = gs.transaction(server, port, toSend)
        # To pass test, Attitude Estimation Mode should be "EstNone", Control Mode should be "ConNone", ADCS Run Mode should be "AdcsEnabled",
        # Sun is Above Local Horizon should be "Yes" (1), and all other states should be "No" (0)

        # 2) As part of CubeSense 1 and 2 health checks, perform a health check on the sun and nadir cameras
        # NOTE - Step 2 of the ADCS health check cannot be automated since it requires human involvement via shining a light at a camera at 
        # varying distances. Additionally, it also requires a person to cover a camera with a cap, and then take that cap off in a later step

        # 3) As part of the CubeControl health check, perform a health check on the coarse sun sensor
        # NOTE - Step 3 of the ADCS health check cannot be automated since it requries human involvement via exposing coarse sun sensors to
        # a bright light, one by one

        # 4) Perform the reaction wheels health check for CubeWheel1
        # 4a) Using command ADCS_get_power_control(), ensure that all nodes are selected as "PowOff" (0)
        server, port, toSend = gs.getInput("obc.adcs.get_power_control")
        response = gs.transaction(server, port, toSend)
        if response['Control'] != 0:
            server, port, toSend = gs.getInput("obc.adcs.set_power_control(0)")
            response = gs.transaction(server, port, toSend)
        # NOTE - Unsure if this turns everything off or turns off a specific ADCS component

        # 4b) Using command ADCS_set_power_control(), switch on CubeWheel1Power Power Selection by selecting "PowOn" (1)
        # TODO - Add in the GS command call for this procedure. According to the ADCS equipment handler at the time of last edit, the command
        # only works for CubeSense1

        # 4c) Verify Results in Table 8
        # TODO - Add a check for these values. The "adcs_get_current_state" GS command does not exist yet at the time of last edit
        # server, port, toSend = gs.getInput("obc.adcs.adcs_get_current_state")
        # response = gs.transaction(server, port, toSend)
        # To pass test, Attitude Estimation Mode should be "EstNone", Control Mode should be "ConNone", ADCS Run Mode should be "AdcsEnabled",
        # CubeWheel1 Enabled should be "Yes" (1), and all other states should be "No" (0)

        # 4d) Using command ADCS_set_wheel_speed(), Set the commanded X speed to 4000 rpm 
        # TODO - Implement this GS command call. Currently does not yet exist at the time of last edit

        # 4e) After 10 seconds, the wheel will settle to the commanded speed. Listen to the wheel to ensure that the correct on is spinning
        time.sleep(10)

        # 4f) Verify results in Table 9
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_measurements")
        response = gs.transaction(server, port, toSend)

        # To pass test, X Wheel Speed should be between 3995-4005 rpm, and Y and Z Wheel Speed should be 0 rpm
        if (response['Wheel_Speed_X' < 3995] or response['Wheel_Speed_X'] > 4005):
            testPassed = "Fail"

        if (response['Wheel_Speed_Y'] != 0 or response['Wheel_Speed_Z'] != 0):
            testPassed = "Fail"
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_power_temp")
        response = gs.transaction(server, port, toSend)

        # To pass test, Wheel1Current should be between 9-17 mA, and Wheel2Current and Wheel3Current should be 0 mA
        if (response['wheel1_I' < 9] or response['wheel1_I'] > 17):
            testPassed = "Fail"

        if (response['wheel2_I'] != 0 or response['wheel3_I'] != 0):
            testPassed = "Fail"

        # 4g) Using command ADCS_set_wheel_speed(), set the commanded X speed to -2000 rpm
        # TODO - Implement this GS command call. Currently does not yet exist at the time of last edit

        # 4h) After 10 seconds, verify table 10
        time.sleep(10)
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_measurements")
        response = gs.transaction(server, port, toSend)

        # To pass test, X Wheel Speed should be between -2005 and -1995 rpm, and Y and Z Wheel Speed should be 0 rpm
        if (response['Wheel_Speed_X' < -2005] or response['Wheel_Speed_X'] > -1995):
            testPassed = "Fail"

        if (response['Wheel_Speed_Y'] != 0 or response['Wheel_Speed_Z'] != 0):
            testPassed = "Fail"
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_power_temp")
        response = gs.transaction(server, port, toSend)

        # To pass test, Wheel1Current should be between 4-10 mA, and Wheel2Current and Wheel3Current should be 0 mA
        if (response['wheel1_I' < 4] or response['wheel1_I'] > 10):
            testPassed = "Fail"

        if (response['wheel2_I'] != 0 or response['wheel3_I'] != 0):
            testPassed = "Fail"
        
        # 4i) Using command ADCS_set_wheel_speed, set the command X speed to 0 rpm
        # TODO - Implement this GS command call. Currently does not yet exist at the time of last edit

        # 4j) After 10 seconds, verify table 11
        time.sleep(10)
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_measurements")
        response = gs.transaction(server, port, toSend)

        # To pass test, X, Y and Z Wheel Speed should be 0 rpm
        if (response['Wheel_Speed_X'] != 0 or response['Wheel_Speed_Y'] != 0 or response['Wheel_Speed_Z'] != 0):
            testPassed = "Fail"
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_power_temp")
        response = gs.transaction(server, port, toSend)

        # To pass test, Wheel1Current should be between 1-7 mA, and Wheel2Current and Wheel3Current should be 0 mA
        if (response['wheel1_I' < 1] or response['wheel1_I'] > 7):
            testPassed = "Fail"

        if (response['wheel2_I'] != 0 or response['wheel3_I'] != 0):
            testPassed = "Fail"

        # 4k) Using command ADCS_set_power_control(), switch off CubeWheel1Power Power Selection by selecting "PowOff" (0)
        server, port, toSend = gs.getInput("obc.adcs.set_power_control(0)")
        response = gs.transaction(server, port, toSend)
        # NOTE - Unsure if this turns everything off or turns off a specific ADCS component

        # 5) Perform the reaction wheels health check for CubeWheel2
        # 5a & b) Repeat steps 4a-4k for CubeWheel2, setting the commanded Y speed instead of the X speed, and using tables 12-15

        #Using command ADCS_get_power_control(), ensure that all nodes are selected as "PowOff" (0)
        server, port, toSend = gs.getInput("obc.adcs.get_power_control")
        response = gs.transaction(server, port, toSend)
        if response['Control'] != 0:
            server, port, toSend = gs.getInput("obc.adcs.set_power_control(0)")
            response = gs.transaction(server, port, toSend)
        # NOTE - Unsure if this turns everything off or turns off a specific ADCS component

        # Using command ADCS_set_power_control(), switch on CubeWheel2Power Power Selection by selecting "PowOn" (1)
        # TODO - Add in the GS command call for this procedure. According to the ADCS equipment handler at the time of last edit, the command
        # only works for CubeSense1

        # Verify Results in Table 12
        # TODO - Add a check for these values. The "adcs_get_current_state" GS command does not exist yet at the time of last edit
        # server, port, toSend = gs.getInput("obc.adcs.adcs_get_current_state")
        # response = gs.transaction(server, port, toSend)
        # To pass test, Attitude Estimation Mode should be "EstNone", Control Mode should be "ConNone", ADCS Run Mode should be "AdcsEnabled",
        # CubeWheel2 Enabled should be "Yes" (1), and all other states should be "No" (0)

        # Using command ADCS_set_wheel_speed(), Set the commanded Y speed to 4000 rpm 
        # TODO - Implement this GS command call. Currently does not yet exist at the time of last edit

        # After 10 seconds, the wheel will settle to the commanded speed. Listen to the wheel to ensure that the correct on is spinning
        time.sleep(10)

        # Verify results in Table 13
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_measurements")
        response = gs.transaction(server, port, toSend)

        # To pass test, Y Wheel Speed should be between 3995-4005 rpm, and X and Z Wheel Speed should be 0 rpm
        if (response['Wheel_Speed_Y' < 3995] or response['Wheel_Speed_Y'] > 4005):
            testPassed = "Fail"

        if (response['Wheel_Speed_X'] != 0 or response['Wheel_Speed_Z'] != 0):
            testPassed = "Fail"
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_power_temp")
        response = gs.transaction(server, port, toSend)

        # To pass test, Wheel2Current should be between 9-17 mA, and Wheel1Current and Wheel3Current should be 0 mA
        if (response['wheel2_I' < 9] or response['wheel2_I'] > 17):
            testPassed = "Fail"

        if (response['wheel1_I'] != 0 or response['wheel3_I'] != 0):
            testPassed = "Fail"

        # Using command ADCS_set_wheel_speed(), set the commanded Y speed to -2000 rpm
        # TODO - Implement this GS command call. Currently does not yet exist at the time of last edit

        # After 10 seconds, verify table 14
        time.sleep(10)
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_measurements")
        response = gs.transaction(server, port, toSend)

        # To pass test, Y Wheel Speed should be between -2005 and -1995 rpm, and X and Z Wheel Speed should be 0 rpm
        if (response['Wheel_Speed_Y' < -2005] or response['Wheel_Speed_Y'] > -1995):
            testPassed = "Fail"

        if (response['Wheel_Speed_X'] != 0 or response['Wheel_Speed_Z'] != 0):
            testPassed = "Fail"
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_power_temp")
        response = gs.transaction(server, port, toSend)

        # To pass test, Wheel2Current should be between 4-10 mA, and Wheel1Current and Wheel3Current should be 0 mA
        if (response['wheel2_I' < 4] or response['wheel2_I'] > 10):
            testPassed = "Fail"

        if (response['wheel1_I'] != 0 or response['wheel3_I'] != 0):
            testPassed = "Fail"
        
        # Using command ADCS_set_wheel_speed, set the command X speed to 0 rpm
        # TODO - Implement this GS command call. Currently does not yet exist at the time of last edit

        # After 10 seconds, verify table 15
        time.sleep(10)
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_measurements")
        response = gs.transaction(server, port, toSend)

        # To pass test, X, Y and Z Wheel Speed should be 0 rpm
        if (response['Wheel_Speed_X'] != 0 or response['Wheel_Speed_Y'] != 0 or response['Wheel_Speed_Z'] != 0):
            testPassed = "Fail"
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_power_temp")
        response = gs.transaction(server, port, toSend)

        # To pass test, Wheel2Current should be between 1-7 mA, and Wheel1Current and Wheel3Current should be 0 mA
        if (response['wheel2_I' < 1] or response['wheel2_I'] > 7):
            testPassed = "Fail"

        if (response['wheel1_I'] != 0 or response['wheel3_I'] != 0):
            testPassed = "Fail"

        # Using command ADCS_set_power_control(), switch off CubeWheel1Power Power Selection by selecting "PowOff" (0)
        server, port, toSend = gs.getInput("obc.adcs.set_power_control(0)")
        response = gs.transaction(server, port, toSend)
        # NOTE - Unsure if this turns everything off or turns off a specific ADCS component

        # 6) Perform the reaction wheels health check for CubeWheel3
        # 6a & b) Repeat steps 4a-4k for CubeWheel3, setting the commanded Z speed instead of the X speed, and using tables 16-19
        
        # Using command ADCS_get_power_control(), ensure that all nodes are selected as "PowOff" (0)
        server, port, toSend = gs.getInput("obc.adcs.get_power_control")
        response = gs.transaction(server, port, toSend)
        if response['Control'] != 0:
            server, port, toSend = gs.getInput("obc.adcs.set_power_control(0)")
            response = gs.transaction(server, port, toSend)
        # NOTE - Unsure if this turns everything off or turns off a specific ADCS component

        # Using command ADCS_set_power_control(), switch on CubeWheel3Power Power Selection by selecting "PowOn" (1)
        # TODO - Add in the GS command call for this procedure. According to the ADCS equipment handler at the time of last edit, the command
        # only works for CubeSense1

        # Verify Results in Table 16
        # TODO - Add a check for these values. The "adcs_get_current_state" GS command does not exist yet at the time of last edit
        # server, port, toSend = gs.getInput("obc.adcs.adcs_get_current_state")
        # response = gs.transaction(server, port, toSend)
        # To pass test, Attitude Estimation Mode should be "EstNone", Control Mode should be "ConNone", ADCS Run Mode should be "AdcsEnabled",
        # CubeWheel3 Enabled should be "Yes" (1), and all other states should be "No" (0)

        # Using command ADCS_set_wheel_speed(), Set the commanded Z speed to 4000 rpm 
        # TODO - Implement this GS command call. Currently does not yet exist at the time of last edit

        # After 10 seconds, the wheel will settle to the commanded speed. Listen to the wheel to ensure that the correct on is spinning
        time.sleep(10)

        # Verify results in Table 17
        # NOTE - There seems to be a typo in the document. Table 17 is completely the same as table 16. It is assumed that the table should
        # look similar to table 13, but with checks for Z Wheel Speed and Wheel3Current instead
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_measurements")
        response = gs.transaction(server, port, toSend)

        # To pass test, Z Wheel Speed should be between 3995-4005 rpm, and X and Y Wheel Speed should be 0 rpm
        if (response['Wheel_Speed_Z' < 3995] or response['Wheel_Speed_Z'] > 4005):
            testPassed = "Fail"

        if (response['Wheel_Speed_X'] != 0 or response['Wheel_Speed_Y'] != 0):
            testPassed = "Fail"
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_power_temp")
        response = gs.transaction(server, port, toSend)

        # To pass test, Wheel3Current should be between 9-17 mA, and Wheel1Current and Wheel2Current should be 0 mA
        if (response['wheel3_I' < 9] or response['wheel3_I'] > 17):
            testPassed = "Fail"

        if (response['wheel1_I'] != 0 or response['wheel2_I'] != 0):
            testPassed = "Fail"

        # Using command ADCS_set_wheel_speed(), set the commanded Z speed to -2000 rpm
        # TODO - Implement this GS command call. Currently does not yet exist at the time of last edit

        # After 10 seconds, verify table 18
        time.sleep(10)
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_measurements")
        response = gs.transaction(server, port, toSend)

        # To pass test, Z Wheel Speed should be between -2005 and -1995 rpm, and X and Y Wheel Speed should be 0 rpm
        if (response['Wheel_Speed_Z' < -2005] or response['Wheel_Speed_Z'] > -1995):
            testPassed = "Fail"

        if (response['Wheel_Speed_X'] != 0 or response['Wheel_Speed_Y'] != 0):
            testPassed = "Fail"
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_power_temp")
        response = gs.transaction(server, port, toSend)

        # To pass test, Wheel3Current should be between 4-10 mA, and Wheel1Current and Wheel2Current should be 0 mA
        if (response['wheel3_I' < 4] or response['wheel3_I'] > 10):
            testPassed = "Fail"

        if (response['wheel1_I'] != 0 or response['wheel2_I'] != 0):
            testPassed = "Fail"
        
        # Using command ADCS_set_wheel_speed, set the command Z speed to 0 rpm
        # TODO - Implement this GS command call. Currently does not yet exist at the time of last edit

        # After 10 seconds, verify table 19
        time.sleep(10)
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_measurements")
        response = gs.transaction(server, port, toSend)

        # To pass test, X, Y and Z Wheel Speed should be 0 rpm
        if (response['Wheel_Speed_X'] != 0 or response['Wheel_Speed_Y'] != 0 or response['Wheel_Speed_Z'] != 0):
            testPassed = "Fail"
        
        server, port, toSend = gs.getInput("obc.adcs.adcs_get_power_temp")
        response = gs.transaction(server, port, toSend)

        # To pass test, Wheel3Current should be between 1-7 mA, and Wheel1Current and Wheel2Current should be 0 mA
        if (response['wheel3_I' < 1] or response['wheel3_I'] > 7):
            testPassed = "Fail"

        if (response['wheel1_I'] != 0 or response['wheel2_I'] != 0):
            testPassed = "Fail"

        # Using command ADCS_set_power_control(), switch off CubeWheel1Power Power Selection by selecting "PowOff" (0)
        server, port, toSend = gs.getInput("obc.adcs.set_power_control(0)")
        response = gs.transaction(server, port, toSend)
        # NOTE - Unsure if this turns everything off or turns off a specific ADCS component

        # Take note of the test results
        if (testPassed == "Pass"):
            colour = '\033[92m' #green
            test.passed += 1
        else:
            colour = '\033[91m' #red
            test.failed += 1

        print(colour + ' - ADCS HEALTH CHECK TEST ' + testPassed + '\n\n' + '\033[0m')

        # PASS CONDITION: -> Tests return expected responses as defined by tables 2-19
        
        return True

    # TODO - Automate the remaining steps in the Clock Synchronization test - 1, 3
    def testClockSynchronization(self):
        testPassed = "Pass"
        # 1) Send a command over UHF to tell the OBC to synchronize all onboard clocks with the ground station's time

        # 2) Send a command to calculate the difference between the OBC time and the EPS and ADCS time
        server, port, toSend = gs.getInput('obc.time_management.get_time')
        response = gs.transaction(server, port, toSend)
        OBC_time = response['timestamp']
        server, port, toSend = gs.getInput('eps.time_management.get_eps_time')
        response = gs.transaction(server, port, toSend)
        EPS_time = response['timestamp']
        # To pass test, the difference between the timestamps should be < 2 seconds
        if (abs(OBC_time - EPS_time) >= 2):
            testPassed = "Fail"

        # 3) Send a command directly over the OBC debug UART to fetch the OBC time in ms and calculate the difference with an accurate source on a PC using chrony
        # To pass test, the difference between the OBC time and stratum-0 time should be < 0.1 seconds

        # Take note of the test results
        if (testPassed == "Pass"):
            colour = '\033[92m' #green
            test.passed += 1
        else:
            colour = '\033[91m' #red
            test.failed += 1

        print(colour + ' - CLOCK SYNCHRONIZATION USING GROUND STATION TEST ' + testPassed + '\n\n' + '\033[0m')

        # PASS CONDITION: -> The maximum difference between OBC time and EPS or ADCS time is < 2 seconds
        #                 -> The maximum difference between OBC time and stratum-0 time is < 0.1 seconds
            
        return True

    # TODO - Automate the remaining steps in the Charon Power Channel Forced Reset test - 2-4
    def testCharonPowerChannelForcedResets(self):
        testPassed = "Pass"

        # 1) Send a command to gather and downlink system-wide HK and display it on the terminal
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0, 0)')
        response = gs.transaction(server, port, toSend)
        for val in response:
            print(str(val) + ": " + str(response[val]))

        # 2) Send a command to force a reset of power channel 1

        # 3) After 10 seconds, repeat step 1
        time.sleep(10)
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
        response = gs.transaction(server, port, toSend)
        for val in response:
            print(str(val) + ": " + str(response[val]))

        # 4) Repeat steps 2 and 3, NINE more times: once each for power channels 2-10 instead of channel 1

        # To pass test, the number of power channel resets for each channel is one higher than the last time

        # Take note of the test results
        if (testPassed == "Pass"):
            colour = '\033[92m' #green
            test.passed += 1
        else:
            colour = '\033[91m' #red
            test.failed += 1

        print(colour + ' - CHARON POWER CHANNEL FORCED RESETS TEST ' + testPassed + '\n\n' + '\033[0m')

        # PASS CONDITION: -> The number of power channel resets for each channel after the reset command is executed must be one more than before the command is executed
        return True

    # TODO - Automate the remaining steps in the Deployables Switch Status test - 2
    def checkDeployablesSwitchStatus(self):
        testPassed = "Pass"
        # 1) Ensure that all deployables are stowed
        input("Please ensure that all deployables are stowed. Press enter to continue.")

        # 2) Send a command for the OBC to read the switch states of all deployment switches
        # To pass test, all switch states must be in a stowed state

        # Take note of the test results
        if (testPassed == "Pass"):
            colour = '\033[92m' #green
            test.passed += 1
        else:
            colour = '\033[91m' #red
            test.failed += 1

        print(colour + ' - DEPLOYABLES SWITCH STATUS TEST ' + testPassed + '\n\n' + '\033[0m')

        # PASS CONDITION: -> All switch states read from step 2 are indicate being in a stowed state
        return True

    # TODO - Automate the remaining steps in the S-Band Send Data at Full Rate over Radio Channel test - 1-3
    def testSBandFullDataRateOverRadio(self):
        # 1) Send a command for the OBC to randomly generate and save in a file 1.25 megabyte packets for 1 minute

        # 2) Store the data generated from step 1 into a file on the OBC

        # 3) Transmit the file from the OBC to the ground station via the S-Band Transmitter

        # PASS CONDITION: -> The packets in the file received are verified to be identical to the packets transmitted
        #                 -> The payload data downlink rate is 10 Mbps 
        return True
    
    # TODO - Automate the remaining steps in the UHF Tx and Rx Over Radio Test - 2-4
    def test_UHF_Tx_Rx_overRadio(self):
        # Use pipe.set_pipe.uhf_gs_pipe
        # 1) Place the flight model assembly of the satellite into a clean box (Doesn't have to be automated)

        # 2) Put the transceiver into transparent (PIPE) mode using a radio command, and continuously send randomly generated 128 byte packets
        # from the ground for 1 minute
        server, port, toSend = gs.getInput('obc.set_pipe.uhf_gs_pipe')
        response = gs.transaction(server, port, toSend)        

        # 3) Store the data generated from step 2 into a file on the OBC

        # 4) Without letting PIPE mode time out, send the file back from the satellite to the GS
        # To pass test, the file sent back from the satellite must be the same as the file originally sent by the GS

        # PASS CONDITION: -> The packets in the file received are verified via code to be identical to the packets transmitted
        return True

    # TODO - Automate the remaining steps in the DFGM Data Output Test - 3, 4
    def check_DFGM_dataOutput(self):
        testPassed = "Pass"
        # 1) Ensure that the OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware

        # 2) Send a command over UHF to turn on the DFGM for 10 seconds and have the OBC process the data output
        # into 1 Hz, 10 Hz, and 100 Hz data. Also store this data into a file on the SD card
        server, port, toSend = gs.getInput('obc.dfgm.dfgm_run(10)')
        response = gs.transaction(server, port, toSend)

        # 3) Send a command over UHF for the OBC to downlink a 1 Hz DFGM data file over UHF and save it on the PC

        # 4) Repeat step 3 for 10 Hz and 100 Hz DFGM data

        # Take note of the test results
        if (testPassed == "Pass"):
            colour = '\033[92m' #green
            test.passed += 1
        else:
            colour = '\033[91m' #red
            test.failed += 1

        print(colour + ' - DFGM DATA OUTPUT TEST ' + testPassed + '\n\n' + '\033[0m')

        # PASS CONDITION: -> The data packet should be visible on the GS computer and able to open and read within 5
        #                    5 seconds of downlink
        #                 -> The packet should not be empty, and should contain data corresponding to an approximate
        #                    magnetic field reading of the immediate area
        #                 -> Each frequency of DFGM data type should correspond to the correct data file 
        return True

    # TODO - Add in the correct power output channel variable names to the pchannels and pchannelsToCheck list
    def test_EPS_powerChannelResets(self):
        testPassed = "Pass"
        # TODO "pchannelX" (where X = a num from 1-10) doesn't exist yet. The name is just a placeholder, so replace them with the right HK names
        pchannels = ['pchannel1', 'pchannel2', 'pchannel3', 'pchannel4', 'pchannel5', 'pchannel6', 'pchannel7', 'pchannel8','pchannel9', 'pchannel10']
        # 1) Ensure that the OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware installed

        # 2) Send a command from the OBC to the EPS to set all EPS output states 
        server, port, toSend = gs.getInput('eps.control.all_output_control(1023)') # 1023 = 0b1111111111
        response = gs.transaction(server, port, toSend)
        
        # 3) Send a command from the OBC to the EPS to retrieve HK data and print it on the terminal display
        # To pass test, all output states should be on (= 1)
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0, 0)')
        response = gs.transaction(server, port, toSend)
        for val in response:
            colour = '\033[0m' #white
            if val in pchannels:
                if (response[val] == 0):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                else:
                    colour = '\033[92m' #green
            print(colour + str(val) + ": " + str(response[val]))

        channels = [1, 2, 3, 4, 5, 7, 8, 9, 10] # Excludes channel 6
        pchannelsToCheck = ['pchannel1', 'pchannel2', 'pchannel3', 'pchannel4', 'pchannel5', 'pchannel7', 'pchannel8','pchannel9', 'pchannel10']
        pChannelIndex = 0
        for channelToReset in channels:
            # 4) Send a command from the OBC to the EPS to turn all output states off individually excluding output 6
            for channel in channels:
                command = 'eps.control.single_output_control(' + str(channel) + ', 0, 0)'
                server, port, toSend = gs.getInput(command)
                response = gs.transaction(server, port, toSend)

            # 5) Send a command from the OBC to the EPS to set EPS output 1 to on
            command = 'eps.control.single_output_control(' + str(channelToReset) + ', 1, 0)'
            server, port, toSend = gs.getInput(command)
            response = gs.transaction(server, port, toSend)

            # 6) Send a command from the OBC to the EPS to retrieve HK data and print it to the terminal display
            # To pass test, the channel switched on should actually be on (1)
            server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0, 0)')
            response = gs.transaction(server, port, toSend)
            for val in response:
                colour = '\033[0m' #white
                if (val == pchannelsToCheck[pChannelIndex]):
                    if (response[val] != 1):
                        testPassed = "Fail"
                        colour = '\033[91m' #red
                    else:
                        colour = '\033[92m' #green
                print(colour + str(val) + ": " + str(response[val]))

            # 7) Send a command from the OBC to the EPS to set EPS output 1 to off
            command = 'eps.control.single_output_control(' + str(channelToReset) + ', 0, 0)'
            server, port, toSend = gs.getInput(command)
            response = gs.transaction(server, port, toSend)

            # 8) Send a command from the OBC to the EPS to retrieve HK data and print it to the terminal display
            # To pass test, the channel switched off should actually be off (0)
            server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0, 0)')
            response = gs.transaction(server, port, toSend)
            for val in response:
                colour = '\033[0m' #white
                if (val == pchannelsToCheck[pChannelIndex]):
                    if (response[val] != 0):
                        testPassed = "Fail"
                        colour = '\033[91m' #red
                    else:
                        colour = '\033[92m' #green
                print(colour + str(val) + ": " + str(response[val]))

            # 9) Repeat steps 4-7 for EPS outputs 2 to 10, excluding output 6
            pChannelIndex += 1

        # 10) Send a command from the OBC to the EPS to set all EPS output states off, excluding output 6
        # NOTE - the channels list already excludes channel 6
        for channel in channels:
                command = 'eps.control.single_output_control(' + str(channel) + ', 0, 0)'
                server, port, toSend = gs.getInput(command)
                response = gs.transaction(server, port, toSend)

        # 11) Send a command from the OBC to the EPS to retrieve HK data and print it to the terminal display
        # To pass test, all channels should be off (0), except channel 6
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0, 0)')
        response = gs.transaction(server, port, toSend)
        for val in response:
            colour = '\033[0m' #white
            if val in pchannels:
                if (response[val] == 1):
                    testPassed = "Fail"
                    colour = '\033[91m' #red
                else:
                    colour = '\033[92m' #green
            print(colour + str(val) + ": " + str(response[val]))

        # Take note of the test results
        if (testPassed == "Pass"):
            colour = '\033[92m' #green
            test.passed += 1
        else:
            colour = '\033[91m' #red
            test.failed += 1

        print(colour + ' - EPS POWER CHANNEL RESET TEST ' + testPassed + '\n\n' + '\033[0m')

        # PASS CONDITION: -> All output states are as expected in steps 3, 6, 8, 11
        return True

    # NOTE - Cannot be automated. Requires manually measuring voltages/currents with a digital multimeter
    def test_EPS_andSolarPanelCharging(self):
        return True

    # NOTE - Cannot be automated. Requires physical involvement with deployment footswitches and a stopwatch
    def test_EPS_deploymentTimer(self):
        return True

    # TODO - Automate the remaining steps in the OBC RTC Backup Power Circuit Test - 3, 4
    def test_OBC_RTC_backupPowerCircuit(self):
        testPassed = "Pass"
        # 1) Ensure that the OBC, UHF, EPS, and Charon are turned on, and that the OBC has the msot up-to-date firmware installed

        # 2) Downlink all HK data, and verify that the time and date are correct to the current time and date
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
        response = gs.transaction(server, port, toSend)
        currtime = response['UNIXtimestamp']
        if (abs(currtime - time.time()) >= 1):
            testPassed = "Fail"

        # 3) Send a command over UHF for the OBC to be powered off

        # 4) After 30 seconds have elapsed, power the OBC back on
        time.sleep(30)

        # 5) Downlink all HK data
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
        response = gs.transaction(server, port, toSend)
        # To pass test, roughly 30 seconds should have passed on the OBC's time
        oldTime = currtime
        currTime = response['UNIXtimestamp']
        timeDiff = currTime - oldTime
        if (timeDiff <= 29 or timeDiff >= 31):
            testPassed = "Fail"

        # PASS CONDITION: -> The time and date of the second set of HK data is roughly 30 seconds from the first set's
        return True

    # TODO - Automate the remaining steps in the OBC Solar Panel Current Measurement and Switch Test - 3
    def test_OBC_solarPanelCurrentMeasurementAndSwitch(self):
        testPassed = "Pass"
        # 1) Ensure that the OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware

        # 2) Command the OBC to collect HK data
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0, 0)')
        response = gs.transaction(server, port, toSend)
        # To pass test, all solar panel currents should be with their expected value ranges (0-600 mA for all)
        solarPanelCurrents = ['Port_Current', 'Port_Dep_Current', 'Star_Current', 'Star_Dep_Current', 'Zenith_Current']
        for current in solarPanelCurrents:
            if (response[current] < 0 or response[current] > 600):
                testPassed = "Fail"
        
        # 3) Command the OBC to switch the solar panel current off

        # 4) Command the OBC to collect HK data
        # To pass test, all solar panel currenst should be 0
        solarPanelCurrents = ['Port_Current', 'Port_Dep_Current', 'Star_Current', 'Star_Dep_Current', 'Zenith_Current']
        for current in solarPanelCurrents:
            if (response[current] != 0):
                testPassed = "Fail"

        # Take note of the test results
        if (testPassed == "Pass"):
            colour = '\033[92m' #green
            test.passed += 1
        else:
            colour = '\033[91m' #red
            test.failed += 1

        print(colour + ' - OBC SOLAR PANEL CURRENT MEASUREMENT AND SWITCH TEST ' + testPassed + '\n\n' + '\033[0m')

        # PASS CONDITION: -> Initial HK data collected for the Solar Panels' currents must be within their expected
        #                    value ranges
        #                 -> HK data collected for the Solar Panels' currents after turning off the solar panels
        #                    should be 0
        return True

    # NOTE - Cannot be automated. Test plan contains missing procedures and pass criteria. This test also may
    # or may not be run as it has been flagged as "Pending Iris Design Changes" 
    def test_OBC_commandsViaIris(self):
        return True

    # TODO - Automate the remaining steps in the Iris Data Acquisition Test - 3-7 
    def testIrisDataAcquisitionAndDownlinkOverSBand(self):
        # 1) Ensure that the OBC, UHF, S Band, EPS, and Electra are turned on, and that the OBC and Electra have the most 
        # up-to-date firmware, including Electra image acquisition parameters

        # 2) Establish test target set up (with lenses) infront of the Electra image sensor

        # 3) Command the OBC to deliever an imaging command to Electra to acquire an image file

        # 4) Command the OBC to instruct Electra to compress the image file and return it to Electra SDRAM

        # 5) Command the OBC to instruct Electra to deliever the compressed image file from Electra SDRAM
        # to the OBC for storage onthe OBC SD card

        # 6) Command a downlink of the compressed image file from the OBC SD card via S Band

        # 7) Decompress the image on the GS

        # PASS CONDITION: -> The compressed image file sent over S Band is received and image characteristics
        #                    meet the success criteria of Iris component image testing
        return True

    # TODO - Automate the remaining steps in the YukonSat Payload test - 2-9
    def runYukonSatPayloadTest(self, testType = 0):
        # testType: 0 = Full Functional Test, 1 = Partial Functional Test

        # 1) Ensure that the OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware installed (Doesn't have to be automated)

        # 2) Send a command to upload 2 test image files to the payload

        # Steps 2 & 3 are only completed for the Full Functional Test Plan
        # if (testType == 0):
            # 3) Send a command over UHF connection to reposition the robotic arm to a position that would intersect with the cubesat structure

            # 4) Send a command over UHF connection to reposition the robotic arm to a position that will NOT intersect with the cubesat structure, and will
            # have the screen in the camera FOV

        # 5) Command the OBC to deliver a command to the payload to display the first uploaded image on the screen and capture an image using the camera. Ensure
        # that this captured image is stored as a file on the OBC

        # 6) Command the OBC to deliver a command to the payload to display the second uploaded image on the screen and capture an image using the camera. Ensure
        # that this captured image is stored as a file on the OBC

        # 7) Send a command to downlink both captured images over S Band

        # 8) Send a command to downlink attitude sensor measurement data collected by the IMU over S Band

        # 9) Repeat steps 7-8 using UHF

        # PASS CONDITION: -> The correct image files areb oth successfully displayed on the screen momentarily during their respective steps
        #                 -> For the Full Functional Test, the arm moves to the requested location and stops moving afterwards during step 4.
        #                 -> The images are retrieved at the ground station PC for both UHF and S Band downlink, and the images are displayed and show the screen with
        #                    the correct uploaded image file in the foreground with the appropriate background for the test setup location. 
        #                 -> For the Full Functional Test, the payload during step 3 either:
        #                       -Doesn't move the arm location and responds with a message indiciating that the requested location is forbidden, or
        #                       -The arm moves but stops moving before colliding with the structure, and also responds with a message indiciating that the requested
        #                        location is forbidden
        return True

    # TODO - Automate the remaining steps in the AuroraSat Payload test - 2-6
    def runAuroraSatPayloadTest(self):
        # 1) Ensure that the OBC, UHF, and EPS are turned on, and that the OBC has the most up-to-date firmware installed (Doesn't have to be automated)

        # 2) Send a command to upload 2 test images to the payload. Select the first image to be displayed during the next image capture

        # 3) Send a command to take a picture using the payload's camera and save it as a file on the OBC

        # 4) Send a command to switch the image displayed on the screen to the second image, and take a picture using the payload's camera and save
        # it as a file on the OBC

        # 5) Send a command to downlink both OBC picture files over S-Band

        # 6) Repeat step 5 using UHF

        # PASS CONDITIONS: -> Both pictures are received uncorrupted at the ground station PC and show the correct test images to displayed on the payload
        #                     screen with the background being the test area, for both S-Band and UHF.
        return True

    def getSummary(self):
        test.summary()
        return True