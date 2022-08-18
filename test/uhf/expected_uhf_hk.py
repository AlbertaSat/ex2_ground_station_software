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
 * @file expected_uhf_hk.py
 * @author Jenish Patel
 * @date 2022-08-08
'''

expected_UHF_HK = {
    'scw1': [0, 0], # Status control word #1
    'scw2': [3,3],  # Status control word #2
    'scw3': [0, 1],  # Status control word #3
    'scw4': [5, 5],  # Status control word #4
    'scw5': [0, 1],  # Status control word #5
    'scw6': [0, 1],  # Status control word #6
    'scw7': [0, 1],  # Status control word #7
    'scw8': [0, 1],  # Status control word #8
    'scw9': [0, 1],  # Status control word #9
    'scw10': [0, 1],  # Status control word #10
    'scw11': [1, 1],  # Status control word #11
    'scw12': [1, 1],  # Status control word #12
    'freq': [437875000, 437875000], 
    'pipe_t': [0, 255],
    'beacon_t': [1, 65535],
    'audio_t': [0, 65535],
    'uptime': [0, 28800], # Uptime, assumed in seconds up to 8 hours
    'pckts_out': [1, 4294967295], # Packets out, max 4 bytes
    'pckts_in': [1, 4294967295], # Packets in, max 4 bytes
    'pckts_in_crc16': [1, 4294967295], # Packets in with CRC error, max 4 bytes
    'temperature': [17, 25] # Internal temperature
}