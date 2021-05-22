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

'''  to run > sudo LD_LIBRARY_PATH=../libcsp/build PYTHONPATH=../libcsp/build python3 src/test_sband.py -I uart -d /dev/ttyUSB0  '''
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
    sendAndExpect('obc.communication.s_set_control(0 0)', {'err': 0})
    sendAndExpect('obc.communication.s_get_control',
                  {'err': 0, 'status': 0, 'mode': 0})
    sendAndExpect('obc.communication.s_get_full_status', {'err': 0, 'PWRGD': 1, 'TXL': 1, 'Transmit Ready': 1, 'Buffer Count': 0, 'Buffer Underrun': 1, 'Buffer Overrun': 2, 'Output Power': np.float32(26), 'Power Amplifier Temperature': np.float32(
        27.3), 'Top Temperature': np.float32(-2.8), 'Bottom Temperature': np.float32(11.7), 'Battery Current': np.float32(95), 'Battery Voltage': np.float32(7.2), 'Power Amplifier Current': np.float32(0.48), 'Power Amplifier Voltage': np.float32(5.1), 'Firmware Version': np.float32(7.14)})
    sendAndExpect('obc.communication.s_set_freq(2250.5)', {'err': 0})
    sendAndExpect('obc.communication.s_get_freq', {
                  'err': 0, 'frequency': np.float32(2250.5)})
    sendAndExpect('obc.communication.s_set_papower(24)', {'err': 0})
    sendAndExpect('obc.communication.s_get_papower', {
                  'err': 0, 'Power Amplifier Power': 24})
    sendAndExpect('obc.communication.s_set_encoder(1 1 0 1)', {'err': 0})
    sendAndExpect('obc.communication.s_get_encoder', {
                  'err': 0, 'scrambler': 1, 'filter': 1, 'modulation': 0, 'rate': 1})
    sendAndExpect('obc.communication.s_get_status',
                  {'err': 0, 'PWRGD': 1, 'TXL': 1})
    sendAndExpect('obc.communication.s_get_TR', {
                  'err': 0, 'Transmit Ready': 1})
    sendAndExpect('obc.communication.s_get_buffer(0)', {'err': 0, 'buffer': 0})
    sendAndExpect('obc.communication.s_get_buffer(1)', {'err': 0, 'buffer': 1})
    sendAndExpect('obc.communication.s_get_buffer(2)', {'err': 0, 'buffer': 2})
    sendAndExpect('obc.communication.s_get_hk', {'err': 0, 'Output Power': np.float32(26), 'Power Amplifier Temperature': np.float32(27.3), 'Top Temperature': np.float32(-2.8), 'Bottom Temperature': np.float32(
        11.7), 'Battery Current': np.float32(95), 'Battery Voltage': np.float32(7.2), 'Power Amplifier Current': np.float32(0.48), 'Power Amplifier Voltage': np.float32(5.1)})
    sendAndExpect(
        'obc.communication.s_set_config(2222.5 28 0 0 1 1 1 0)', {'err': 0})
    sendAndExpect('obc.communication.s_get_config', {'err': 0, 'Frequency': np.float32(2222.5), 'Power Amplifier Power': 28, 'Power Amplifier status': 0,
                                                     'Power Amplifier mode': 0, 'Encoder scrambler': 1, 'Encoder filter': 1, 'Encoder modulation': 1, 'Encoder rate': 0})
    sendAndExpect('obc.communication.s_soft_reset', {'err': 0})


if __name__ == '__main__':
    start = time.time()
    for i in range(0, 1):
        testAllCommandsToOBC()
    delta = time.time() - start
    print("Tests took: " + str(int(delta)))
