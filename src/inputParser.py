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
 * @file inputParser.py
 * @author Robert Taylor
 * @date 2022-07-21
'''

from system import getServices, SatelliteNodes, varTypes
import numpy as np

# TODO: rework this whole class

class InputParser:
    def __init__(self):
        self.remotes = SatelliteNodes
        self.appIdx = 0
        self.serviceIdx = 2
        self.subserviceIdx = 4

    def parseInput(self, input : str):
        tokens = self.lexer(input)
        command = {}

        remote = None

        for node in SatelliteNodes:
            if node[1] == tokens[self.appIdx]:
                remote = node
                break
        if remote is None:
            raise ValueError("No such remote or bad format")
        command['dst'] = remote[2]
        services = getServices(remote[0])

        if tokens[self.serviceIdx] in services:
            # Matches <service>
            service = services[tokens[self.serviceIdx]]
            command['dport'] = service['port']
            if 'subservice' not in service:
                # Then there is no subservice, skip to arg check
                if 'inoutInfo' not in service:
                    raise ValueError('No in/out info for service')
                if not self.__argCheck(
                        tokens[(self.serviceIdx + 1)::], service['inoutInfo'], command):
                    return None
            elif tokens[self.serviceIdx + 1] != '.':
                # If there is a subservice, next token must be a '.'
                raise ValueError('Bad format')

        else:
            raise ValueError('No such service')
            return None

        # TODO: what is going on here
        if tokens[self.subserviceIdx] in service['subservice']:
            subservice = service['subservice'][tokens[self.subserviceIdx]]
            command['subservice'] = subservice['subPort']

            if 'inoutInfo' not in subservice:
                raise ValueError('No in/out info for subservice')
            if not self.__argCheck(tokens[(
                    self.subserviceIdx + 1)::], subservice['inoutInfo'], command, subservice['subPort']):
                return None
        else:
            raise ValueError('No such subservice')

        return command

    def lexer(self, input):
        tokenList = []
        splitInput = input.split("(")
        if len(splitInput) > 2 or len(splitInput) == 0:
            raise ValueError("Invalid command string format")
        commandPortion = splitInput[0]
        parametersPortion = None
        try:
            parametersPortion = splitInput[1][0:-1]
        except:
            pass
        
        commandSplit = commandPortion.split(".")
        if len(commandSplit) != 3:
            raise ValueError("Invalid command string format")
        tokenList.append(commandSplit[0].upper())
        #TODO: get rid of these dots
        tokenList.append(".")
        tokenList.append(commandSplit[1].upper())
        tokenList.append(".")        
        tokenList.append(commandSplit[2].upper())

        if (parametersPortion):
            tokenList.append("(")
            for t in parametersPortion.split(","):
                tokenList.append(t);
            tokenList.append(")")
        for i in range(len(tokenList)):
            tokenList[i] = tokenList[i].strip()
        return tokenList

    def __argCheck(self, args, inoutInfo, command, subservice=None):
        # TODO: wtf is this
        outArgs = bytearray()

        if not inoutInfo['args']:
            # Command has no arguments
            if subservice is not None:
                # Commands has no args, but has subservice
                outArgs.extend([subservice])
                command['args'] = outArgs
                return True
            # Otherwise just put an empty byte in there
            command['args'] = []
            return True

        if args[0] != '(' and args[-1] != ')':
            raise ValueError('Bad format')

        args.pop(0)
        args.pop(-1)
        if len(args) != len(inoutInfo['args']):
            raise ValueError('Wrong # of args')
        if subservice is not None:
            outArgs.extend([subservice])
 
        i = 0
        for name, type in inoutInfo['args'].items():
            if type == 'var':
                nparr = np.array([args[i]], dtype=varTypes[outArgs[-1]])
            else:
                nparr = np.array([args[i]], dtype=type)
            outArgs.extend(nparr.tobytes())
            i += 1
        command['args'] = outArgs
        return command

if __name__ == '__main__':
    parser = InputParser()
    cmd1 = parser.parseInput('EX2.TIME_MANAGEMENT.SET_TIME(1598385718)')
    print(cmd1)

    cmd2 = parser.parseInput('YUK.TIME_MANAgemENT.GET_TIME')
    print(cmd2)
