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
    test.send('obc.dfgm.dfgm_get_hk') # Update empty HK buffer by turning on DFGM for 1 sec
    time.sleep(2)

    test.sendAndExpect('obc.dfgm.dfgm_run(1)', {'err': 0})
    time.sleep(2)

    test.sendAndExpect('obc.dfgm.dfgm_run(5)', {'err': 0})
    time.sleep(6) 

    test.sendAndExpect('obc.dfgm.dfgm_start', {'err': 0})
    time.sleep(5) # Let DFGM run for a bit

    test.sendAndExpect('obc.dfgm.dfgm_stop', {'err': 0}) # Check if DFGM actually stops

    test.send('obc.dfgm.dfgm_get_hk') # Check if data gets corrupt somehow (temp. should be ~20, not ~65000)


    # Error checking tests
    test.sendAndExpect('obc.dfgm.dfgm_run(2147483648)', {'err': 1}) # Bad param. - Overflow for 32-bit int
    test.sendAndExpect('obc.dfgm.dfgm_run(-1)', {'err': 1}) # Bad param. - Negative runtime
    test.sendAndExpect('obc.dfgm.dfgm_run(0)', {'err': 1}) # Bad param. - Zero runtime

    test.send('obc.dfgm.dfgm_run(100)')
    test.sendAndExpect('obc.dfgm.dfgm_run(1)', {'err': 2}) # Busy - DFGM already running
    test.sendAndExpect('obc.dfgm.dfgm_start', {'err': 2}) # Busy - DFGM already running
    test.send('obc.dfgm.dfgm_get_hk()') # Should not fail
    test.send('obc.dfgm.dfgm_stop', {'err': 0})


    test.summary() #call when done to print summary of tests


if __name__ == '__main__':
    testAllCommandsToOBC()
