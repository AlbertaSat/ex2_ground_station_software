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
 * @file expected_charon_hk.py
 * @author Jenish Patel
 * @date 2022-08-08
'''

expected_charon_HK = {
    'crc' : [0, 65535], # GPS CRC, Assuming max 2 bytes
    'temp1' : '>b', # Temperature Sensors 1-8 in deg C
    'temp2' : '>b',
    'temp3' : '>b',
    'temp4' : '>b',
    'temp5' : '>b',
    'temp6' : '>b',
    'temp7' : '>b',
    'temp8' : '>b'   
}