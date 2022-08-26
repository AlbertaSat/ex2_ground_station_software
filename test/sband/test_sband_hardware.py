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
 * @author Andrew Rooney, Arash Yazdani
 * @date 2020-11-20
'''

'''  to run > yarn run:test_sband -I uart -d /dev/ttyUSB0 '''

''' The goal of this test is to run commands that are safe with the Sband hardware and does not change critical configurations'''

import numpy as np

import sys
from os import path
sys.path.append("./test")

from groundstation_tester import Tester

tester = Tester() #call to initialize local test class

def testAllCommandsToOBC():
    tester.sendAndExpect('ex2.communication.s_set_control(0 0)', {'err': 0})
    tester.sendAndExpect('ex2.communication.s_get_control',
                  {'err': 0, 'status': 0, 'mode': 0})
    tester.send('ex2.communication.s_get_full_status')
    tester.send('ex2.communication.s_get_freq')
    tester.sendAndExpect('ex2.communication.s_set_papower(24)', {'err': 0})
    tester.sendAndExpect('ex2.communication.s_get_papower', {
                  'err': 0, 'Power Amplifier Power': 24})
    tester.send('ex2.communication.s_get_encoder')
    tester.sendAndExpect('ex2.communication.s_get_buffer(0)', {'err': 0, 'buffer': 0})
    tester.send('ex2.communication.s_get_hk')
    
    tester.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
