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
        self.now = None
        self.listnow = []
        self.repeat = 0

    def _splitdt(self, dt: datetime):
        """Split the fields of a datetime object into a list

        The (ordered) list allows us to refer to datetime fields by position vs
        name. Note that datetime uses microseconds and full years, whereas we
        use milliseconds and (optionally) abbreviated years.
        """

        return [
            dt.microsecond,
            dt.second,
            dt.minute,
            dt.hour,
            dt.day,
            dt.month,
            dt.year,
        ]

    def parseCmdList(self, cmdList = None):
        """Parse all the commands in the list provided.

        If cmdList is provided, it over-rides the one provided in the constructor
        """

        if cmdList:
           self.cmdList = cmdList
        for cron in self.cmdList:
            print(f"cmd: <{cron}>")
            self.repeat = 0
            self.cmds.append(self._parseCmd(cron))

    def _parseWildcard(self, index: int, field: str):
        if self.repeat != 0:
            return self.listnow[index]

        # Limitations: we don't support wildcard milliseconds, and if you
        # specify month as a wildcard we assume all months contain 30 days.
        # If this turns out to be a problem we can figure something out.
        periods = [0, 1, 60, 60*60, 24*60*60, 30*24*60*60, 0]

        first = self.listnow[index]
        slash = field.find('/')
        if slash == -1:
            self.repeat = periods[index]
        else:
            print(f"step in index {index}: {field}")
            step = int(field[slash+1:])
            self.repeat = step*periods[index]
            # To calculate first, move to the next step multiple.
            # For example, if field=7 and step=5, bump field to 10
            rem = first % step
            if rem > 0:
                maxs = [999, 59, 59, 23, 31, 2023]
                print("now[{}]={}, step={}, new={}".format(index, first, step,
                                                           first+step-rem))
                first = first + (step - rem)
                if first > maxs[index]:
                    # The tricky part about bumping a field is that it may
                    # need to wrap and overflow to the next field. And then
                    # the next field could overflow, etc. The most obvious
                    # example is incrementing the seconds field at 23:59:59.
                    print(f"overflow {first}, at index {index}")
                    self.listnow[index] = first
                    for i in range(index,6):
                        if self.listnow[i] > maxs[i]:
                            print("overflow at {}: {}".format(i, self.listnow[i]))
                            self.listnow[i] -= maxs[i] + 1
                            self.listnow[i+1] += 1
                            if i >= 3:
                                print(f"Warning: overflow into day/month {field}")
                    first = self.listnow[index]
        return first
    def parseCmd(self, cronspec: str):
        self.now = datetime.now(timezone.utc)
        self.listnow = self._splitdt(self.now)
        self.repeat = 0

        cmd = {}
        cmdfields = cronspec.split()
        timefields = []
        for i in range(7):
            if cmdfields[i].isnumeric():
                timefields.append(int(cmdfields[i]))
            elif cmdfields[i].find('*') != -1:
                timefields.append(self._parseWildcard(i, cmdfields[i]))
            else:
                print(f"illegal cron specifier: {cmdfields[i]}")
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
        if nextdt < self.now:
            # Particularly for periodic commands, it's possible that first has
            # already passed. For example, for "0 0 */5 * * *" it's possible we
            # calculated first to be 11:05:00, and it's already 11:07:00. Just
            # add the period and we should get 11:10:00.
            print(f"Warning: cron spec {nextdt} < now {self.now}")
            if self.repeat > 0:
                cmd['first'] += self.repeat
                print(
                    f"Adjusting first by {self.repeat} sec to {datetime.fromtimestamp(cmd['first'], timezone.utc)}"
                )

        cmd['repeat'] = self.repeat
        cmd['last'] = 0
        cmd['op'] = " ".join(cmdfields[7:])

        print(f"cmd: {cmd}")
        return cmd
