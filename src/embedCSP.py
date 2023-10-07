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
 * @file embedCSP.py
 * @author Robert Taylor
 * @date 2022-07-21
'''

import re
from inputParser import InputParser
from scheduleParser import ScheduleParser

class EmbedPacket:
    def __init__(self, commandList, data):
        self.inputParse = InputParser()
        self.schedParse = ScheduleParser()
        self.data = data
        self.cmdList = commandList
        self.cmds = []
        self.schedule = []

    def embedCSP(self):
        self._buildCommandList()
        self._buildEmbeddedPacket()
        return self.data


    def _buildCommandList(self):
        if len(self.cmdList) > 0:
            for i in range(len(self.cmdList)):
                # parse the time and command, then embed the command as a CSP packet
                cmd = self.schedParse.parseCmd(self.cmdList[i])
                command = self.inputParse.parseInput(cmd['op'])
                command['first'] = cmd['first']
                command['repeat'] = cmd['repeat']
                command['last'] = cmd['last']
                # append the list
                print(f"Command: {command}")
                self.schedule.append(command)

    def _buildEmbeddedPacket(self):
        for cmd in self.schedule:
            # for each line of command, place the fields into the CSP packet
            # note that "to_bytes(4, byteorder='big')" == htonl() 
            scheduledTime = cmd['first'].to_bytes(4, byteorder='big')
            self.data.extend(scheduledTime)
            scheduledTime = cmd['repeat'].to_bytes(4, byteorder='big')
            self.data.extend(scheduledTime)
            scheduledTime = cmd['last'].to_bytes(4, byteorder='big')
            self.data.extend(scheduledTime)
            scheduledDst = cmd['dst']
            dst = (scheduledDst).to_bytes(1, byteorder='big')
            self.data.extend(dst)
            scheduledDport = cmd['dport']
            dport = (scheduledDport).to_bytes(1, byteorder='big')
            self.data.extend(dport)
            packetContent = cmd['args']
            oplen = len(packetContent).to_bytes(2, byteorder='big')
            self.data.extend(oplen)
            self.data.extend(packetContent)


if __name__ == "__main__":
    commandList = ["0        50      1     7   4       5        5    52     ex2.time_management.get_time()"]
    parser = InputParser()
    command = "EX2.SCHEDULER.SET_SCHEDULE()"
    commandDict = parser.parseInput(command)
    embedObj = EmbedPacket(commandList, commandDict['args'])
    print(embedObj.embedCSP())
