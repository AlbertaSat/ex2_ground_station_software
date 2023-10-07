"""
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
"""
"""
 * @file dummyUtils.py
 * @author John Mabanta
 * @date 2022-07-30
"""

import random
from system import services


def generateFakeHKDict():
    """Returns a fake housekeeping dictionary for dummy responses"""
    fake_hk = services["HOUSEKEEPING"]["subservice"]["GET_HK"]["inoutInfo"][
        "returns"
    ].copy()

    fake_string = "Test String!"
    # Replace data types with values
    for key in fake_hk:
        fake_uint = random.randint(0, 255)
        fake_int = random.randint(-128, 127)
        fake_float = random.uniform(-128.0, 127.0)
        if "B" in fake_hk[key] or "u" in fake_hk[key] or "V" in fake_hk[key]:
            fake_hk[key] = fake_uint
        elif "b" in fake_hk[key] or "i" in fake_hk[key]:
            fake_hk[key] = fake_int
        elif "f" in fake_hk[key]:
            fake_hk[key] = fake_float
        elif "U" in fake_hk[key]:
            fake_hk[key] = fake_string
        else:
            raise NotImplementedError("Found data type not accounted for!")

    return fake_hk
