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
 * @file expected_dfgm_hk.py
 * @author Jenish Patel
 * @date 2022-08-08
'''

expected_DFGM_HK = {
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