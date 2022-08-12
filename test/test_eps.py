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
 * @file test_eps.py
 * @author Arash Yazdani
 * @date 2021-08-25
'''

'''  to run > yarn run:test_eps -I uart -d /dev/ttyUSB0 '''


import numpy as np
from tester import Tester

tester = Tester() #call to initialize local test class

def testAllCommandsToOBC():
    tester.send('eps.time_management.get_eps_time')
    tester.sendAndExpect('eps.control.single_output_control(10, 1, 0)', {'err': 0}) #Preferably a channe that does not power a subsystem
    tester.send('eps.cli.general_telemetry') # CAUTION: No such subservice
    tester.sendAndExpect('eps.control.single_output_control(10, 0, 0)', {'err': 0})
    tester.sendAndExpect('eps.configuration.get_active_config(0, 0)', {'err': 0, 'type':0, 'Value': 4})
    tester.sendAndExpect('eps.configuration.get_active_config(136, 2)', {'err': 0, 'type':2, 'Value': 500}) #Might change though. Just checking another type
    
    tester.summary() #call when done to print summary of tests

if __name__ == '__main__':
    testAllCommandsToOBC()
