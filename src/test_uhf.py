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
 * @file test.py
 * @author Andrew Rooney
 * @date 2020-11-20
'''

'''  to run > sudo LD_LIBRARY_PATH=../libcsp/build PYTHONPATH=../libcsp/build python3 src/test.py -I uart -d /dev/ttyUSB1  '''
import time
from groundStation import groundStation
import numpy as np

opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())


def sendAndExpect(send, expect):
    server, port, toSend = gs.getInput(inVal=send)
    response = gs.transaction(server, port, toSend)
    testpassed = 'Pass' if response == expect else 'Fail'
    print(' - TEST CASE ' + testpassed + ' -\n\tSent: ' + send +
          '\n\tRecieved: ' + str(response) +
          '\n\tExpected: ' + str(expect) + '\n\n')
    return response == expect


def testAllCommandsToOBC():
    current = int(time.time())
    """sendAndExpect('obc.TIME_MANAGEMENT.SET_TIME(' + str(current) + ')', {'err':0})
    sendAndExpect('obc.TIME_MANAGEMENT.get_time', {'err':0, 'timestamp': current})
    sendAndExpect('obc.housekeeping.parameter_report(0)', {'structureID': 0, 'temp': np.float32(5.34)})
    sendAndExpect('obc.communication.s_SET_control(1 1)', {'err':0})
    sendAndExpect('obc.communication.s_set_freq(1010.101)', {'err':0})
    sendAndExpect('obc.communication.s_get_freq', {'err':0, 'frequency': np.float32(1010.101)})"""
    sendAndExpect('obc.communication.UHF_SET_SCW(0 1 0 3 0 0 0 0 0 1 0 0)', {
                  'err': 0})  # sometimes it won't reach its subservice!
    sendAndExpect('obc.communication.UHF_SET_FREQ(436000000)', {'err': 0})
    sendAndExpect('obc.communication.UHF_SET_PIPE_T(30)', {'err': 0})
    sendAndExpect('obc.communication.uhf_set_beacon_t(89)', {'err': 0})
    sendAndExpect('obc.communication.uhf_set_audio_t(536)', {'err': 0})
    sendAndExpect('obc.communication.uhf_low_pwr(1)', {'err': 0})
    sendAndExpect('obc.communication.uhf_restore(1)', {'err': 0})
    sendAndExpect('obc.communication.uhf_secure(1)', {'err': 0})
    sendAndExpect('obc.communication.uhf_get_full_stat', {'err': 0, 'HFXT': 0, 'UartBaud': 1, 'Reset': 0, 'RF Mode': 3, 'Echo': 0, 'BCN': 0, 'PIPE': 0, 'Bootloader': 0, 'CTS': 0, 'SEC': 1, 'FRAM': 0, 'RFTS': 0, 'Frequency': 436000000,
                                                          'PIPE timeout': 30, 'Beacon period': 89, 'Audio trans. period': 536, 'Uptime': 12, 'Packets out': 100, 'Packets in': 70, 'Packets in CRC16': 10, 'Temperature': np.float32(18.4), 'Low power status': 0, 'Payload Size': 127, 'Secure key': 32})
    sendAndExpect('obc.communication.uhf_set_source(UX1UHF)', {'err': 0})
    sendAndExpect('obc.communication.uhf_set_destination(cq12AB)', {'err': 0})
    sendAndExpect('obc.communication.uhf_get_callsign', {
                  'err': 0, 'Destination': 'CQ12AB', 'Source': 'UX1UHF'})
    sendAndExpect(
        'obc.communication.uhf_set_morse(--.--..-.---..-.-.-..-.--..-..--)', {'err': 0})
    sendAndExpect('obc.communication.uhf_get_morse', {
                  'err': 0, 'Morse': '--.--..-.---..-.-.-..-.--..-..--'})
    # 67H69H71H67H67H69H71H67H71H72H74W71H72H74W
    sendAndExpect('obc.communication.uhf_set_midi(H67H69H71H)', {'err': 0})
    sendAndExpect('obc.communication.uhf_get_midi',
                  {'err': 0, 'MIDI': 'H67H69H71H'})
    sendAndExpect(
        'obc.communication.uhf_set_beacon_msg(HelloAlbertaSat)', {'err': 0})
    sendAndExpect('obc.communication.uhf_get_beacon_msg', {
                  'err': 0, 'Beacon Message': 'HELLOALBERTASAT'})
    #sendAndExpect('obc.communication.uhf_set_beacon_msg(8,MyBeacon)', {'err':0})
    #sendAndExpect('obc.communication.uhf_get_beacon_msg', {'err': 0, 'Beacon Message': 'MYBEACON'})
    sendAndExpect('obc.communication.uhf_set_pipe', {'err': 0})
    sendAndExpect('obc.communication.uhf_set_bcn', {'err': 0})
    sendAndExpect('obc.communication.uhf_set_echo', {'err': 0})
    sendAndExpect(
        'obc.communication.uhf_set_params(437500000 45 60 70)', {'err': 0})
    sendAndExpect('obc.communication.uhf_get_full_stat', {'err': 0, 'HFXT': 0, 'UartBaud': 1, 'Reset': 0, 'RF Mode': 3, 'Echo': 1, 'BCN': 1, 'PIPE': 1, 'Bootloader': 0, 'CTS': 0, 'SEC': 1, 'FRAM': 0, 'RFTS': 0, 'Frequency': 437500000,
                                                          'PIPE timeout': 45, 'Beacon period': 60, 'Audio trans. period': 70, 'Uptime': 12, 'Packets out': 100, 'Packets in': 70, 'Packets in CRC16': 10, 'Temperature': np.float32(18.4), 'Low power status': 0, 'Payload Size': 127, 'Secure key': 32})
    sendAndExpect('obc.communication.uhf_set_I2C(23)', {'err': 0})


if __name__ == '__main__':
    start = time.time()
    for i in range(0, 1):
        testAllCommandsToOBC()
    delta = time.time() - start
    print("Tests took: " + str(int(delta)))
