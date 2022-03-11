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
 * @file test_dfgm.py
 * @author Daniel Sacro
 * @date 2022-3-10
'''
import time
import numpy as np
from testLib import testLib as test

test = test() #call to initialize local test class

def testAllCommandsToOBC():
    # Collect all HK data and ensure that they are all within their expected values

    # Collect and process DFGM data for 10 seconds, then downlink it over SBAND

    # Collect and process DFGM data for 10 seconds, then downlink it over UHF

    test.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
