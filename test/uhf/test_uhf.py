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
 * @file test_uhf.py
 * @author Andrew Rooney, Arash Yazdani
 * @date 2020-11-20
'''

'''  to run > yarn run:test_uhf -I uart -d /dev/ttyUSB0 '''

import numpy as np

import sys
from os import path
sys.path.append("./test")

from testLib import testLib as test

test = test() #call to initialize local test class



def testAllCommandsToOBC():
    test.sendAndExpect('obc.communication.UHF_SET_SCW(0 1 0 3 0 0 0 0 0 1 0 0)', {
                  'err': 0})  # sometimes it won't reach its subservice!
    test.sendAndExpect('obc.communication.UHF_SET_FREQ(436000000)', {'err': 0})
    test.sendAndExpect('obc.communication.UHF_SET_PIPE_T(30)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_set_beacon_t(89)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_set_audio_t(536)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_low_pwr(1)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_restore(1)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_secure(1)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_get_full_stat', {'err': 0, 'HFXT': 0, 'UartBaud': 1, 'Reset': 0, 'RF Mode': 3, 'Echo': 0, 'BCN': 0, 'PIPE': 0, 'Bootloader': 0, 'CTS': 0, 'SEC': 1, 'FRAM': 0, 'RFTS': 0, 'Frequency': 436000000,
                                                          'PIPE timeout': 30, 'Beacon period': 89, 'Audio trans. period': 536, 'Uptime': 12, 'Packets out': 100, 'Packets in': 70, 'Packets in CRC16': 10, 'Temperature': np.float32(18.4), 'Low power status': 0, 'Payload Size': 127, 'Secure key': 32})
    test.sendAndExpect('obc.communication.uhf_set_source(UX1UHF)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_set_destination(cq12AB)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_get_callsign', {
                  'err': 0, 'Destination': b'CQ12AB', 'Source': b'UX1UHF'})
    test.sendAndExpect(
        'obc.communication.uhf_set_morse(--.|--|..-|.---|.|.-.-|.-..|-.|--..)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_get_morse', {
                  'err': 0, 'Morse': b'--. -- ..- .--- . .-.- .-.. -. --..'})
    # 67H69H71H67H67H69H71H67H71H72H74W71H72H74W
    test.sendAndExpect('obc.communication.uhf_set_midi(M67H69H71H)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_get_midi',
                  {'err': 0, 'MIDI': b'67H69H71H'})
    test.sendAndExpect(
        'obc.communication.uhf_set_beacon_msg(HelloAlbertaSat)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_get_beacon_msg', {
                  'err': 0, 'Beacon Message': b'HELLOALBERTASAT'})
    test.sendAndExpect('obc.communication.uhf_set_pipe', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_set_bcn', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_set_echo', {'err': 0})
    test.sendAndExpect(
        'obc.communication.uhf_set_params(437500000 45 60 70)', {'err': 0})
    test.sendAndExpect('obc.communication.uhf_get_full_stat', {'err': 0, 'HFXT': 0, 'UartBaud': 1, 'Reset': 0, 'RF Mode': 3, 'Echo': 1, 'BCN': 1, 'PIPE': 1, 'Bootloader': 0, 'CTS': 0, 'SEC': 1, 'FRAM': 0, 'RFTS': 0, 'Frequency': 437500000,
                                                          'PIPE timeout': 45, 'Beacon period': 60, 'Audio trans. period': 70, 'Uptime': 12, 'Packets out': 100, 'Packets in': 70, 'Packets in CRC16': 10, 'Temperature': np.float32(18.4), 'Low power status': 0, 'Payload Size': 127, 'Secure key': 32})
    test.sendAndExpect('obc.communication.uhf_set_I2C(23)', {'err': 0})

    test.summary() #call when done to print summary of tests


if __name__ == '__main__':
    testAllCommandsToOBC()
