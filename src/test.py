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
from groundStation.groundStation import *

opts = options()
csp = groundStation(opts.getOptions())

def sendAndExpect(send, expect):
    server, port, toSend = csp.getInput(inVal = send)
    response = csp.transaction(server, port, toSend)
    testpassed = 'Pass' if response == expect else 'Fail'
    print(' - TEST CASE ' + testpassed + ' -\n\tSent: ' + send +
        '\n\tRecieved: ' + str(response) +
        '\n\tExpected: ' + str(expect) + '\n\n')
    return response == expect

def testAllCommandsToOBC():
    current = int(time.time())
    sendAndExpect('obc.TIME_MANAGEMENT.SET_TIME(' + str(current) + ')', {'err':0})
    sendAndExpect('obc.TIME_MANAGEMENT.get_time', {'err':0, 'timestamp': current})

if __name__ == '__main__':
    for i in range(1, 5000):
        testAllCommandsToOBC()
