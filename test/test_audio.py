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

import sys
import os
import signal
import subprocess

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
    

def test_nv_sdr_fwd():
    lport = "40000"
    ofile = "nv.sdr.bin"
    ofd = open(ofile, "wb")
    pid = subprocess.Popen(["nc", "-l", lport], stdout=ofd).pid

    cmd = "ex2.ns_payload.nv_start(1, 512, VOL0:/hts1a_c2.bit)"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute() 
    print("nv_start response: {}".format(response))

    gs.networkManager.set_sdr_rx()
    print("transmission complete")

    cmd = "ex2.ns_payload.nv_stop"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute() 
    print("nv_stop response: {}".format(response))

    os.kill(pid, signal.SIGSTOP)
    status = os.stat(ofile)
    assert status.st_size > 0
    print(status)

def test_nv_csp_rcv():
    # Remove the output from the last run, if it exists
    ofile = "nv.c2"
    if os.path.isfile(ofile):
        os.remove(ofile)

    nv = ReceiveNorthernVoices(gs.networkManager)

    cmd = "ex2.ns_payload.nv_start(1, 512, VOL0:/hts1a_c2.bit)"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute()
    assert response['err'] == 0

    pktcnt = nv.receiveFile(ofile, 10000)
    assert pktcnt > 0
    nv.close()

    cmd = "ex2.ns_payload.nv_stop"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute()
    assert response['err'] == 0

def test_nv_csp_fwd():
    nv = ReceiveNorthernVoices(gs.networkManager)

    cmd = "ex2.ns_payload.nv_start(1, 512, VOL0:/hts1a_c2.bit)"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute()
    assert response['err'] == 0

    lport = "41000"
    ofile = "nv.csp.bin"
    ofd = open(ofile, "wb")
    pid = subprocess.Popen(["nc", "-l", lport], stdout=ofd).pid

    pktcnt = nv.receiveStream(int(lport), 10000)
    assert pktcnt > 0

    cmd = "ex2.ns_payload.nv_stop"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute()
    assert response['err'] == 0

    nv.close()
    os.kill(pid, signal.SIGSTOP)
    status = os.stat(ofile)
    print("amt {} size {}".format(pktcnt, status.st_size))
    #assert status.st_size == amt
    
if __name__ == '__main__':
    test_time()
#    test_nv_csp_rcv()
#    test_nv_csp_fwd()
    test_nv_sdr_fwd()
