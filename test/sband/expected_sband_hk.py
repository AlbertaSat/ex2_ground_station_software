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
 * @file expected_sband_hk.py
 * @author Jenish Patel
 * @date 2022-08-08
'''

expected_sBand_HK = {
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