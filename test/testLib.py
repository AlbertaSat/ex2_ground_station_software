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
 * @file testLib.py
 * @author Dustin Wagner, Daniel Sacro
 * @date 2021-06-28
'''

'''In addition to sending/receiving CSP packets and formatting test results, the class in this 
file also contains a function that runs the OBC system-wide housekeeping test'''

import numpy as np
from groundStation import groundStation
import time
import sys
from os import path
sys.path.append("./src")


opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())

# TODO - Add in remaining HK variables and their expected values to the following dictionaries:
#        expected_EPS_HK, expected_OBC_HK, expected_charon_HK, expected_sBand_HK, expected_DFGM_HK
#        expected_NIM_HK, expected_yukon_HK, expected_adcs_HK
# NOTE - The HK variables to be added in don't exist yet at the time of last edit


class testLib(object):
    def __init__(self):
        self.start = time.time()
        self.failed = 0
        self.passed = 0
        self.response = None
        self.expected_EPS_HK = {
            # Battery Voltage in mV, 7400 is the threshold for passing from safe to normal mode, 8400 is full
            'vBatt_mv': [7400, 8400],
            # Battery Input Current in mA, 0 when not being charged, not sure what the max should be
            'curBattIn_mA': [0, 1100],
            # Battery Output Current in mA, 0 when no outputs are on
            'currBattOut_mA': [0, 400],
            # Battery State, 0 for critical, 1 for safe, 2 for normal, 3 for full
            'battMode': [0, 3],
            # Battery Heater Mode (Should be Auto, which is 1, switches to 0 after reset)
            'battHeaterMode': [0, 1],
            # Battery Heater State (Should be OFF, which is 0)
            'battHeaterState': [0, 0],
            # MPPT Panel X Current (4 values) in mA, could go up to 500mA (estimate) if solar panels are plugged in and charging
            'curSolarPanels1_mA': [0, 500],
            'curSolarPanels2_mA': [0, 500],
            'curSolarPanels3_mA': [0, 500],
            'curSolarPanels4_mA': [0, 500],
            # MPPT Panel Y Current (4 values) in mA
            'curSolarPanels5_mA': [0, 500],
            'curSolarPanels6_mA': [0, 500],
            'curSolarPanels7_mA': [0, 500],
            'curSolarPanels8_mA': [0, 500],
            # Solar Panel Voltage (4 values) max seen during testing was 15.4V
            'mpptConverterVoltage1_mV': [0, 16000],
            'mpptConverterVoltage2_mV': [0, 16000],
            'mpptConverterVoltage3_mV': [0, 16000],
            'mpptConverterVoltage4_mV': [0, 16000],
            # Solar panel X Power (4 values), N/A
            # Solar panel Y Power (4 values), N/A
            # Charge Current (4 values), maybe just 1 value for all solar panels summed up - not sure what max should be
            'curSolar_mA': [0, 500],
            # Charge Voltage (4 values), N/A or maybe equal to battery voltage
            # MPPT Mode, should be auto but could be HW after a reset, 0 for HW, 1 for manual, 2 for auto, 3 for auto w/ timeout
            'mpptMode': [0, 3],
            # Output State (12 values) = outputStatus...?, N/A
            # Output Latch-up (12 values), N/A
            'outputFaultCount1': [0, 0],  # Output Faults (12 values)
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
            'outputOnDelta1': [0, 0],  # Output Time On (12 values) in seconds
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
            # Output Time Off (12 values) in seconds
            'outputOffDelta1': [0, 0],
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
            'curOutput1_mA': [0, 0],  # Output currents (12 values) in mA
            'curOutput2_mA': [0, 0],
            'curOutput3_mA': [0, 0],
            'curOutput4_mA': [0, 0],
            'curOutput5_mA': [0, 0],
            # Current for OBC which must be on for these tests, didn't touch max/min
            'curOutput6_mA': [118, 550],
            'curOutput7_mA': [0, 0],
            'curOutput8_mA': [0, 0],
            # Current for OBC which must be on for these tests, didn't touch max/min
            'curOutput9_mA': [36, 232],
            'curOutput10_mA': [0, 0],
            'curOutput11_mA': [0, 0],
            'curOutput12_mA': [0, 0],
            # Output converters (12 values) = OutputConverterVoltage	There is AOcurOutput...?
            # converter Voltage (4 values) = N/A... 		There is output converter voltage?
            # Converter state, 4 bit binary number in decimal where XXXX represents the states of each of the 4 converters
            'outputConverterState': [0, 15],
            'temp1_c': [17, 35],  # MPPT converter temps (4 values) in deg C
            'temp2_c': [17, 35],
            'temp3_c': [17, 35],
            'temp4_c': [17, 35],
            'temp5_c': [17, 35],  # output converter temp (4 values) in deg C
            'temp6_c': [17, 35],
            'temp7_c': [17, 35],
            'temp8_c': [17, 35],
            'temp9_c': [17, 25],  # battery pack temp in deg C
            'temp10_c': [17, 25],
            'temp11_c': [17, 25],
            'temp12_c': [17, 25],
            # GS WDT Reboot count, made the max really large due to EPS issues
            'wdt_gs_counter': [0, 1000],
            # GS WDT Remaining time, max is 24 hours
            'wdt_gs_time_left': [1, 86400],
            # Last reset reason = last_reset_reason (in Athena HK?)
            # boot counter = bootCnt, made max large due to EPS issues
            'bootCnt': [0, 500]
        }

        self.expected_OBC_HK = {
            # MCU Temperature - in ADCS...?
            # Converter Temperature
            # Uptime
            # Memory Usage
        }

        self.expected_UHF_HK = {
            'freq': [436.5, 436.5],  # Radio frequency in MHz
            'uptime': [1, 21600],  # Uptime in s
            'temperature': [17, 25],  # Internal Temperature in deg C
        }

        self.expected_solarPanel_HK = {
            'Nadir_Temp1': [0, 70],  # Nadir Temp 1 in deg C
            'Nadir_Temp_Adc': [0, 70],  # Nadir Temp ADC in deg C
            'Port_Temp1': [0, 70],  # Port Temp 1-3  in deg C
            'Port_Temp2': [0, 70],
            'Port_Temp3': [0, 70],
            'Port_Temp_Adc': [0, 70],  # Port Temp ADC in deg C
            'Port_Dep_Temp1': [0, 70],  # Port Dep Temp 1-3 in deg C
            'Port_Dep_Temp2': [0, 70],
            'Port_Dep_Temp3': [0, 70],
            'Port_Dep_Temp_Adc': [0, 70],  # Port Dep Temp ADC in deg C
            'Star_Temp1': [0, 70],  # Star Temp 1-3 in deg C
            'Star_Temp2': [0, 70],
            'Star_Temp3': [0, 70],
            'Star_Temp_Adc': [0, 70],  # Star Temp ADC in deg C
            'Star_Dep_Temp1': [0, 70],  # Star Dep Temp 1-3 in deg C
            'Star_Dep_Temp2': [0, 70],
            'Star_Dep_Temp3': [0, 70],
            'Star_Dep_Temp_Adc': [0, 70],  # Star Dep Temp ADC in deg C
            'Zenith_Temp1': [0, 70],  # Zenith Temp 1-3 in deg C
            'Zenith_Temp2': [0, 70],
            'Zenith_Temp3': [0, 70],
            'Zenith_Temp_Adc': [0, 70],  # Zenith Temp ADC in deg C
            'Nadir_Pd1': [0, 100],  # Nadir PD 1 in %
            'Port_Pd1': [0, 100],  # Port PD 1-3 in %
            'Port_Pd2': [0, 100],
            'Port_Pd3': [0, 100],
            'Port_Dep_Pd1': [0, 100],  # Port Dep PD 1-3 in %
            'Port_Dep_Pd2': [0, 100],
            'Port_Dep_Pd3': [0, 100],
            'Star_Pd1': [0, 100],  # Star PD 1-3 in %
            'Star_Pd2': [0, 100],
            'Star_Pd3': [0, 100],
            'Star_Dep_Pd1': [0, 100],  # Star Dep PD 1-3 in %
            'Star_Dep_Pd2': [0, 100],
            'Star_Dep_Pd3': [0, 100],
            'Zenith_Pd1': [0, 100],  # Zenith PD 1-3 in %
            'Zenith_Pd2': [0, 100],
            'Zenith_Pd3': [0, 100],
            'Port_Voltage': [0, 16500],  # Port Voltage in mV
            'Port_Dep_Voltage': [0, 16500],  # Port Dep Voltage in mV
            'Star_Voltage': [0, 16500],  # Star Voltage in mV
            'Star_Dep_Voltage': [0, 16500],  # Star Dep Voltage in mV
            'Zenith_Voltage': [0, 16500],  # Zenith Voltage in mV
            'Port_Current': [0, 600],  # Port Current in mA
            'Port_Dep_Current': [0, 600],  # Port Dep Current in mA
            'Star_Current': [0, 600],  # Star Current in mA
            'Star_Dep_Current': [0, 600],  # Star Dep Current in mA
            'Zenith_Current': [0, 600],  # Zenith Current in mA
        }

        self.expected_charon_HK = {
            # GPS CRC
            # Temperature Sensors 1-8 in deg C
        }

        self.expected_sBand_HK = {
            # Radio Frequency in MHz
            # Encoder Register (bit order, data rate, modulation, filter, scrambler)
            # Status register
            'outputPower': [30, 30],  # RF Output Power in dBm
            'PA_Temp': [17, 35],  # PA Temperature in deg C
            'Top_Temp': [17, 35],  # Top Temperature Sensor in deg C
            'Bottom_Temp': [17, 35],  # Bottom Temperature Sensor in deg C
            'Bat_Current': [0],  # Battery Current in A
            'Bat_Voltage': [6, 12],  # Battery Voltage in V
            'PA_Current': [0.86, 0.86],  # PA Current in A
            'PA_Voltage': [5, 5],  # PA Voltage in V
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
            'Sensor_Temperature': [17, 25],  # Sensor Temperature in deg C
            'Board_Temperature': [17, 25],  # Board Temperature in deg C
            # Reference Temperature in deg C
            'Reference_Temperature': [17, 25],
            'Input_Voltage': [4900, 5100],  # Input Voltage in mV
            'Input_Current': [30, 50],  # Input Current in mA
            # 'Core_Voltage': [, ], # Core Voltage in mV
            # Positive Rail Voltage in mV
            'Positive_Rail_Voltage': [4900, 5100],
            'Reference_Voltage': [4900, 5100],  # Reference Voltage in mV
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
            'Estimated_Angular_Rate_X': [0, 1],
            'Estimated_Angular_Rate_Y': [0, 1],
            'Estimated_Angular_Rate_Z': [0, 1],
            'Estimated_Angular_Angle_X': [-180, 180],
            'Estimated_Angular_Angle_Y': [-180, 180],
            'Estimated_Angular_Angle_Z': [-180, 180],
            'Sat_Position_ECI_X': [-10000, 10000],
            'Sat_Position_ECI_Y': [-10000, 10000],
            'Sat_Position_ECI_Z': [-10000, 10000],
            'Sat_Velocity_ECI_X': [-10000, 10000],
            'Sat_Velocity_ECI_Y': [-10000, 10000],
            'Sat_Velocity_ECI_Z': [-10000, 10000],
            'Sat_Position_LLH_X': [-90, 90], # Latitude
            'Sat_Position_LLH_Y': [-180, 180], # Longitude
            'Sat_Position_LLH_Z': [0, 1],
            'ECEF_Position_X': [0, 1],
            'ECEF_Position_Y': [0, 1],
            'ECEF_Position_Z': [0, 1],
            'Coarse_Sun_Vector_X': [0, 1],
            'Coarse_Sun_Vector_Y': [0, 1],
            'Coarse_Sun_Vector_Z': [0, 1],
            'Fine_Sun_Vector_X': [0, 1],
            'Fine_Sun_Vector_Y': [0, 1],
            'Fine_Sun_Vector_Z': [0, 1],
            'Nadir_Vector_X': [0, 1],
            'Nadir_Vector_Y': [0, 1],
            'Nadir_Vector_Z': [0, 1],
            'Wheel_Speed_X': [0, 1],
            'Wheel_Speed_Y': [0, 1],
            'Wheel_Speed_Z': [0, 1],
            'Mag_Field_Vector_X': [0, 1],
            'Mag_Field_Vector_Y': [0, 1],
            'Mag_Field_Vector_Z': [0, 1],
            'TC_num': [0, 1],
            'TM_num': [0, 1],
            'CommsStat_flags_1': [0, 1],
            'CommsStat_flags_2': [0, 1],
            'CommsStat_flags_3': [0, 1],
            'CommsStat_flags_4': [0, 1],
            'CommsStat_flags_5': [0, 1],
            'CommsStat_flags_6': [0, 1],
            'Wheel1_Current': [0, 1],
            'Wheel2_Current': [0, 1],
            'Wheel3_Current': [0, 1],
            'CubeSense1_Current': [0, 1],
            'CubeSense2_Current': [0, 1],
            'CubeControl_Current3v3': [0, 1],
            'CubeControl_Current5v0': [0, 1],
            'CubeStar_Current': [0, 1],
            'CubeStar_Temp': [0, 1],
            'Magnetorquer_Current': [0, 1],
            'MCU_Temp': [0, 1],
            'Rate_Sensor_Temp_X': [0, 1],
            'Rate_Sensor_Temp_Y': [0, 1],
            'Rate_Sensor_Temp_Z': [0, 1],
        }

        pass

    def check_EPS_HK(self):
        checkPassed = True
        for val in self.expected_EPS_HK:
            if (self.response[val] > (self.expected_EPS_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' > ' + str(self.expected_EPS_HK[val][1]))
            elif (self.response[val] < (self.expected_EPS_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' < ' + str(self.expected_EPS_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.expected_EPS_HK[val][0]) + ' <= ' + str(
                    self.response[val]) + ' <= ' + str(self.expected_EPS_HK[val][1]))
        return checkPassed

    def check_OBC_HK(self):
        checkPassed = True
        for val in self.expected_OBC_HK:
            if (self.response[val] > (self.expected_OBC_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' > ' + str(self.expected_OBC_HK[val][1]))
            elif (self.response[val] < (self.expected_OBC_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' < ' + str(self.expected_OBC_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.expected_OBC_HK[val][0]) + ' <= ' + str(
                    self.response[val]) + ' <= ' + str(self.expected_OBC_HK[val][1]))
        return checkPassed

    def check_UHF_HK(self):
        checkPassed = True
        for val in self.expected_UHF_HK:
            if (self.response[val] > (self.expected_UHF_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' > ' + str(self.expected_UHF_HK[val][1]))
            elif (self.response[val] < (self.expected_UHF_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' < ' + str(self.expected_UHF_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.expected_UHF_HK[val][0]) + ' <= ' + str(
                    self.response[val]) + ' <= ' + str(self.expected_UHF_HK[val][1]))
        return checkPassed

    def check_solarPanel_HK(self, ignoringSomeHK=0):
        checkPassed = True
        # Ignore list contains HK variables from this subsystem that aren't required by the AuroraSat and YukonSat payloads to pass the test
        ignoreList = ['Port_Temp3', 'Port_Dep_Temp3', 'Star_Temp3', 'Star_Dep_Temp3',
                      'Zenith_Temp3', 'Port_Pd3', 'Port_Dep_Pd3', 'Star_Pd3', 'Star_Dep_Pd3', 'Zenith_Pd3']
        for val in self.expected_solarPanel_HK:
            if (ignoringSomeHK and val in ignoreList):
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.response[val]))
            elif (self.response[val] > (self.expected_solarPanel_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' > ' + str(self.expected_solarPanel_HK[val][1]))
            elif (self.response[val] < (self.expected_solarPanel_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' < ' + str(self.expected_solarPanel_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.expected_solarPanel_HK[val][0]) + ' <= ' + str(
                    self.response[val]) + ' <= ' + str(self.expected_solarPanel_HK[val][1]))
        return checkPassed

    def check_charon_HK(self, ignoringSomeHk=0):
        checkPassed = True
        # Ignore list contains HK variables from this subsystem that aren't required by the AuroraSat and YukonSat payloads to pass the test
        ignoreList = []  # TODO - Include the variable name for GPS CRC in this ignoreList
        for val in self.expected_charon_HK:
            if (ignoringSomeHk and val in ignoreList):
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.response[val]))
            elif (self.response[val] > (self.expected_charon_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' > ' + str(self.expected_charon_HK[val][1]))
            elif (self.response[val] < (self.expected_charon_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' < ' + str(self.expected_charon_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.expected_charon_HK[val][0]) + ' <= ' + str(
                    self.response[val]) + ' <= ' + str(self.expected_charon_HK[val][1]))
        return checkPassed

    def check_sBand_HK(self):
        checkPassed = True
        for val in self.expected_sBand_HK:
            if (self.response[val] > (self.expected_sBand_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' > ' + str(self.expected_sBand_HK[val][1]))
            elif (self.response[val] < (self.expected_sBand_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' < ' + str(self.expected_sBand_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.expected_sBand_HK[val][0]) + ' <= ' + str(
                    self.response[val]) + ' <= ' + str(self.expected_sBand_HK[val][1]))
        return checkPassed

    def check_iris_HK(self):
        checkPassed = True
        for val in self.expected_iris_HK:
            if (self.response[val] > (self.expected_iris_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' > ' + str(self.expected_iris_HK[val][1]))
            elif (self.response[val] < (self.expected_iris_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' < ' + str(self.expected_iris_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.expected_iris_HK[val][0]) + ' <= ' + str(
                    self.response[val]) + ' <= ' + str(self.expected_iris_HK[val][1]))
        return checkPassed

    def check_DFGM_HK(self):
        checkPassed = True
        for val in self.expected_DFGM_HK:
            if (self.response[val] > (self.expected_DFGM_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' > ' + str(self.expected_DFGM_HK[val][1]))
            elif (self.response[val] < (self.expected_DFGM_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' < ' + str(self.expected_DFGM_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.expected_DFGM_HK[val][0]) + ' <= ' + str(
                    self.response[val]) + ' <= ' + str(self.expected_DFGM_HK[val][1]))
        return checkPassed

    def check_NIM_HK(self):
        checkPassed = True
        for val in self.expected_NIM_HK:
            if (self.response[val] > (self.expected_NIM_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' > ' + str(self.expected_NIM_HK[val][1]))
            elif (self.response[val] < (self.expected_NIM_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' < ' + str(self.expected_NIM_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.expected_NIM_HK[val][0]) + ' <= ' + str(
                    self.response[val]) + ' <= ' + str(self.expected_NIM_HK[val][1]))
        return checkPassed

    def check_yukon_HK(self):
        checkPassed = True
        self.expected
        for val in self.expected_yukon_HK:
            if (self.response[val] > (self.expected_yukon_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' > ' + str(self.expected_yukon_HK[val][1]))
            elif (self.response[val] < (self.expected_yukon_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' < ' + str(self.expected_yukon_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.expected_yukon_HK[val][0]) + ' <= ' + str(
                    self.response[val]) + ' <= ' + str(self.expected_yukon_HK[val][1]))
        return checkPassed

    def check_ADCS_HK(self):
        checkPassed = True
        for val in self.expected_ADCS_HK:
            if (self.response[val] > (self.expected_ADCS_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' > ' + str(self.expected_ADCS_HK[val][1]))
            elif (self.response[val] < (self.expected_ADCS_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(self.response[val]) + ' < ' + str(self.expected_ADCS_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(self.expected_ADCS_HK[val][0]) + ' <= ' + str(
                    self.response[val]) + ' <= ' + str(self.expected_ADCS_HK[val][1]))
        return checkPassed

    # Checks all HK data by default
    def testHousekeeping(self, EPS=1, OBC=1, UHF=1, solar=1, charon=1, sBand=1, iris=1, DFGM=1, NIM=1, yukon=1, ADCS=1):
        server, port, toSend = gs.getInput('obc.housekeeping.get_hk(1, 0 ,0)')
        self.response = gs.transaction(server, port, toSend)
        testPassed = 'Pass'

        if (EPS):
            checkPassed = self.check_EPS_HK()
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
            colour = '\033[92m'  # green
            self.passed += 1
        else:
            colour = '\033[91m'  # red
            self.failed += 1

        print(colour + ' - HOUSEKEEPING TEST ' +
              testPassed + '\n\n' + '\033[0m')

        return True

    def sendAndExpect(self, send, expect):
        server, port, toSend = gs.getInput(inVal=send)
        self.response = gs.transaction(server, port, toSend)
        if self.response == expect:
            testpassed = 'Pass'
            colour = '\033[92m'  # green
            self.passed += 1
        else:
            testpassed = 'Fail'
            colour = '\033[91m'  # red
            self.failed += 1

        print(colour + ' - TEST CASE ' + testpassed + ' -\n\tSent: ' + send +
              '\n\tRecieved: ' + str(self.response) +
              '\n\tExpected: ' + str(expect) + '\n\n' + '\033[0m')
        return self.response == expect

    def send(self, send):
        server, port, toSend = gs.getInput(inVal=send)
        self.response = gs.transaction(server, port, toSend)
        if self.response != {}:
            testpassed = 'Pass'
            colour = '\033[92m'  # green
            self.passed += 1
        else:
            testpassed = 'Fail'
            colour = '\033[91m'  # red
            self.failed += 1

        print(colour + ' - TEST CASE ' + testpassed + ' -\n\tSent: ' + send +
              '\n\tRecieved: ' + str(self.response) + '\n\n' + '\033[0m')
        return True

    def summary(self):
        delta = time.time() - self.start
        print('Summary')
        print('\tTests performed: ' + str(self.failed + self.passed))
        print('\tTime taken: ' + str(round(np.float32(delta), 2)) + 's')
        print('\tPassed: ' + str(self.passed) +
              ', Failed: ' + str(self.failed))
        success = int(self.passed/(self.passed + self.failed) * 100)
        if success == 100:
            colour = '\033[92m'  # green
        elif success >= 80:
            colour = '\033[93m'  # yellow
        else:
            colour = '\033[91m'  # red
        print(colour + '\t' + str(success) + '%' + ' Success\n' + '\033[0m')
