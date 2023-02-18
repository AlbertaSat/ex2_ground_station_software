'''
 * Copyright (C) 2023  University of Alberta
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
 * @file test_audio.py
 * @author Ron Unrau
 * @date
'''

'''  to run > test_audio.py -I sdr -u '''

import sys
from os import path

print(sys.path)

import libcsp_py3 as libcsp
from src.receiveNVoices import ReceiveNorthernVoices

from testLib import testLib as test
from testLib import gs

import time
from datetime import tzinfo, timedelta, datetime
import calendar

test = test() #call to initialize local test class

def test_time():
    # Get the current satellite time and adjust it if necessary. By updating
    # the satellite's time subsequent tests can safely use "now" to manage
    # schedules and check results.
    cmd = "ex2.time_management.get_time"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)

    # get the current time as UTC
    dt = datetime.utcnow()
    now = calendar.timegm(dt.timetuple())

    response = transactObj.execute()
    if response == {} or response['err'] != 0:
        print("get_time error: {}".format(response))
        return

    print("now: {}, sat: {}".format(now, response))
    sat = int(response['timestamp'])
    dt = datetime.fromtimestamp(sat)
    # Arbitrarily decide that a 10 second diference is "close enough"
    if abs(sat - now) < 10:
        print("satellite time {} (delta {})".format(dt, sat - now))
        return

    print("adjusting satellite time {} (delta {})".format(dt, sat - now))

    cmd = "ex2.time_management.set_time({})".format(now)
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    # set the satellite's time to this script's time
    response = transactObj.execute()
    assert response != {}, "set_schedule - no response"
    assert response['err'] == 0
    

def test_nv_sdr_play():
    cmd = "ex2.ns_payload.nv_start(1, 512, VOL0:/hts1a_c2.bit)"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute() 
    print("nv_start response: {}".format(response))

    print("changing SDR RX")
    gs.networkManager.set_sdr_rx()
    print("transmission complete")

    cmd = "ex2.ns_payload.nv_stop"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute() 
    print("nv_stop response: {}".format(response))

def test_nv_csp_play():
    nv = ReceiveNorthernVoices(gs.networkManager)

    cmd = "ex2.ns_payload.nv_start(1, 512, VOL0:/hts1a_c2.bit)"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute()
    assert response['err'] == 0

    amt = nv.receiveFile("nv.c2", 10000)
    assert amt > 0

    cmd = "ex2.ns_payload.nv_stop"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute()
    assert response['err'] == 0
    
if __name__ == '__main__':
    test_time()
    test_nv_csp_play()
#    test_nv_sdr_play()

