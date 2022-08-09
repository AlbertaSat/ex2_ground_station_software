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
 * @file expected_obc_hk.py
 * @author Jenish Patel
 * @date 2022-08-08
'''

expected_OBC_HK = {
    'temparray1': [17, 25], # MCU Temperature
    'OBC_software_ver': [0, 3], # Assumed values for software version but range is likely off
    'temparray2': [17, 25], # Converter Temperature
    'OBC_uptime': [0, 28800], # Uptime, assumed in seconds up to 8 hours
    'SD_usage_1': [0, 80], # Given in percentage, SD card #1
    'SD_usage_2': [0, 80], # Given in percentage, SD card #2
    'boot_cnt': [1, 4294967295], # Boot counter, max 4 bytes
    'last_reset_reason': [0, 4], # Boot reason, 1 byte, only 4 or 5 options
    'last_reset_source': [0, 65535] # Boot source, 2 bytes, lots of options
}

expected_OBC_HK_old = {
    #'temparray1': [17, 25],
    'temparray2': [17, 25],
    'boot_cnt': [1, 4294967295],#max 4 bytes
    'last_reset_reason': [0, 4],
    'OBC_mode': [0, 256],#max byte
    'OBC_uptime': [0, 28800], # Uptime, assumed in seconds up to 8 hours
    'solar_panel_supply_curr': [0, 256],#max byte
    'OBC_software_ver': [0, 3],
    'cmds_received': [1, 4294967295],#max 4 bytes
    'pckts_uncovered_by_FEC': [1, 4294967295],#max 4 bytes
}