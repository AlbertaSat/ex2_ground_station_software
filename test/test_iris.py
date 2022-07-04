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
 * @file test_iris.py
 * @author Jenish Patel
 * @date 2022-06-21
'''

'''  to run > yarn test_iris -I uart -d /dev/ttyUSB0 '''

import numpy as np

import sys
from os import path
sys.path.append("./test")

from testLib import testLib as test

import time

test = test() #call to initialize local test class

def testAllCommandsToOBC():
    # Basic functionality tests
    test.sendAndExpect('obc.iris.iris_power_on', {'err': 0}) # Turn on Iris
    time.sleep(5)
    test.sendAndExpect('obc.iris.iris_get_hk', {'err': 0}) # Check error status

    # TODO: Populate tests once housekeeping test is completed and verified

    test.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()