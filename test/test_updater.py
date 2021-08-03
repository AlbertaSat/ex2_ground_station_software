'''
 * Copyright (C) 2020  University of Alberta
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
 * @file test_sband.py
 * @author Robert Taylor
 * @date 2020-07-20
'''

'''  to run > yarn run:test_updater -I uart -d /dev/ttyUSB0 '''

import numpy as np
from testLib import testLib as test

test = test() #call to initialize local test class

def testUpdaterCommandsToOBC():
    test.sendAndExpect('obc.updater.erase_app()', {'err': 0})
    test.sendAndExpect('obc.updater.set_app_address(2097152)', {'err': 0})
    test.sendAndExpect('obc.updater.set_app_crc(1234)', {'err': 0})
    test.sendAndExpect('obc.updater.get_app_info()', {'err' : 0, 'exists' : 0, 'size' : 387424, 'addr' : 2097152, 'crc' : 1234})

if __name__ == '__main__':
    testUpdaterCommandsToOBC();