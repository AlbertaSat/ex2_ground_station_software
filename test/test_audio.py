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

'''  to run > yarn test_scheduler -I uart '''

import libcsp_py3 as libcsp
import numpy as np
import os

import sys
from os import path
sys.path.append("./test")

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
    cmd = "ex2.ns_payload.nv_start(1, 512, VOL0:/barks.mp3)"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute() 
    print("nv_start response: {}".format(response))

    libcsp.set_sdr_rx()
    print("broadcast received");

    cmd = "ex2.ns_payload.nv_stop"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute() 
    print("nv_stop response: {}".format(response))

def test_nv_csp_play():
    cmd = "ex2.ns_payload.nv_start(1, 512, VOL0:/robot.mp3)"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute()
    print("nv_start response: {}".format(response))

    socket = gs.networkManager.socket()
    gs.networkManager.bind(socket, 24);
    gs.networkManager.listen(socket, 5);
    conn = gs.networkManager.accept(socket, 10000);

    done = False
    blksz = 0
    while not done:
        data = gs.networkManager.receive(16, 24, 100000);
        print("NV data: {}".format(data))
        word = data[0:1]
        bs = int.from_bytes(word, "big");
        word = data[2:3]
        cnt = int.from_bytes(word, "big");
        print("data bs {} cnt {}".format(bs, cnt))
        if blksz == 0:
            blksz = bs
        if bs < blksz:
            done = True

    cmd = "ex2.ns_payload.nv_stop"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute() 
    print("nv_stop response: {}".format(response))

    
if __name__ == '__main__':
    test_time()
    test_nv_csp_play()
