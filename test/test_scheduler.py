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
        self.cron["yr"] = dt.year;

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
    
    dt = datetime.now(timezone.utc)
    task1 = CronTime(dt)
    task2 = CronTime(dt)
    task3 = CronTime(dt)
    task4 = CronTime(dt)

    # schedule some tasks to execute up to sleep_time seconds in the future
    sleep_time = 40

    schedFile = "test-schedule.txt"
    with open(schedFile, "w") as f:
        # Note that the tasks are specified out of chronological order
        task1.inc(timedelta(seconds = sleep_time))
        f.write("{} {}\n".format(task1, "ex2.time_management.get_time"))
        task2.inc(timedelta(seconds = sleep_time - 10))
        f.write("{} {}\n".format(task2, "ex2.time_management.get_time"))
        task3.inc(timedelta(seconds = sleep_time - 30))
        f.write("{} {}\n".format(task3, "ex2.time_management.get_time"))
        task4.inc(timedelta(seconds = sleep_time - 20))
        f.write("{} {}\n".format(task4, "ex2.time_management.get_time"))

    # Upload the schedule file to the satellite
    cmd = "ex2.scheduler.set_schedule({})".format(schedFile)
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)

    # set the schedule
    response = transactObj.execute() 
    print("set_schedule response: {}".format(response))

    assert response != {}, "set_schedule - no response"
    assert response['err'] == 0, "set_schedule error {}".format(response['err'])

    cmds = get_schedule()
    for c in cmds:
        cmd_dt = datetime.fromtimestamp(c['next'], timezone.utc)
        diff = cmd_dt - dt
        print("next: {} ({}), diff {}".format(cmd_dt, c['next'], diff.total_seconds()))

    print("sleeping for {} seconds".format(sleep_time))
    time.sleep(sleep_time*2)

    # Thes task should have executed now. There are a couple of ways to read
    # the log file, for example, using the cli or the logger. At this moment
    # the cli read command seems to be truncating some lines in the middle of
    # the ~10KB file.
    #cmd = "ex2.cli.send_cmd(15, read syslog.log)"

    cmd = "ex2.logger.get_file"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute()

    log = response['log'].decode()
    # Split the response into lines, then separate out the scheduler related
    # lines. Those lines can be checked to see that the schedule was accepted
    # and executed.
    i = 0
    for line in log.split("\n"):
        print(line)
        if line.find("get_time") != -1:
            fields = line.split(":")
            timestamp = int(fields[1].strip())
            print("executed at {} vs desired {}".format(timestamp, cmds[i]['next']))
            i = i+1
    # print("longest_len {}".format(longest_len))


def test_set_periodic():
    # Set a schedule on the satellite and check that it executes when it is
    # supposed to. This is achieved through several steps:
    # 1. create a schedule
    # 2. use scedhuler.set_schedule to upload the schedule
    # 3. wait until the scheduled task has executed
    # 4. get the satellite log to check that the task was executed
    
    dt = datetime.now(timezone.utc)
    task1 = CronTime(dt)
    task2 = CronTime(dt)

    task1.cron['sec'] = 0
    task1.cron['min'] = "*"  # Should make task1 run every 60 seconds
    task1.cron['hr'] = "*"
    task2.cron['sec'] = "*/20"  # Should make task2 run every 20 seconds
    task2.cron['min'] = "*"
    task2.cron['hr'] = "*"

    # schedule some tasks to execute up to sleep_time seconds in the future
    sleep_time = 120

    schedFile = "periodic-schedule.txt"
    with open(schedFile, "w") as f:
        f.write("{} {}\n".format(task1, "ex2.time_management.get_time"))
        f.write("{} {}\n".format(task2, "ex2.time_management.get_time"))

    # Upload the schedule file to the satellite
    cmd = "ex2.scheduler.set_schedule({})".format(schedFile)
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    # set the schedule
    response = transactObj.execute() 
    print("set_schedule response: {}".format(response))

    assert response != {}, "set_schedule - no response"
    assert response['err'] == 0, "set_schedule error {}".format(response['err'])

    cmds = get_schedule()
    for c in cmds:
        cmd_dt = datetime.fromtimestamp(c['next'], timezone.utc)
        diff = cmd_dt - dt
        print("next: {} ({}), diff {}".format(cmd_dt, c['next'], diff.total_seconds()))

    print("sleeping for {} seconds".format(sleep_time))
    time.sleep(sleep_time*2)

    cmd = "ex2.logger.get_file"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)
    response = transactObj.execute()

    log = response['log'].decode()
    i = 0
    # Split the response into lines, then separate out the scheduler related
    # lines. Those lines can be checked to see that the schedule was accepted
    # and executed.
    for line in log.split("\n"):
        print(line)
        if line.find("get_time") != -1:
            fields = line.split(":")
            timestamp = int(fields[1].strip())
            print("{}: executed at {}".format(i, timestamp))
            i = i+1

def get_schedule():
    # Retrieve the current schedule from the satellite.
    # Return the parsed response as an array of scheduled commands
    cmd = "ex2.scheduler.get_schedule"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)

    response = transactObj.execute()
    assert(response['err'] == 0)

    count = response['count']
    # print("{} commands scheduled".format(count))

    cmds = []
    if count == 0:
        return None

    for i in range(count):
        curr = {}
        offset = i*10  # 10 bytes per cmd scheduled
        curr['next'] = int.from_bytes(response['cmds'][offset:offset+4], byteorder='big')
        offset += 4
        curr['freq'] = int.from_bytes(response['cmds'][offset:offset+4], byteorder='big')
        offset += 4
        curr['dst'] = response['cmds'][offset]
        curr['dport'] = response['cmds'][offset+1]
        cmds.append(curr)

    print(cmds)
    return cmds


def test_scheduler_delete():
    # Send the delete schedule command. It shouldn't matter if there is a
    # schedule present or not.
    cmd = "ex2.scheduler.delete_schedule"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)

    response = transactObj.execute()
    print("delete_schedule response: {}".format(response))

    # Send the delete schedule command. It shouldn't matter if there is a
    # schedule present or not.
    cmd = "ex2.scheduler.get_schedule"
    transactObj = gs.interactive.getTransactionObject(cmd, gs.networkManager)

    response = transactObj.execute()
    assert(response['err'] == 0)
    assert(response['count'] == 0)
    
if __name__ == '__main__':
    test_time()
    test_set_multiple()
    test_set_periodic()
    test_scheduler_delete()
