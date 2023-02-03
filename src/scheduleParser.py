'''
 * Copyright (C) 2022  University of Alberta
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
 * @file scheduleParser.py
 * @author Ron Unrau
 * @date 2023-02-01
'''
from datetime import datetime
from datetime import timezone
import calendar

class ScheduleParser:
    """A class that contains methods to parse an AlbertaSat schedule.

    An AlbertaSat schedule is based loosely on crontab(5). A schedule comprises
    multiple commands, where each command is of the form "<cron spec> <task>".
    A <cron spec> has time fields of the form "msec sec min hr day mo yr", where
    each time field (except milliseonds) is allowed to contain a wildcard.
    Wildcards can be '*', which means repeat every unit (sec, min, etc) or 
    '*/<step>', which means repeat every <step> units. A <cron spec> is parsed
    into a (first, repeat, last) tuple, which effectively say "run this <task>
    at time <first>, and every <repeat> seconds until <last>. The three times
    are given as Unix UTC timestamps.
    """

    def __init__(self, cmdList = None):
        self.cmdList = cmdList
        self.cmds = []
        self.now = []
        self.repeat = 0

    def _splitdt(self, dt: datetime):
        """Split the fields of a datetime object into a list

        The (ordered) list allows us to refer to datetime fields by position vs
        name. Note that datetime uses microseconds and full years, whereas we
        use milliseconds and (optionally) abbreviated years.
        """

        listdt = []
        listdt.append(dt.microsecond)
        listdt.append(dt.second)
        listdt.append(dt.minute)
        listdt.append(dt.hour)
        listdt.append(dt.day)
        listdt.append(dt.month)
        listdt.append(dt.year)
        return listdt

    def parseCmdList(self, cmdList = None):
        """Parse all the commands in the list provided.

        If cmdList is provided, it over-rides the one provided in the constructor
        """

        if cmdList:
           self.cmdList = cmdList
        for cron in self.cmdList:
            print("cmd: <{}>".format(cron))
            self.repeat = 0
            self.cmds.append(self._parseCmd(cron))

    def _parseWildcard(self, index: int, field: str):
        if not self.now:
            # lazy initialization
            self.now = datetime.now(timezone.utc)
            listnow = self._splitdt(self.now)

        if self.repeat != 0:
            return listnow[index]

        # Limitations: we don't support wildcard milliseconds, and if you
        # specify month as a wildcard we assume all months contain 30 days.
        # If this turns out to be a problem we can figure something out.
        periods = [0, 1, 60, 60*60, 24*60*60, 30*24*60*60, 0]

        slash = field.find('/')
        if slash == -1:
            self.repeat = periods[index]
        else:
            self.repeat = int(field[slash+1:])*periods[index]

        return listnow[index]

    def parseCmd(self, cronspec: str):
        cmd = {}
        cmdfields = cronspec.split()
        timefields = []
        for i in range(7):
            if cmdfields[i].isnumeric():
                timefields.append(int(cmdfields[i]))
            elif cmdfields[i].find('*') != -1:
                timefields.append(self._parseWildcard(i, cmdfields[i]))
            else:
                print("illegal cron specifier: {}".format(cmdfields[i]))
                timefields.append(0)

        if timefields[6] < 2000:  # support years as 2023 or 23
            timefields[6] += 2000

        # Create a datetime object to hold the first/next scheduled time
        # Note the constructor throws a value exception if any of the fields are
        # out of legal range (including 0 for day, month, and year)
        nextdt = datetime(timefields[6], timefields[5], timefields[4],
                               hour=timefields[3], minute=timefields[2],
                               second=timefields[1],
                               microsecond=timefields[0]*1000,
                               tzinfo=timezone.utc)
        cmd['first'] = calendar.timegm(nextdt.timetuple())
        cmd['repeat'] = self.repeat
        cmd['last'] = 0
        cmd['op'] = " ".join(cmdfields[7:])
        print("cmd: {}".format(cmd))
        return cmd
