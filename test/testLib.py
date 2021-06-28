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
 * @file commandParser.py
 * @author Dustin Wagner
 * @date 2021-06-28
'''

'''This File contains no actual tests. Only a class to send/receive and format results of tests'''

import time
import sys
from os import path
sys.path.append("./src")
from groundStation import groundStation

import numpy as np

opts = groundStation.options()
gs = groundStation.groundStation(opts.getOptions())


class testLib(object):
    def __init__(self):
        self.start = time.time()
        self.failed = 0
        self.passed = 0
        pass

    def sendAndExpect(self, send, expect):
        server, port, toSend = gs.getInput(inVal = send)
        response = gs.transaction(server, port, toSend)
        if response == expect:
            testpassed = 'Pass'
            colour = '\033[92m' #green
            self.passed += 1
        else:
            testpassed = 'Fail'
            colour = '\033[91m' #red
            self.failed += 1

        print(colour + ' - TEST CASE ' + testpassed + ' -\n\tSent: ' + send +
            '\n\tRecieved: ' + str(response) +
            '\n\tExpected: ' + str(expect) + '\n\n' + '\033[0m')
        return response == expect
    
    def summary(self):
        delta = time.time() - self.start
        print('Summary')
        print('\tTests performed: ' + str(self.failed + self.passed))
        print('\tTime taken: '+ str(round(np.float32(delta), 2)) + 's')
        print('\tPassed: ' + str(self.passed) + ', Failed: ' + str(self.failed))
        success = int(self.passed/(self.passed + self.failed) * 100)
        if success == 100:
            colour = '\033[92m' #green
        elif success >= 80:
            colour = '\033[93m' #yellow
        else:
            colour = '\033[91m' #red
        print(colour + '\t' + str(success) + '%' + ' Success\n' + '\033[0m')