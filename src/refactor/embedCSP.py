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

class EmbedPacket:
    def __init__(self, commandList, data):
        self.inputParse = InputParser()
        self.data = data
        self.cmdList = commandList
        self.schedule = list()

    def embedCSP(self):
        self._buildCommandList()
        self._buildEmbeddedPacket()
        return self.data

    def _buildCommandList(self):
        if len(self.cmdList) > 0:
            for i in range(0, len(self.cmdList)):
                # parse the time and command, then embed the command as a CSP packet
                cmdStart = re.search(r'[a-z]', self.cmdList[i], re.I)
                if cmdStart is not None:
                    cmdStart = cmdStart.start()
                scheduledTime = self.cmdList[i][:cmdStart]
                scheduledTime = " ".join(scheduledTime.strip().split())
                ascii_values = [ord(character) for character in scheduledTime]
                scheduledCmd = self.cmdList[i][cmdStart:]

                command = self.inputParse.parseInput(scheduledCmd)
                command['time'] = ascii_values
                # append the list
                print("Command: {}".format(command))
                self.schedule.append(command)

    def _buildEmbeddedPacket(self):
        for cmd in self.schedule:
            # for each line of command, parse the packet
            scheduledTime = cmd['time']
            scheduledDst = cmd['dst']
            dst = (scheduledDst).to_bytes(1, byteorder='big')
            scheduledDport = cmd['dport']
            dport = (scheduledDport).to_bytes(1, byteorder='big')
            packetContent = cmd['args']
            self.data.extend(scheduledTime)
            self.data.extend(dst)
            self.data.extend(dport)
            self.data.extend((len(packetContent)).to_bytes(2, byteorder='big'))
            self.data.extend(packetContent)


if __name__ == "__main__":
    commandList = ["0        50      1     7   4       5        5    52     ex2.time_management.get_time()"]
    parser = InputParser()
    command = "EX2.SCHEDULER.SET_SCHEDULE()"
    commandDict = parser.parseInput(command)
    embedObj = EmbedPacket(commandList, commandDict['args'])
    print(embedObj.embedCSP())
