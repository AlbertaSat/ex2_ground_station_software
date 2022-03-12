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
 * @file test_eps_hk_only.py
 * @author Josh Lazaruk
 * @date 2022-02-15
'''

'''  to run > yarn run:test_eps_hk_only -I uart -d /dev/ttyUSB0 '''


import time
import numpy as np
from testLib import testLib as test
test = test()  # call to initialize local test class


def testAllCommandsToOBC():

    i = 0
    while i < 9:
        test.send('eps.time_management.get_eps_time')
        test.send('eps.cli.general_telemetry')
        time.sleep(1800)
        i += 1
    
    test.summary()  # call when done to print summary of tests


if __name__ == '__main__':
    testAllCommandsToOBC()
