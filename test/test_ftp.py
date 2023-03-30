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
 * @file test_scheduler.py
 * @author Ron Unrau
 * @date
'''

'''  to run > yarn test_scheduler -I uart '''

from datetime import datetime
from datetime import timezone
from datetime import timedelta
import calendar

from src.options import optionsFactory
from src.options import Options
from src.ftp import ftpSender

from testLib import testLib as test
from testLib import gs

test = test() #call to initialize local test class

def test_scheduler_get():
    test.send('ex2.scheduler.get_schedule')

def test_time():
    # Get the current satellite time and adjust it if necessary. By updating
    # the satellite's time subsequent tests can safely use "now" to manage
    # schedules and check results.
    cmd = "ex2.time_management.get_time"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)

    # get the current time as UTC
    dt = datetime.now(timezone.utc)
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
    
def test_ftp_upload():
    opts = optionsFactory("ftp")
    options = "-p README.md -d /dev/ttyUSB0".split()
    ftpRunner = ftpSender(opts.getOptions(argv=options))
    ftpRunner.run()
    
    print("done")

if __name__ == '__main__':
    test_time()
    test_ftp_upload()
