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
 * @file test_uhf_hardware.py
 * @author Arash Yazdani
 * @date 2021-08-25
'''

'''  to run > yarn run:test_uhf_hardware -I uart -d /dev/ttyUSB0 '''

''' The goal of this test is to run commands that are safe with the uhf hardware and does not change critical configurations'''

import numpy as np

import sys
from os import path
sys.path.append("./test")

from testLib import testLib as test

test = test() #call to initialize local test class



def testAllCommandsToOBC():
    test.send('obc.communication.uhf_get_full_stat')
    test.sendAndExpect('obc.communication.uhf_set_source(UX1UHF)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_set_destination(cq12AB)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_get_callsign', {
                  'err': 0, 'Destination': b'CQ12AB', 'Source': b'UX1UHF'})
    test.sendAndExpect(
        'obc.communication.uhf_set_morse(--.|--|..-|.---|.|.-.-|.-..|-.|--..)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_get_morse', {
                  'err': 0, 'Morse': b'--. -- ..- .--- . .-.- .-.. -. --..'})
    test.sendAndExpect('obc.communication.uhf_set_midi(M67H69H71H)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_get_midi',
                  {'err': 0, 'MIDI': b'67H69H71H'})
    test.sendAndExpect(
        'obc.communication.uhf_set_beacon_msg(HelloAlbertaSat)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_get_beacon_msg', {
                  'err': 0, 'Beacon Message': b'HELLOALBERTASAT'})
    test.sendAndExpect('obc.communication.uhf_set_bcn', {'err': 0})

    test.summary() #call when done to print summary of tests


if __name__ == '__main__':
    testAllCommandsToOBC()
