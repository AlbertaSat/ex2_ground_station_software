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

import numpy as np
import os

import sys
from os import path
sys.path.append("./test")

from testLib import testLib as test
from testLib import gs

import time
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import calendar

test = test() #call to initialize local test class

class CronTime:
    def __init__(self, dt : datetime):
        self.dt = dt
        self.cron = {}
        self.cron["msec"] = int(dt.microsecond/1000.0)
        self.cron["sec"] = dt.second
        self.cron["min"] = dt.minute
        self.cron["hr"] = dt.hour
        self.cron["day"] = dt.day
        self.cron["mon"] = dt.month
        self.cron["yr"] = dt.year - 1970;

    def _setCron(self, dt : datetime):
        if self.cron["msec"] != '*':
            self.cron["msec"] = int(dt.microsecond/1000.0)
        if self.cron["sec"] != '*':
            self.cron["sec"] = dt.second
        if self.cron["min"] != '*':
            self.cron["min"] = dt.minute
        if self.cron["hr"] != '*':
            self.cron["hr"] = dt.hour
        if self.cron["day"] != '*':
            self.cron["day"] = dt.day
        if self.cron["mon"] != '*':
            self.cron["mon"] = dt.month
        if self.cron["yr"] != '*':
            self.cron["yr"] = dt.year;

    def inc(self, relTime : timedelta):
        self.dt = self.dt + relTime
        self._setCron(self.dt)    

    def __str__(self):
        fmt = ""
        for key in self.cron:
            fmt += "{} ".format(self.cron[key])
        return fmt                

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
    
def test_set_multiple():
    # Set a schedule on the satellite and check that it executes when it is
    # supposed to. This is achieved through several steps:
    # 1. create a schedule
    # 2. use scedhuler.set_schedule to upload the schedule
    # 3. wait until the scheduled task has executed
    # 4. get the satellite log to check that the task was executed
    
    dt = datetime.utcnow()
    now = calendar.timegm(dt.timetuple())
    ctime = CronTime(dt)

    # schedule some tasks to execute up to sleep_time seconds in the future
    sleep_time = 20

    schedFile = "test-schedule.txt"
    with open(schedFile, "w") as f:
        # Note that the tasks are specified out of chronological order
        ctime.inc(timedelta(seconds = sleep_time))
        f.write("{} {}\n".format(ctime, "ex2.time_management.get_time"))
        ctime.inc(timedelta(seconds = sleep_time - 5))
        f.write("{} {}\n".format(ctime, "ex2.time_management.get_time"))
        ctime.inc(timedelta(seconds = sleep_time - 15))
        f.write("{} {}\n".format(ctime, "ex2.time_management.get_time"))
        ctime.inc(timedelta(seconds = sleep_time - 10))
        f.write("{} {}\n".format(ctime, "ex2.time_management.get_time"))

    # Upload the schedule file to the satellite
    cmd = "ex2.scheduler.set_schedule({})".format(schedFile)
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)

    # set the schedule
    response = transactObj.execute() 
    print("set_schedule response: {}".format(response))

    assert response != {}, "set_schedule - no response"
    assert response['err'] == 0, "set_schedule error {}".format(response['err'])

    print("sleeping for {} seconds".format(sleep_time))
    time.sleep(sleep_time)

    # Thes task should have executed now. There are a couple of ways to read
    # the log file, for example, using the cli or the logger. At this moment
    # the cli read command seems to be truncating some lines in the middle of
    # the ~10KB file.
    #cmd = "ex2.cli.send_cmd(15, read syslog.log)"

    # The logger currently gets the first 500 bytes of the log file.
    # Although we will probably change the logger to get the *last* 500 bytes
    # of the file, the checks below are just FYI for now.
    cmd = "ex2.logger.get_file"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute()

    # NB: the line length stuff is to help debug the truncation issues
    longest_len = 0
    log = response['log'].decode()
    # Split the response into lines, then separate out the scheduler related
    # lines. Those lines can be checked to see that the schedule was accepted
    # executed.
    for line in log.split("\n"):
        if len(line) > longest_len:
            longest_len = len(line)
            # print("new longest line {}: {}".format(longest_len, line))
            if line.find("scheduler") != -1:
                # print("line len {}, isprint {}".format(len(line), line.isprintable()))
                print(line)
            if line.find("executed") != -1:
                for field in line.split(","):
                    if field.find("unix") != -1:
                        ut = field.split(" ")
                        print("executed at {}".format(ut))
    # print("longest_len {}".format(longest_len))


def test_scheduler_delete():
    # Set a schedule on the satellite and check that it executes when it is
    # supposed to. This is achieved through several steps:
    # 1. create a schedule
    # 2. use scedhuler.set_schedule to upload the schedule
    # 3. wait until the scheduled task has executed
    # 4. get the satellite log to check that the task was executed
    
    dt = datetime.now(timezone.utc)
    now = calendar.timegm(dt.timetuple())
    ctime = CronTime(dt)

    # schedule some task to execute sleep_time minutes in the future
    sleep_time = 20
    ctime.inc(datetime.timedelta(seconds = sleep_time))

    # The dummy task is to work-around a current bug in the scheduler.
    # Specifically, the scheduler crashes if there is no periodic task.
    dummy = CronTime(dt)
    dummy.cron['mon'] = '*'

    schedFile = "test-schedule.txt"
    with open(schedFile, "w") as f:
        f.write("{} {}\n".format(ctime, "ex2.time_management.get_time"))
        f.write("{} {}\n".format(dummy, "ex2.time_management.get_time"))

    # Upload the schedule file to the satellite
    cmd = "ex2.scheduler.set_schedule({})".format(schedFile)
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)

    # set the schedule
    response = transactObj.execute() 
    print("set_schedule response: {}".format(response))

    assert response != {}, "set_schedule - no response"
    assert response['err'] == 0, "set_schedule error {}".format(response['err'])

    # Note that different things happen if you issue delete before or after the
    # schedule executes.
    sleep_time = 21
    print("sleeping for {} seconds".format(sleep_time))
    time.sleep(sleep_time)

    # Upload the schedule file that is to be deleted to the satellite
    cmd = "ex2.scheduler.delete_schedule({})".format(schedFile)
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)

    response = transactObj.execute() 
    print("delete_schedule response: {}".format(response))
    
    
if __name__ == '__main__':
    test_scheduler_get()
    test_time()
    test_scheduler_set()
    test.summary()
