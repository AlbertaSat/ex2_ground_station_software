'''
 * Copyright (C) 2022  University of Alberta
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
 * @file expected_eps_hk.py
 * @author Jenish Patel
 * @date 2022-08-08
'''

expected_EPS_HK = {
    # Battery Voltage in mV, 7400 is the threshold for passing from safe to normal mode, 8400 is full
    'vBatt_mV': [7400, 8400],
    # Battery Input Current in mA, 0 when not being charged, not sure what the max should be
    'curBattIn_mA': [0, 1100],
    # Battery Output Current in mA, 0 when no outputs are on
    'curBattOut_mA': [0, 400],
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
    'wdt_gs_time_left_s': [1, 86400],
    # Last reset reason = last_reset_reason (in Athena HK?)
    # boot counter = bootCnt, made max large due to EPS issues
    'bootCnt': [0, 500]
}