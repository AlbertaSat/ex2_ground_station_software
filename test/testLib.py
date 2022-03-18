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
 * @file commandParser.py
 * @author Dustin Wagner, Daniel Sacro
 * @date 2021-06-28
'''

'''In addition to sending/receiving CSP packets and formatting test results, the class in this 
file also contains a function that runs the OBC system-wide housekeeping test'''

from email.charset import add_charset
import time
import sys
from os import path
from tkinter import W
sys.path.append("./src")
from groundStation import groundStation

import numpy as np

opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())

# TODO - Add in remaining HK variables and their expected values to the following dictionaries:
#        expected_EPS_HK, expected_OBC_HK, expected_charon_HK, expected_sBand_HK, expected_DFGM_HK
#        expected_NIM_HK, expected_yukon_HK
# NOTE - The HK variables to be added in don't exist yet at the time of last edit
class testLib(object):
    def __init__(self):
        self.start = time.time()
        self.failed = 0
        self.passed = 0
        self.response = None
        self.expected_EPS_HK = {
            'vBatt_mv': [7400, 7800], # Battery Voltage in mV
            'curBattIn_mA': [1100, 1100], # Battery Input Current in mA
            'currBattOut_mA': [1, 400], # Battery Output Current in mA
            # Battery State
            'battHeaterMode': [1,1], # Battery Heater Mode (Should be Auto, which is 1)
            'battHeaterState': [0, 0], # Battery Heater State (Should be OFF, which is 0)
            'curSolarPanels1_mA': [0, 0], # MPPT Panel X Current (4 values) in mA
            'curSolarPanels2_mA': [0, 0],
            'curSolarPanels3_mA': [0, 0],
            'curSolarPanels4_mA': [0, 0],
            'curSolarPanels5_mA': [0, 0], # MPPT Panel Y Current (4 values) in mA
            'curSolarPanels6_mA': [0, 0],
            'curSolarPanels7_mA': [0, 0],
            'curSolarPanels8_mA': [0, 0],
            # Solar Panel Voltage (4 values)
            # Solar panel X Power (4 values)
            # Solar panel Y Power (4 values)
            # Charge Current (4 values)
            # Charge Voltage (4 values)
            'mpptMode': 'AUTO', # MPPT Mode
            # Output State (12 values) = outputStatus...?
            # Output Latch-up (12 values)
            'outputFaultCount1': [0, 0], # Output Faults (12 values)
            'outputFaultCount2': [0, 0],
            'outputFaultCount3': [0, 0],
            'outputFaultCount4': [0, 0],
            'outputFaultCount5': [0, 0],
            'outputFaultCount6': [0, 0],
            'outputFaultCount7': [0, 0],
            'outputFaultCount8': [0, 0],
            'outputFaultCount9': [0, 0],
            'outputFaultCount10': [0, 0],
            'outputFaultCount11': [0, 0],
            'outputFaultCount12': [0, 0],
            'outputOnDelta1': [0, 0],# Output Time On (12 values) in seconds
            'outputOnDelta2': [0, 0],
            'outputOnDelta3': [0, 0],
            'outputOnDelta4': [0, 0],
            'outputOnDelta5': [0, 0],
            'outputOnDelta6': [0, 0],
            'outputOnDelta7': [0, 0],
            'outputOnDelta8': [0, 0],
            'outputOnDelta9': [0, 0],
            'outputOnDelta10': [0, 0],
            'outputOnDelta11': [0, 0],
            'outputOnDelta12': [0, 0],
            'outputOffDelta1': [0, 0], # Output Time Off (12 values) in seconds
            'outputOffDelta2': [0, 0],
            'outputOffDelta3': [0, 0],
            'outputOffDelta4': [0, 0],
            'outputOffDelta5': [0, 0],
            'outputOffDelta6': [0, 0],
            'outputOffDelta7': [0, 0],
            'outputOffDelta8': [0, 0],
            'outputOffDelta9': [0, 0],
            'outputOffDelta10': [0, 0],
            'outputOffDelta11': [0, 0],
            'outputOffDelta12': [0, 0],
            'curOutput1_mA': [0, 0], # Output currents (12 values) in mA
            'curOutput2_mA': [0, 0],
            'curOutput3_mA': [0, 0],
            'curOutput4_mA': [0, 0],
            'curOutput5_mA': [0, 0],
            'curOutput6_mA': [118, 550],
            'curOutput7_mA': [0, 0],
            'curOutput8_mA': [0, 0],
            'curOutput9_mA': [36, 232],
            'curOutput10_mA': [0, 0],
            'curOutput11_mA': [0, 0],
            'curOutput12_mA': [0, 0],
            # Output converters (12 values) = OutputConverterVoltage	There is AOcurOutput...?
            # converter Voltage (4 values) = N/A... 		There is output converter voltage?
            'outputConverterState': [1,1], # Converter state (Should be ON, which is assumed to be 1)
            'temp1_c': [17, 35], # MPPT converter temps (4 values) in deg C
            'temp2_c': [17, 35],
            'temp3_c': [17, 35],
            'temp4_c': [17, 35],
            'temp5_c': [17, 35], # output covnerter temp (4 values) in deg C
            'temp6_c': [17, 35],
            'temp7_c': [17, 35],
            'temp8_c': [17, 35],
            'temp9_c': [17, 25], # battery pack temp in deg C
            'temp10_c': [17, 25],
            'temp11_c': [17, 25],
            'temp12_c': [17, 25],
            'wdt_gs_counter': [0, 10], # GS WDT Reboot count
            'wdt_gs_time_left': [1, 86400], # GS WDT Remaining time
            # Last reset reason = last_reset_reason (in Athena HK?)
            'bootCnt': [0, 50]# boot counter = bootCnt
        }
       
        self.expected_OBC_HK = {
            # MCU Temperature - in ADCS...?
            # Converter Temperature
            # Uptime
            # Memory Usage
        }

        self.expected_UHF_HK = {
            'freq': [436.5, 436.5], # Radio frequency in MHz
            'uptime': [1, 21600], # Uptime in s
            'temperature': [17, 25], # Internal Temperature in deg C
        }

        self.expected_solarPanel_HK = {
            'Nadir_Temp1': [0, 70],# Nadir Temp 1 in deg C
            'Nadir_Temp_Adc': [0, 70], # Nadir Temp ADC in deg C
            'Port_Temp1': [0, 70], # Port Temp 1-3  in deg C
            'Port_Temp2': [0, 70],
            'Port_Temp3': [0, 70],
            'Port_Temp_Adc': [0, 70], # Port Temp ADC in deg C
            'Port_Dep_Temp1': [0, 70], # Port Dep Temp 1-3 in deg C
            'Port_Dep_Temp2': [0, 70],
            'Port_Dep_Temp3': [0, 70],
            'Port_Dep_Temp_Adc': [0, 70], # Port Dep Temp ADC in deg C
            'Star_Temp1': [0, 70], # Star Temp 1-3 in deg C
            'Star_Temp2': [0, 70],
            'Star_Temp3': [0, 70],
            'Star_Temp_Adc': [0, 70], # Star Temp ADC in deg C
            'Star_Dep_Temp1': [0, 70], # Star Dep Temp 1-3 in deg C
            'Star_Dep_Temp2': [0, 70],
            'Star_Dep_Temp3': [0, 70],
            'Star_Dep_Temp_Adc': [0, 70], # Star Dep Temp ADC in deg C
            'Zenith_Temp1': [0, 70], # Zenith Temp 1-3 in deg C
            'Zenith_Temp2': [0, 70],
            'Zenith_Temp3': [0, 70],
            'Zenith_Temp_Adc': [0, 70], # Zenith Temp ADC in deg C
            'Nadir_Pd1': [0, 100], # Nadir PD 1 in %
            'Port_Pd1': [0, 100], # Port PD 1-3 in %
            'Port_Pd2': [0, 100],
            'Port_Pd3': [0, 100],
            'Port_Dep_Pd1': [0, 100], # Port Dep PD 1-3 in %
            'Port_Dep_Pd2': [0, 100],
            'Port_Dep_Pd3': [0, 100],
            'Star_Pd1': [0, 100], # Star PD 1-3 in %
            'Star_Pd2': [0, 100],
            'Star_Pd3': [0, 100],
            'Star_Dep_Pd1': [0, 100], # Star Dep PD 1-3 in %
            'Star_Dep_Pd2': [0, 100],
            'Star_Dep_Pd3': [0, 100],
            'Zenith_Pd1': [0, 100], # Zenith PD 1-3 in %
            'Zenith_Pd2': [0, 100],
            'Zenith_Pd3': [0, 100],
            'Port_Voltage': [0, 16500], # Port Voltage in mV
            'Port_Dep_Voltage': [0, 16500], # Port Dep Voltage in mV
            'Star_Voltage': [0, 16500], # Star Voltage in mV
            'Star_Dep_Voltage': [0, 16500], # Star Dep Voltage in mV
            'Zenith_Voltage': [0, 16500], # Zenith Voltage in mV
            'Port_Current': [0, 600], # Port Current in mA
            'Port_Dep_Current': [0, 600], # Port Dep Current in mA
            'Star_Current': [0, 600], # Star Current in mA
            'Star_Dep_Current': [0, 600], # Star Dep Current in mA
            'Zenith_Current': [0, 600], # Zenith Current in mA
        }

        self.expected_charon_HK = {
            # GPS CRC
            # Temperature Sensors 1-8 in deg C
        }

        self.expected_sBand_HK = {
            # Radio Frequency in MHz
            # Encoder Register (bit order, data rate, modulation, filter, scrambler)
            # Status register
            'outputPower': [30, 30],# RF Output Power in dBm
            'PA_Temp': [17, 35], # PA Temperature in deg C
            'Top_Temp': [17, 35], # Top Temperature Sensor in deg C
            'Bottom_Temp': [17, 35], # Bottom Temperature Sensor in deg C
            'Bat_Current': [0],# Battery Current in A
            'Bat_Voltage': [6, 12], # Battery Voltage in V
            'PA_Current': [0.86, 0.86], # PA Current in A
            'PA_Voltage': [5, 5], # PA Voltage in V
        }

        self.expected_iris_HK = {
            # VNIR Sensor Temperature
            # SWIR Sensor Temperature
            # SDRAM usage
            # Number of images
            # Software Version
            # Temp Sensors (0-5)
        }

        self.expected_DFGM_HK = {
            'Sensor_Temperature': [17, 25], # Sensor Temperature in deg C
            'Board_Temperature': [17, 25], # Board Temperature in deg C
            'Reference_Temperature': [17, 25], # Reference Temperature in deg C
            'Input_Voltage': [4900, 5100], # Input Voltage in mV
            'Input_Current': [30, 50], # Input Current in mA
            #'Core_Voltage': [, ], # Core Voltage in mV
            'Positive_Rail_Voltage': [4900, 5100], # Positive Rail Voltage in mV
            'Reference_Voltage': [4900, 5100], # Reference Voltage in mV
        }

        self.expected_NIM_HK = {
            # PCB Temperature 00 - Main Board in deg C
            # PCB Temperature 01 - Main Board in deg C
            # PCB Temperature 02 - Screen board in deg C
            # PCB Temperature 03 - Screen board in deg C
            # PCB Temperature 04 - Camera board in deg C
            # PCB Temperature 05 - Camera board in deg C
            # eNIM Pre-Test Backgronud Reading in Lux
            # eNIM Test Pattern Reading in Lux
        }

        self.expected_yukon_HK = {
            # Temperatures TBD in deg C
            # Motor Encoder Positions
            # Payload MCU RAM Available in Bytes
            # Science Package Data File Size in Bytes
            # TBD Camera Health
            # TBD SD Artwork Buffer Positions in "16 Bytes"
        }

        self.expected_ADCS_HK = {
            # Estimated Angular Rate(s)
            # Estimated Angular Angle(s)
            # Satellite Position (ECI Frame)
            # Satellite Velocity (ECI Frame)
            # Satellite Position (LLH, WGS-84 Frame)
            # ECEF Position
            # Coarse Sun Vector
            # Fine Sun Vector
            # Nadir Vector
            # Wheel Speed
            # Magnetic Field Vector
            # Communication Status
            # Wheel Currents
            # CubeSense Current Measurements
            # CubeControl Current Measurements
            # ADCS Misc. Current Measurements
            # ADCS Temperatures
            # Rate Sensor Temperatures
            # Current ADCS State
        }
        
        pass

    def check_EPS_HK(self):
        checkPassed = True
        for val in self.expected_EPS_HK:
            if (self.response[val] > (self.expected_EPS_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' > ' + str(self.expected_EPS_HK[val][1]))
            elif (self.response[val] < (self.expected_EPS_HK[val])[0]):
                # Less than min
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' < ' + str(self.expected_EPS_HK[val][0]))
            else:
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.expected_EPS_HK[val][0]) + ' <= ' + str(self.response[val]) + ' <= ' + str(self.expected_EPS_HK[val][1]))
        return checkPassed

    def check_OBC_HK(self):
        checkPassed = True
        for val in self.expected_OBC_HK:
            if (self.response[val] > (self.expected_OBC_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' > ' + str(self.expected_OBC_HK[val][1]))
            elif (self.response[val] < (self.expected_OBC_HK[val])[0]):
                # Less than min
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' < ' + str(self.expected_OBC_HK[val][0]))
            else:
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.expected_OBC_HK[val][0]) + ' <= ' + str(self.response[val]) + ' <= ' + str(self.expected_OBC_HK[val][1]))
        return checkPassed

    def check_UHF_HK(self):
        checkPassed = True
        for val in self.expected_UHF_HK:
            if (self.response[val] > (self.expected_UHF_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' > ' + str(self.expected_UHF_HK[val][1]))
            elif (self.response[val] < (self.expected_UHF_HK[val])[0]):
                # Less than min
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' < ' + str(self.expected_UHF_HK[val][0]))
            else:
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.expected_UHF_HK[val][0]) + ' <= ' + str(self.response[val]) + ' <= ' + str(self.expected_UHF_HK[val][1]))
        return checkPassed

    def check_solarPanel_HK(self, ignoringSomeHK = 0):
        checkPassed = True
        # Ignore list contains HK variables from this subsystem that aren't required by the AuroraSat and YukonSat payloads to pass the test
        ignoreList = ['Port_Temp3', 'Port_Dep_Temp3', 'Star_Temp3', 'Star_Dep_Temp3', 'Zenith_Temp3' ,'Port_Pd3' ,'Port_Dep_Pd3' ,'Star_Pd3' ,'Star_Dep_Pd3' ,'Zenith_Pd3']
        for val in self.expected_solarPanel_HK:
            if (ignoringSomeHK and val in ignoreList):
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.response[val]))
            elif (self.response[val] > (self.expected_solarPanel_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' > ' + str(self.expected_solarPanel_HK[val][1]))
            elif (self.response[val] < (self.expected_solarPanel_HK[val])[0]):
                # Less than min
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' < ' + str(self.expected_solarPanel_HK[val][0]))
            else:
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.expected_solarPanel_HK[val][0]) + ' <= ' + str(self.response[val]) + ' <= ' + str(self.expected_solarPanel_HK[val][1]))
        return checkPassed
    
    def check_charon_HK(self, ignoringSomeHk = 0):
        checkPassed = True
        # Ignore list contains HK variables from this subsystem that aren't required by the AuroraSat and YukonSat payloads to pass the test
        ignoreList = [] # TODO - Include the variable name for GPS CRC in this ignoreList
        for val in self.expected_charon_HK:
            if (ignoringSomeHk and val in ignoreList):
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.response[val]))
            elif (self.response[val] > (self.expected_charon_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' > ' + str(self.expected_charon_HK[val][1]))
            elif (self.response[val] < (self.expected_charon_HK[val])[0]):
                # Less than min
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' < ' + str(self.expected_charon_HK[val][0]))
            else:
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.expected_charon_HK[val][0]) + ' <= ' + str(self.response[val]) + ' <= ' + str(self.expected_charon_HK[val][1]))
        return checkPassed

    def check_sBand_HK(self):
        checkPassed = True
        for val in self.expected_sBand_HK:
            if (self.response[val] > (self.expected_sBand_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' > ' + str(self.expected_sBand_HK[val][1]))
            elif (self.response[val] < (self.expected_sBand_HK[val])[0]):
                # Less than min
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' < ' + str(self.expected_sBand_HK[val][0]))
            else:
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.expected_sBand_HK[val][0]) + ' <= ' + str(self.response[val]) + ' <= ' + str(self.expected_sBand_HK[val][1]))
        return checkPassed

    def check_iris_HK(self):
        checkPassed = True
        for val in self.expected_iris_HK:
            if (self.response[val] > (self.expected_iris_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' > ' + str(self.expected_iris_HK[val][1]))
            elif (self.response[val] < (self.expected_iris_HK[val])[0]):
                # Less than min
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' < ' + str(self.expected_iris_HK[val][0]))
            else:
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.expected_iris_HK[val][0]) + ' <= ' + str(self.response[val]) + ' <= ' + str(self.expected_iris_HK[val][1]))
        return checkPassed

    def check_DFGM_HK(self):
        checkPassed = True
        for val in self.expected_DFGM_HK:
            if (self.response[val] > (self.expected_DFGM_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' > ' + str(self.expected_DFGM_HK[val][1]))
            elif (self.response[val] < (self.expected_DFGM_HK[val])[0]):
                # Less than min
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' < ' + str(self.expected_DFGM_HK[val][0]))
            else:
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.expected_DFGM_HK[val][0]) + ' <= ' + str(self.response[val]) + ' <= ' + str(self.expected_DFGM_HK[val][1]))
        return checkPassed

    def check_NIM_HK(self):
        checkPassed = True
        for val in self.expected_NIM_HK:
            if (self.response[val] > (self.expected_NIM_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' > ' + str(self.expected_NIM_HK[val][1]))
            elif (self.response[val] < (self.expected_NIM_HK[val])[0]):
                # Less than min
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' < ' + str(self.expected_NIM_HK[val][0]))
            else:
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.expected_NIM_HK[val][0]) + ' <= ' + str(self.response[val]) + ' <= ' + str(self.expected_NIM_HK[val][1]))
        return checkPassed

    def check_yukon_HK(self):
        checkPassed = True
        self.expected
        for val in self.expected_yukon_HK:
            if (self.response[val] > (self.expected_yukon_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' > ' + str(self.expected_yukon_HK[val][1]))
            elif (self.response[val] < (self.expected_yukon_HK[val])[0]):
                # Less than min
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' < ' + str(self.expected_yukon_HK[val][0]))
            else:
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.expected_yukon_HK[val][0]) + ' <= ' + str(self.response[val]) + ' <= ' + str(self.expected_yukon_HK[val][1]))
        return checkPassed

    def check_ADCS_HK(self):
        checkPassed = True
        for val in self.expected_ADCS_HK:
            if (self.response[val] > (self.expected_ADCS_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' > ' + str(self.expected_ADCS_HK[val][1]))
            elif (self.response[val] < (self.expected_ADCS_HK[val])[0]):
                # Less than min
                colour = '\033[91m' #red
                checkPassed = False
                print(colour + str(val) + ': ' + str(self.response[val]) + ' < ' + str(self.expected_ADCS_HK[val][0]))
            else:
                colour = '\033[0m' #white
                print(colour + str(val) + ': ' + str(self.expected_ADCS_HK[val][0]) + ' <= ' + str(self.response[val]) + ' <= ' + str(self.expected_ADCS_HK[val][1]))
        return checkPassed

    # Checks all HK data by default
    def testHousekeeping(self, EPS = 1, OBC = 1, UHF = 1, solar = 1, charon = 1, sBand = 1, iris = 1, DFGM = 1, NIM = 1, yukon = 1, ADCS = 1):
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
        self.response = gs.transaction(server, port, toSend)
        testPassed = 'Pass'

        if (EPS):
            checkPassed = self.check_OBC_HK()
            if not checkPassed:
                testPassed = 'Fail'
        
        if (OBC):
            checkPassed = self.check_OBC_HK()
            if not checkPassed:
                testPassed = 'Fail'

        if (UHF):
            checkPassed = self.check_UHF_HK()
            if not checkPassed:
                testPassed = 'Fail'

        if (solar):
            # if NIM + yukon > 0, certain HK values will be ignored in the test since the AuroraSat and YukonSat payloads don't require them
            checkPassed = self.check_solarPanel_HK(NIM + yukon)
            if not checkPassed:
                testPassed = 'Fail'

        if (charon):
            # if NIM + yukon > 0, certain HK values will be ignored in the test since the AuroraSat and YukonSat payloads don't require them
            checkPassed = self.check_charon_HK(NIM + yukon)
            if not checkPassed:
                testPassed = 'Fail'

        if (sBand):
            checkPassed = self.check_sBand_HK()
            if not checkPassed:
                testPassed = 'Fail'

        if (iris):
            checkPassed = self.check_iris_HK()
            if not checkPassed:
                testPassed = 'Fail'

        if (DFGM):
            checkPassed = self.check_DFGM_HK()
            if not checkPassed:
                testPassed = 'Fail'

        if (NIM):
            checkPassed = self.check_NIM_HK()
            if not checkPassed:
                testPassed = 'Fail'

        if (yukon):
            checkPassed = self.check_yukon_HK()
            if not checkPassed:
                testPassed = 'Fail'

        if (ADCS):
            checkPassed = self.check_ADCS_HK()
            if not checkPassed:
                testPassed = 'Fail'
        
        # Take note of the test's result
        if (testPassed == 'Pass'):
            colour = '\033[92m' #green
            self.passed += 1
        else:
            colour = '\033[91m' #red
            self.failed += 1

        print(colour + ' - HOUSEKEEPING TEST ' + testPassed + '\n\n' + '\033[0m')
        
        return True

    def sendAndExpect(self, send, expect):
        server, port, toSend = gs.getInput(inVal = send)
        self.response = gs.transaction(server, port, toSend)
        if self.response == expect:
            testpassed = 'Pass'
            colour = '\033[92m' #green
            self.passed += 1
        else:
            testpassed = 'Fail'
            colour = '\033[91m' #red
            self.failed += 1

        print(colour + ' - TEST CASE ' + testpassed + ' -\n\tSent: ' + send +
            '\n\tRecieved: ' + str(self.response) +
            '\n\tExpected: ' + str(expect) + '\n\n' + '\033[0m')
        return self.response == expect

    def send(self, send):
        server, port, toSend = gs.getInput(inVal = send)
        self.response = gs.transaction(server, port, toSend)
        if self.response != {}:
            testpassed = 'Pass'
            colour = '\033[92m' #green
            self.passed += 1
        else:
            testpassed = 'Fail'
            colour = '\033[91m' #red
            self.failed += 1

        print(colour + ' - TEST CASE ' + testpassed + ' -\n\tSent: ' + send +
            '\n\tRecieved: ' + str(self.response) + '\n\n' + '\033[0m')
        return True
    
    def summary(self):
        delta = time.time() - self.start
        print('Summary')
        print('\tTests performed: ' + str(self.failed + self.passed))
        print('\tTime taken: '+ str(round(np.float32(delta), 2)) + 's')
        print('\tPassed: ' + str(self.passed) + ', Failed: ' + str(self.failed))
        success = int(self.passed/(self.passed + self.failed) * 100)
        if success == 100:
            colour = '\033[92m' #green
        elif success >= 80:
            colour = '\033[93m' #yellow
        else:
            colour = '\033[91m' #red
        print(colour + '\t' + str(success) + '%' + ' Success\n' + '\033[0m')
