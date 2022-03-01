'''  to run > yarn run:test_dfgm -I uart -d /dev/ttyUSB0 '''

import numpy as np

import sys
from os import path
sys.path.append("./test")

from testLib import testLib as test

import time

test = test() #call to initialize local test class

def testAllCommandsToOBC():
    # Basic functionality tests
    test.sendAndExpect('obc.dfgm.dfgm_run(5)', {'err': 0})
    time.sleep(6) # Wait for first command to end
    test.sendAndExpect('obc.dfgm.dfgm_start', {'err': 0})
    time.sleep(5) # Let the DFGM run for a bit, then stop it
    test.sendAndExpect('obc.dfgm.dfgm_stop', {'err': 0})
    test.send('obc.dfgm.dfgm_get_hk')

    # TO DO: Error checking tests
    

    test.summary() #call when done to print summary of tests


if __name__ == '__main__':
    testAllCommandsToOBC()
