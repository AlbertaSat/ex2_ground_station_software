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
 * @file test_full_flatsat.py
 * @author Daniel Sacro
 * @date 2022-3-10
'''

'''Please note that many of the ground station commands and housekeeping variables needed in this file do not yet exist at the time of last edit'''
import time
import numpy as np

import sys
import os
sys.path.append("./test")
from testLib import testLib as test

sys.path.append("../src")
from groundStation import groundStation
opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())

test = test() #call to initialize local test class

# This dictionary contains the maximum average power (Watts) that should be consumed by each subsystem component in the Ex-Alta 2 satellite
# NOTE - The maximum average values are stored in a list and are ordered in the following order: Safe Mode (0), Standby (1), DFGM Science (2),
# Imaging (3), and Mixed Science (4)
# Commented numbers beside each value correspond to the quantity of each component
powerBudget_exAlta2 = {
    # ADCS
    'CubeComputer': [0, 0.12, 0.12, 0.12, 0.12], # 1
    'CubeSense': [0, 0.20, 0.20, 0.20, 0.20], # 2
    'Coarse Sun Sensors': [0, 0.1, 0.1, 0.1, 0.1], # 10
    'Torque Rods': [0, 0, 0, 0, 0], # 2
    'Torque Coil': [0, 0, 0, 0, 0], # 1
    'CubeControl': [0, 0, 0.49, 0.49, 0.49], # 1
    'CubeMag': [0, 0.4, 0.4, 0.4, 0.4], # 1
    'Small Plus CubeWheel': [0, 0, 1.14, 1.14, 1.14], # 3
    # Payload
    'IRIS Multispectral Imager': [0, 0, 0, 1.2, 1.2], # 1
    'Digital Fluxgate Magnetometer': [0, 0, 0.40, 0, 0.40], # 1
    # Communications
    'Charon (GPS)': [0, 0, 0, 0, 0], #1
    'S Band Transmitter (Idle)': [0, 0.02, 0.02, 0.02, 0.02], #1
    'S Band Tranmsitter (Transmitting)': [0, 0.25, 0.25, 0.25, 0.25], #1
    'UHF (Transmitting)': [1.16, 1.16, 1.16, 1.16, 1.16], #1
    'UHF (Receiving/Idle)': [0.36, 0.36, 0.36, 0.36, 0.36], #1
    # Power
    'Nanoavionics EPS': [0.15, 0.15, 0.15, 0.15, 0.15], #1
    'Hyperion Solar Panels': [0.07, 0.07, 0.07, 0.07, 0.07], #1
    # OBC
    'Athena OBC': [0.78, 0.78, 0.78, 0.78, 0.78], #1
}

# This dictionary contains the maximum average power (Watts) that should be consumed by each subsystem component in the 2U satellite
# NOTE - The maximum average values are stored in a list and are ordered in the following order: Safe Mode (0), Standby (1), Detumbling (2),
# DFGM Science (3), Payload (4), and Mixed Science (5)
# Commented numbers beside each value correspond to the quantity of each component
powerBudget_2U = {
    # ADCS
    'CubeComputer': [0, 0.12, 0.12, 0.12, 0.12, 0.12], # 1
    'Coarse Sun Sensors': [0, 0.1, 0.1, 0.1, 0.1, 0.1], # 10
    'Torque Rods': [0, 0, 0.7, 0, 0, 0], # 2
    'Torque Coil': [0, 0, 0.3, 0, 0, 0], # 1
    'CubeControl': [0, 0, 0.49, 0.49, 0.49, 0.49], # 1
    'CubeMag': [0, 0.4, 0.4, 0.4, 0.4, 0.4], # 1
    'Small Plus CubeWheel': [0, 0, 0.19, 0.38, 0.38, 0.38], # 3
    # Payload
    '2U Payload': [0, 0, 0, 0, 0.45, 0.45], # 1
    'Digital Fluxgate Magnetometer': [0, 0, 0, 0.40, 0, 0.40], # 1
    # Communications
    'S Band Transmitter (Idle)': [0, 0.02, 0.02, 0.02, 0.02, 0.02], #1
    'S Band Tranmsitter (Transmitting)': [0, 0.25, 0.25, 0.25, 0.25, 0.25], #1
    'UHF (Transmitting)': [1.16, 1.16, 1.16, 1.16, 1.16, 1.16], #1
    'UHF (Receiving/Idle)': [0.36, 0.36, 0.36, 0.36, 0.36, 0.36], #1
    # Power
    'Nanoavionics EPS': [0.15, 0.15, 0.15, 0.15, 0.15, 0.15], #1
    'Hyperion Solar Panels': [0.06, 0.06, 0.06, 0.06, 0.06, 0.06], #1
    # OBC
    'Athena OBC': [0.78, 0.78, 0.78, 0.78, 0.78, 0.78], #1
}

# TODO - Automate the remaining steps in the Validate Power Budget test - 1-5
def validatePowerBudget():
    testPassed = "Pass"

    # 1) Power on the entire FlatSat, and ensure that it is in Standby mode

    # 2) Send a command every ~30 seconds for 1.5 hrs to the OBC to gather system-wide HK info that contains the power consumption of each component (30 sec, 180 times)
    for i in range(180):
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
        response = gs.transaction(server, port, toSend)
        time.sleep(30)
        # Sum up all power consumption values for each component
    # Calculate the average power consumption of each component across all HK measurements (total sum / 180)
    # To pass test, the average power consumption values should not exceed the maximum values given in the power budget

    # 3) Repeat step 2 three more times: Once each for DFGM Science mode, Payload or Imaging mode, and Mixed Science mode

    # 4) Deplete the battery until the EPS enters Safe Mode
    # Connect EPS output channel 10 to a positive terminal of the DC load, and PGND1 to the negative terminal of a DC load
    # Power on the DC load and adjust the current to [TBD] A (0.1 A less than the current software overcurrent limit on channel 10)
    # Once the EPS external LEDs indicate safe mode has been entered, power off the DC load and leave it connected

    # 5) Repeat step 2 ensuring that the FlatSat remains in Safe Mode 

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - CHARON POWER CHANNEL FORCED RESET TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: -> For each operational mode, the calculated average power consumption values of each power channel are less than the values
    #                    specified in the "Nominal Load Calculations" sheet of the appropriate power budget (Table 22 for Ex-Alta 2 or 23 for 2U
    #                    satellites in the FlatSat Test Plan)
    return True

# TODO - Automate the remaining steps in the Safe Mode Behaviour and Recovery test - 2-9, 11, 13-16
def testSafeModeBehaviourAndRecovery():
    testPassed = "Pass"
    # 1) Ensure the EPS battery charger is DISCONNECTED
    input("\nPlease disconnect the EPS battery charger. Press enter to resume tests.\n") 

    # 2) Send a command to save a list of all tasks/processes that are running (Save list of all tasks/processes to a list)
    server, port, toSend = gs.getInput('obc.obc.get_tasks') # TODO - Replace this command with the proper command
    step2Tasks = gs.transaction(server, port, toSend)

    # 3) Deplete the battery until the EPS enters Safe Mode
    # Connect EPS output channel 10 to a positive terminal of the DC load, and PGND1 to the negative terminal of a DC load
    # Power on the DC load and adjust the current to [TBD] A (0.1 A less than the current software overcurrent limit on channel 10)
    # Once the EPS external LEDs indicate safe mode has been entered, power off the DC load and leave it connected 

    # 4) Continually query the system state with a ground station command every 10 seconds and display it on the terminal
    safeMode = -1 # TODO - Replace number with the actual value for "Safe Mode"
    while (True):
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
        response = gs.transaction(server, port, toSend)

        # 5) Continue running the system in this state until Safe Mode is displayed on the ground station PC
        if (response['OBC_mode'] == safeMode):
            break
        else:
            time.sleep(10)  

    # 6) Send a command to save a list of all tasks/processes that are running in Safe Mode (Compare to step 2. Step 2's list should have more items)
    server, port, toSend = gs.getInput('obc.obc.get_tasks') # TODO - Replace this command with the proper command that gets a list of all tasks
    step6Tasks = gs.transaction(server, port, toSend)
    # To pass test, the list of tasks/processes in safe mode (step 6) should be less than that from the normal operations (step 2)
    if (len(step6Tasks) >= len(step2Tasks)):
        testPassed = "Fail"
        
    # 7) Send a command to take an image using Iris (Shouldn't work)
    # To pass test, command response should return unsuccessful

    # 8) Send a command to detumble (Shouldn't work)
    # To pass test, command response should return unsuccessful

    # 9) Send a command to downlink a file over S-Band (Shouldn't work)
    # To pass test, command response should return unsuccessful

    # 10) Send a command to take DFGM data (Shouldn't work)
    server, port, toSend = gs.getInput('obc.dfgm.dfgm_run(1)')
    response = gs.transaction(server, port, toSend)
    # To pass test, command response should return unsuccessful
    if (response['err'] != 1):
        testPassed = "Fail"

    # 11) Send a command to override the safeguard and take DFGM data and save it to a file on the SD card (Should work)
    # TODO - Place a command to override the safeguard here
    server, port, toSend = gs.getInput('obc.dfgm.dfgm_run(1)')
    response = gs.transaction(server, port, toSend)
    # To pass test, command response should return successful
    if (response['err'] != 0):
        testPassed = "Fail"

    # 12) Connect the EPS battery charger
    input("\nPlease connect the EPS battery charger. Press enter to resume tests.\n") 

    # 13) Continually query the system state with a ground station command and display it on the terminal
    normalMode = -1 # TODO - Replace number with the actual value for "Normal Mode"
    while (True):
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
        response = gs.transaction(server, port, toSend)

        # 14) Continue running the system in this state until the EPS enters Normal Mode as displayed on the ground station PC
        if (response['OBC_mode'] == normalMode):
            break
        else:
            time.sleep(10) 

    # 15) Send a command to save a list of all tasks/processes that are running in Normal Mode (Compare to step 2. Both lists should be identical)
    server, port, toSend = gs.getInput('obc.obc.get_tasks') # TODO - Replace this command with the proper command that gets a list of all tasks
    step15Tasks = gs.transaction(server, port, toSend)
    # To pass test, the list of tasks/processes in normal mode (step 15) should be identical to the list from step 2
    if  (len(step15Tasks) != len(step2Tasks)):
        testPassed = "Fail"

    # 16) Send a command to take DFGM data and save it to a file on the SD card (Should work)
    server, port, toSend = gs.getInput('obc.dfgm.dfgm_run(1)')
    response = gs.transaction(server, port, toSend)
    # To pass test, command response should return successful
    if (response['err'] != 0):
        testPassed = "Fail"

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - SAFE MODE BEHAVIOUR AND RECOVERY TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: -> The list of tasks/processes in safe mode (step 6) is less than that from the normal operations (step 2).
    #                 -> None of the commands sent in steps 7-10 are executed, and the command reponses indicate that.
    #                 -> The command sent in step 11 is fully executed and the command response indicates that.
    #                 -> The list of tasks/processes in step 15 is identical to the list from step 2.
    #                 -> The command sent in step 16 is fully executed and the command response indicates that 
    return True

# TODO - Automate the remaining steps in the Charon Power Channel Forced Reset test - 2-4
def testCharonPowerChannelForcedReset():
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

    print(colour + ' - CHARON POWER CHANNEL FORCED RESET TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: -> The number of power channel resets for each channel after the reset command is executed must be one more than before the command is executed
    return True

# TODO - Automate the remaining steps in the Charon Power Channel Forced Reset test - 1, 3
def testClockSynchronizationUsing_GS():
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

# TODO - Automate the remaining steps in the Interruption of S Band Transmission test - 1, 4, 5
def testInterruptionOfSBandTransmission():
    testPassed = "Pass"
    # 1) Send a command to downlink a large file (that would take 2 minutes to complete) over S Band

    # 2) Run ground station S Band SDR to receive data, but eject the SDR in the middle of the transmission period by using the linux command "sudo tee unbind"
    # Run ground station S band SDR to receive data
    # Run linux command "sudo tee unbind"
    os.system('sudo tee unbind')

    # 3) After 20-30 seconds, remount the SDR using the linux command "sudo tee bind". Take any other steps necessary to commission the ground station UHF (such as
    # restarting the gnuradio script)
    time.sleep(30)
    os.system('sudo tee bind')

    # 4) After S Band transmission is complete, send a UHF command to request that the satellite re-transmit the data that was not received by the ground station
    # over another S Band transmission

    # 5) Receive S Band data using ground station SDR and assemble a complete file
    # To pass test, the assmbled file should be identical to the source file on the OBC

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - INTERRUPTION OF S BAND TRANSMISSION TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: -> The assembled file after step 5 is identical to the source file on the OBC
    return True

# TODO - Automate the remaining steps in the Interruption of UHF Uplink test - 1, 4-7, 10
def testInterruptionOf_UHF_uplink():
    testPassed = "Pass"

    # 1) Send a command to run a system-wide health check

    # 2) Immediately eject the UHF SDR using the linux command "sudo tee unbind"
    os.system('sudo tee unbind')

    # 3) After 3 seconds, remount the SDR using the linux command "sudo tee bind". Take any other steps necessary to commision the GS UHF (such as restarting the gnuradio script)
    time.sleep(3)
    os.system('sudo tee bind')

    # 4) Send a command to print all of the OBC's recently executed commands to the terminal
    # To pass test, the command list displayed should NOT include the system-wide health check command from step 1

    # 5) Send a command to run a system-wide health check

    # 6) Send a command to print all of the OBC's recently executed commands to the terminal
    # To pass test, the command list displayed SHOULD include the system-wide health check command from step 5

    # 7) Using the GS PC, initiate upload of an Iris firmware image to the OBC SD card
    # To pass test, there should be NO confirmation from the system that the file has completed uploading

    # 8) After 1 second, eject the UHF SDR using the linux command "sudo tee unbind"
    time.sleep(1)
    os.system('sudo tee unbind')

    # 9) After 3 seconds, remount the SDR using the linux command "sudo tee bind". Take any other steps necessary to commission the GS UHF (such as restarting the gnuradio script)
    time.sleep(3)
    os.system('sudo tee bind')

    # 10) Wait for a response from the system
    time.sleep(240)
    # To pass test, the system responds with a confirmation that the file has completed uploading

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - INTERRUPTION OF UHF UPLINK TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: -> The command list displayed during step 4 does not include the system-wide health check command sent in step 1
    #                 -> The command list displayed during step 6 includes the system-wide health check command in step 5
    #                 -> Before step 8, there is no confirmation from the system that the file has completed uploading
    #                 -> In 1 to 240 (TBC) seconds after step 9, the system responds with a confirmation that the file has completed uploading 
    return True

# TODO - Automate the remaining steps in the Interruption of UHF Downlink test - 1, 4-7, 10
def testInterruptionOf_UHF_downlink():
    testPassed = "Pass"

    # 1) Send a command to run a system-wide health check

    # 2) After 1 second, eject the UHF SDR using the linux command "sudo tee unbind"
    time.sleep(1)
    os.system('sudo tee unbind')

    # 3) After 3 seconds, remount the SDR using the linux command "sudo tee bind". Take any other steps necessary to commission the GS UHF (such as restarting the gnuradio script)
    time.sleep(3)
    os.system('sudo tee bind')

    # 4) Send a command to print all the OBCs recently executed commands
    # To pass test, the command list displayed should NOT include the system-wide health check command from step 1

    # 5) Send a command to run a system-wide health check

    # 6) Send a command to print all the OBCs recently executed commands
    # To pass test, the command list displayed SHOULD include the system-wide health check command from step 5

    # 7) Send a command to downlink the recently acquired housekeeping file
    # To pass test, there should be NO confirmation from the system that the file has completed uploading

    # 8) After 2 seconds, eject the UHF SDR using the linux command "sudo tee unbind"
    time.sleep(2)
    os.system('sudo tee unbind')

    # 9) After 3 seconds, remount the SDR using the linux command "sudo tee bind". Take any other steps necessary to commission the GS UHF (such as restarting the gnuradio script)
    time.sleep(3)
    os.system('sudo tee bind')

    # 10) Wait for a response from the system
    time.sleep(240)
    # To pass test, the system responds with a confirmation that the file has completed uploading

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - INTERRUPTION OF UHF DOWNLINK TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: -> The command list displayed during step 4 does not include the system-wide health check command sent in step 1
    #                 -> The command list displayed during step 6 includes the system-wide health check command sent in step 5
    #                 -> Before step 8, there is no confirmation from the system that the file has completed uploading
    #                 -> In 1 to 240 (TBC) seconds after step 9, the system responds with a confirmation that the file has completed uploading 
    return True

# TODO - Automate the remaining steps in the Interruption of Firmware Update test - 1-3, 6-9
def testInterruptionOfFirmwareUpdate():
    testPassed = "Pass"

    # 1) Ensure that there is a firmware image available for upload from the ground station with a different firmware version number than the one on the satellite

    # 2) Send a command to begin a firmware update

    # 3) Begin updating the onboard firmware image from the GS using the image from step 1

    # 4) After 3 seconds, eject the UHF SDR using the linux command "sudo tee unbind"
    time.sleep(3)
    os.system('sudo tee unbind')

    # 5) After 3 seconds, remount the SDR using the linux command "sudo tee bind". Take any other steps necessary to commission the GS UHF (such as restarting the gnuradio script)
    time.sleep(3)
    os.system('sudo tee bind')

    # 6) Send a command to print the status of the current onboard firmware images to the ground station terminal
    # To pass test, the original image still remains on the satellite (i.e. current image hasn't changed yet)

    # 7) Re-upload or continue uploading the new firmware image

    # 8) Boot the new firmware image

    # 9) Send a command to print the version number of the current firmware image to the GS terminal
    # To pass test, the current image is now the new image uploaded to the satellite

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - INTERRUPTION OF FIRMWARE UPDATE TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: -> After step 6, the original image remains on the satellite, and there is no new image yet
    #                 -> The firmware version number in step 9 is the number from the new image uploaded to the satellite 
    return True

# TODO - Automate the remaining steps in the Mode Change DUring Flight Schedule Activity Execution test - 1-4
def testModeChangeDuringFlightScheduleActivityExecution():
    testPassed = "Pass"
    # 1) Send a command to run system components in a high-power-consumption state until the battery voltage reaches 7.3 V

    # 2) Upload a flight schedule to the stallite that has 2 activities:
    # a) In T+30 s from upload time, runs the system in the same state as step 1 for 5 minutes so that the EPS enters safe mode
    # b) In T+6 minutes, runs the system in the same state as step 1 for 5 minutes

    # 3) After 5 minutes, gather system wide HK on the GS PC
    time.sleep(300)
    server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
    response = gs.transaction(server, port, toSend)
    # To pass test, satellite should be in safe mode, and only the UHF and OBC's power channels are enabled
    safeMode = -1 # TODO - Replace value with the actual value for the safeMode
    if (response['mode'] != safeMode):
        testPassed = "Fail"

    # 4) After 7 minutes, gather system wide HK on the GS PC
    time.sleep(420)
    server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
    response = gs.transaction(server, port, toSend)
    # To pass test, satellite should be in safe mode, and only the UHF and OBC's power channels are enabled
    if (response['mode'] != safeMode):
        testPassed = "Fail"

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - MODE CHANGE DURING FLIGHT SCHEDULE ACTIVITY EXECUTION TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: -> In steps 3 and 4, the housekeeping says the satellite is in safe mode and only the UHF and OBC's power channels are enabled 
    return True

# NOTE - The LEOP test cannot be automated. It requires visual inspections, manual measurements with a multimeter,
# and the physical act of holding down or releasing footswitches or antennas
def test_LEOP():
    return True

# NOTE - The Failed LEOP test cannot be automated. It requires the physical act of holding down deployable mechanisms
def testFailed_LEOP():
    return True

# TODO - Automate the remaining steps in the ITU-requested Transmitter Turn Off and Turn On test - 1-5, 7-11
def test_ITU_requestedTransmitterTurnOffAndTurnOn():
    testPassed = "Pass"

    # 1) Send a command to cease all radio emissions until commanded to resume

    # 2) For the next 10 minutes, observe if any beacons are received on the GS PC

    # 3) Send a command to reboot the OBC

    # 4) After 30 seconds, send a flight schedule using the GS that contains a HK file downlink over both UHF and S Band in T+60 seconds
    time.sleep(30)

    # 5) For the next 10 minutes, observe if any data is received on the GS PC via either UHF or S Band

    # 6) Send a command to hard-reset the EPS
    server, port, toSend = gs.getInput('eps.eps_reset.eps_hard_reset(17767)')
    response = gs.transaction(server, port, toSend)

    # 7) After 30 seconds, send a command to downlink a HK file over UHF
    time.sleep(30)

    # 8) Repeat step 7, but for S Band instead of UHF

    # 9) Repeat step 2

    # 10) Send a command to resume normal operations

    # To pass test, no data transmitted by the satellite during steps 1-10 should be displayed on the GS PC, aside from responses to commands

    # 11) Repeat step 2

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - ITU-REQUESTED TRANSMITTER TURN OFF AND TURN ON TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: -> At no point between steps 1 and 10 (inclusive) is any data transmitted by the satellite displayed on the GS PC, aside from responses
    #                    to commands
    #                 -> Beacons containing nominal values as defined by the housekeeping data sheet are observed at a typical cadence during step 11
    #                       NOTE - Name of HK data sheet is "TX2-SE-XXX Ver. 0.10 Ex-Alta 2 Housekeeping Data"
    return True

# TODO - Automate the remaining steps in the Full Memory Fill test - 1-8
def testFullMemoryFill():
    testPassed = "Pass"

    # 1) Send a command to fill one OBC SD card 99.9% full with ~50 files of dummy data, at least one of which is a HK data file dated one month old

    # 2) Send a command to gather 2 minutes of raw DFGM data and save it to a file on the full SD card. Observe the command response
    server, port, toSend = gs.getInput('obc.dfgm.dfgm_run(120)')
    response = gs.transaction(server, port, toSend)
    # To pass test, the command response should indicate that the data will not be recorded/saved due to a full SD card

    # 3) Send a command to gather an image from the currently attached imaging payload and save it to a file on the full SD card. Observe the command response
    # To pass test, the command response should indicate that the data will not be recorded/saved due to a full SD card

    # 4) Send a command to gather full HK data and save it to a file on the full SD card. Observe the command response
    server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
    response = gs.transaction(server, port, toSend)
    # To pass test, the command response should indicate that the data will not be recorded/saved due to a full SD card

    # 5) Send a command to upload a large file to the full SD card. Observce the command response

    # 6) Send a command to fill the OBC RAM 99% full with dummy data

    # 7) Send a command to allocate 2% of the total OBC RAM. Observe the command response
    # To pass test, the OBC does not allocate the newly requested RAM and remains at 99% RAM usage

    # 8) Using the GS PC, attempt to perform a firmware update with a dummy image that is larger than the OBC flash storage size. Observe the response
    # To pass test, the OBC should NOT update the firmware image, and the previous firmware image SHOULD still be retained in memory

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - FULL MEMORY FILL TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: -> After step 2, the command response indicates that DFGM data will not be recorded due to a full SD card
    #                 -> After step 3, the command response indicates that image data will not be recorded due to full SD card
    #                 -> After step 4, the command response indicates that HK data has overwritten oldest dated stored HK data
    #                 -> After step 7, the OBC does not allocate the newly requested RAM and remains at 99% RAM usage. This must be clearly indicated in the
    #                    command response
    #                 -> After step 8, the OBC does not update the firmware image, and the previous firmware image is retained in memory. This must be clearly
    #                    indicated in the command response 
    return True

# TODO - Automate the remaining steps in the Send Commands to EPS via Iris test - 1-6
def testSendCommandsTo_EPS_viaIris(): # NOTE - TBC pending Iris design changes. There may be changes to this test
    testPassed = "Pass"

    # 1) Send a command to turn off the OBC

    # 2) Send a command to the EPS through Iris to reset the OBC power channel for 10 seconds. Wait 10 seconds

    # 3) Send a command to ping the OBC
    # To pass test, the OBC's response to the ping is observed

    # 4) Send a command to Iris to gather and downlink raw EPS HK data over UHF and display it on the terminal
    # To pass test, all HK data values should be displayed on the terminal with all values being nominal, and the last reset reason should not be "Power_on"

    # 5) Send a command to Iris to perform an EPS hard-reset

    # 6) After 10 seconds, repeat step 4
    # To pass test, the last reset reason should be "Power_on"

    # Take note of the test results
    if (testPassed == "Pass"):
        colour = '\033[92m' #green
        test.passed += 1
    else:
        colour = '\033[91m' #red
        test.failed += 1

    print(colour + ' - SEND COMMANDS TO EPS VIA IRIS TEST ' + testPassed + '\n\n' + '\033[0m')

    # PASS CONDITION: -> An OBC response to the ping sent in step 3 is observed on the GS PC
    #                 -> All HK data is displayed on the terminal during step 4 and all values are nominal according to the housekeeping data sheet, and the
    #                    "Last Reset Reason" field DOES NOT equal "Power_on"
    #                 -> The "Last Reset Reason" field displayed during step 6 equals "Power_on" 
    return True

# NOTE - The Day in the Life test cannot be automated. "All 'Expected Results' will be verified by a human"
def testDayInTheLife():
    # For the Prototype FlatSat, run the "Daily Activity Sample for Ex-Alta 2"

    # For the Ex-Alta 2 Protoflight FlatSat, run the "Daily Activity Sample for Ex-Alta 2"

    # For the AuroraSat Protoflight FlatSat, run the "Daily Activity Sample for AuroraSat"

    # For the YukonSat Protoflight FlatSat, run the "Daily Activity Sample for YukonSat"

    # PASS CONDITION: -> All DFGM, image, and HK data was downlinked to the GS PC and is not corrupted 
    #                 -> All DFGM data magnitude and direction is within +/- 10% of the expected magnetic field 
    #                    at the time, position, and orientation of the test, with an expected level of noise and
    #                    interference present
    #                 -> When viewed as images, all image data shows the test pattern at the expected resolution
    #                    and focus
    #                 -> All received housekeeping values are nominal as defined in the HK data sheet
    #                 -> All file delete operations were successful
    #                 -> ADCS TLE was updated successfully
    #                 -> All onboard clock synchronoizations were performed successfully
    #                 -> If any anomalies occur, their root cause was traced back to operator failure (not system
    #                    failure), and were successfully recovered from 
    return True

# NOTE - The Week in the Life test cannot be automated. "All 'Expected Results' will be verified by a human"
def testWeekInTheLife():
    # Ensure that OBC tools used to detect and flat memory leaks and uninitialized memory reads are enabled

    # For the Prototype FlatSat, run the "Daily Activity Sample for Ex-Alta 2"

    # For the Ex-Alta 2 Protoflight FlatSat, run the "Daily Activity Sample for Ex-Alta 2"

    # For the AuroraSat Protoflight FlatSat, run the "Daily Activity Sample for AuroraSat"

    # For the YukonSat Protoflight FlatSat, run the "Daily Activity Sample for YukonSat"

    # PASS CONDITION: -> All DFGM, image, and HK data was downlinked to the GS PC and is not corrupted 
    #                 -> All DFGM data magnitude and direction is within +/- 10% of the expected magnetic field 
    #                    at the time, position, and orientation of the test, with an expected level of noise and
    #                    interference present
    #                 -> When viewed as images, all image data shows the test pattern at the expected resolution
    #                    and focus
    #                 -> All received housekeeping values are nominal as defined in the HK data sheet
    #                 -> All file delete operations were successful
    #                 -> ADCS TLE was updated successfully 
    #                 -> All onboard clock synchronoizations were performed successfully
    #                 -> No memory leaks or reads from uninitialized memory are flagged 
    #                 -> If any anomalies occur, their root cause was traced back to operator failure (not system
    #                    failure), and were successfully recovered from
    return True

def testAllCommandsToOBC():
    print("\n---------- VALIDATE POWER BUDGET TEST ----------\n")
    # TODO - Finish function implementation
    validatePowerBudget()
    
    print("\n---------- SAFE MODE BEHAVIOUR AND RECOVERY TEST ----------\n")
    # TODO - Finish function implementation
    testSafeModeBehaviourAndRecovery()    

    print("\n---------- CHARON POWER CHANNEL FORCED RESET TEST ----------\n")
    # TODO  - Finish function implementation
    testCharonPowerChannelForcedReset()
    
    print("\n---------- CLOCK SYNCHRONIZATION USING GROUND STATION TEST ----------\n")
    # TODO - Finish function implementation
    testClockSynchronizationUsing_GS()

    print("\n---------- INTERRUPTION OF S BAND TRANSMISSION TEST ----------\n")
    # TODO - Finish function implementation
    testInterruptionOfSBandTransmission()

    print("\n---------- INTERRUPTION OF UHF UPLINK TEST ----------\n")
    # TODO - Finish function implementation
    testInterruptionOf_UHF_uplink()

    print("\n---------- INTERRUPTION OF UHF DOWNLINK TEST ----------\n")
    # TODO - Finish function implementation
    testInterruptionOf_UHF_downlink()
    
    print("\n---------- INTERRUPTION OF FIRMWARE UPDATE TEST ----------\n")
    # TODO - Finish function implementation
    testInterruptionOfFirmwareUpdate()

    print("\n---------- MODE CHANGE DURING FLIGHT SCHEDULE ACTIVITY EXECUTION TEST ----------\n")
    # TODO - Finish function implementation
    testModeChangeDuringFlightScheduleActivityExecution()

    print("\n---------- ITU-REQUESTED TRANSMITTER TURN OFF AND TURN ON TEST ----------\n")
    # TODO  - Finish function implementation
    test_ITU_requestedTransmitterTurnOffAndTurnOn()

    print("\n---------- FULL MEMORY FILL TEST ----------\n")
    # TODO  - Finish function implementation
    testFullMemoryFill()

    print("\n---------- SEND COMMANDS TO EPS VIA IRIS TEST ----------\n")
    # TODO  - Finish function implementation
    testSendCommandsTo_EPS_viaIris()

    test.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
