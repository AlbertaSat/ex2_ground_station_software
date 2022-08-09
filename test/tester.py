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
 * @file testLib.py
 * @author Dustin Wagner, Daniel Sacro
 * @date 2021-06-28
'''

'''In addition to sending/receiving CSP packets and formatting test results, the class in this 
file also contains a function that runs the OBC system-wide housekeeping test'''

import numpy as np
import time
import sys
from os import path
sys.path.append("./src")
from groundStation import GroundStation
from options import optionsFactory

class Tester(GroundStation):
    def __init__(self):
        opts = optionsFactory("basic")
        super().__init__(opts.getOptions())

        self.start = time.time()
        self.failed = 0
        self.passed = 0
        
        pass

    def checkModuleHK(self, real_module_HK, expected_module_HK, ignore_params_list=None) -> bool:
        checkPassed = True
        for val in expected_module_HK:
            if ((ignore_params_list is not None) and (val in ignore_params_list)):
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(real_module_HK[val]))
            elif (real_module_HK[val] > (expected_module_HK[val])[1]):
                # Greater than Max
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(real_module_HK[val]) + ' > ' + str(expected_module_HK[val][1]))
            elif (real_module_HK[val] < (expected_module_HK[val])[0]):
                # Less than min
                colour = '\033[91m'  # red
                checkPassed = False
                print(colour + str(val) + ': ' +
                      str(real_module_HK[val]) + ' < ' + str(expected_module_HK[val][0]))
            else:
                colour = '\033[0m'  # white
                print(colour + str(val) + ': ' + str(expected_module_HK[val][0]) + ' <= ' + str(
                    real_module_HK[val]) + ' <= ' + str(expected_module_HK[val][1]))
        return checkPassed

    def sendAndExpect(self, send, expect):
        inStr = self.inputHandler.getInput("to send: ")
        try:
            transactObj = self.interactive.getTransactionObject(inStr, self.networkManager)
            ret = transactObj.execute()
            print()
            if ret == expect:
                testpassed = 'Pass'
                colour = '\033[92m' #green
                self.passed += 1
            else:
                testpassed = 'Fail'
                colour = '\033[91m' #red
                self.failed += 1
            print()

            print(colour + ' - TEST CASE ' + testpassed + ' -\n\tSent: ' + send +
            '\n\tRecieved: ' + str(ret) + '\n\n' + '\033[0m')
        except Exception as e:
            print(e)
            pass

        return ret == expect

    def send(self, send):
        inStr = self.inputHandler.getInput("to send: ")
        try:
            transactObj = self.interactive.getTransactionObject(inStr, self.networkManager)
            ret = transactObj.execute()
            print()
            if ret != {}:
                testpassed = 'Pass'
                colour = '\033[92m' #green
                self.passed += 1
            else:
                testpassed = 'Fail'
                colour = '\033[91m' #red
                self.failed += 1
            print()

            print(colour + ' - TEST CASE ' + testpassed + ' -\n\tSent: ' + send +
            '\n\tRecieved: ' + str(ret) + '\n\n' + '\033[0m')
        except Exception as e:
            print(e)
            pass

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
    
    def sendSatCliCmd(self, gs, cmd):
            server, port, toSend = gs.getInput(cmd, inVal="{}.cli.send_cmd({},{})".format(gs.satellite, len(cmd), cmd))
            gs.transaction(server, port, toSend)
