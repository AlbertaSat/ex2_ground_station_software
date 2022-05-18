'''
 * Copyright (C) 2020  University of Alberta
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
 * @file commandParser.py
 * @author Andrew Rooney
 * @date 2020-08-26
'''


import numpy as np
import re

try: # When running from website
    from ex2_ground_station_software.src.groundStation.system import SystemValues
except ImportError: # When running from this repo's cli
    from groundStation.system import SystemValues


class CommandParser(object):

    def __init__(self):
        # Contructor
        self.vals = SystemValues()

    ''' PUBLIC METHODS '''

    def parseInputValue(self, input):
        tokens = self._lexer(input)
        self._command = {}

        if tokens[self.vals.appIdx] in self.vals.APP_DICT and tokens[self.vals.appIdx + 1] == '.':
            # Matches <app>.
            self._command['dst'] = self.vals.APP_DICT[tokens[self.vals.appIdx]]
        else:
            print('No such remote or bad format')
            return None

        if tokens[self.vals.serviceIdx] in self.vals.SERVICES:
            # Matches <service>
            service = self.vals.SERVICES[tokens[self.vals.serviceIdx]]
            self._command['dport'] = service['port']
            if 'subservice' not in service:
                # Then there is no subservice, skip to arg check
                if 'inoutInfo' not in service:
                    print('No in/out info for service')
                    return None
                if not self.__argCheck(
                        tokens[(self.vals.serviceIdx + 1)::], service['inoutInfo']):
                    return None
            elif tokens[self.vals.serviceIdx + 1] != '.':
                # If there is a subservice, next token must be a '.'
                print('Bad format')
                return None

        else:
            print('No such service')
            return None

        if tokens[self.vals.subserviceIdx] in service['subservice']:
            subservice = service['subservice'][tokens[self.vals.subserviceIdx]]
            self._command['subservice'] = subservice['subPort']

            if 'inoutInfo' not in subservice:
                print('No in/out info for subservice')
                return None
            if not self.__argCheck(tokens[(
                    self.vals.subserviceIdx + 1)::], subservice['inoutInfo'], subservice['subPort']):
                return None
        else:
            print('No such subservice')
            return None

        return self._command

    def parseReturnValue(self, src, dst, dport, data, length):
        try:
            sender = [
                x for x in self.vals.APP_DICT if self.vals.APP_DICT[x] == src][0]
            dest = [
                x for x in self.vals.APP_DICT if self.vals.APP_DICT[x] == dst][0]
            service = [
                x for x in self.vals.SERVICES if self.vals.SERVICES[x]['port'] == dport][0]
        except IndexError as e:
            print("ERROR: bad header information")
            return None

        idx = 0
        outputObj = {}
        subservice = {}

        if service and (
                'subservice' in self.vals.SERVICES[service]) and length > 0:
            subservice = [self.vals.SERVICES[service]['subservice'][x] for x in self.vals.SERVICES[service]
                          ['subservice'] if self.vals.SERVICES[service]['subservice'][x]['subPort'] == data[idx]][0]
            idx += 1

        if 'inoutInfo' not in subservice:
            # error: check system SystemValues
            return None

        returns = subservice['inoutInfo']['returns']
        args = subservice['inoutInfo']['args']
        for retVal in returns:
            if returns[retVal] == 'var':
            #Variable size config return
                outputObj[retVal] = np.frombuffer( data, dtype = self.vals.varTypes[outputObj['type']], count=1, offset=idx)[0]
                return outputObj

            else:
                outputObj[retVal] = np.frombuffer(
                    data, dtype=returns[retVal], count=1, offset=idx)[0]
                idx += np.dtype(returns[retVal]).itemsize

        return outputObj

    ''' PRIVATE METHODS '''

    def __argCheck(self, args, inoutInfo, subservice=None):
        outArgs = bytearray()

        if not inoutInfo['args']:
            # Command has no arguments
            if subservice is not None:
                # Commands has no args, but has subservice
                outArgs.extend([subservice])
                self._command['args'] = outArgs
                return True
            # Otherwise just put an empty byte in there
            self._command['args'] = []
            return True

        if args[0] != '(' and args[-1] != ')':
            print('Bad format')
            return None

        args.pop(0)
        args.pop(-1)
        if len(args) != len(inoutInfo['args']):
            print('Wrong # of args')
            return None
        if subservice is not None:
            outArgs.extend([subservice])

        for i in range(0, len(args)):
            if inoutInfo['args'][i]:
                if inoutInfo['args'][i] == 'var':
                    #Variable size config arg
                    nparr = np.array([args[i]], dtype=self.vals.varTypes[outArgs[-1]])
                else :
                    nparr = np.array([args[i]], dtype=inoutInfo['args'][i])
                outArgs.extend(nparr.tobytes())
        self._command['args'] = outArgs
        return True

    def _lexer(self, input):
        tokenList = []
        # If an old command is not parsed, use '([a-zA-Z_-]+|[\(\)]|[0-9_.-]*)' and make an issue
        tmp = re.split('([-.|]+|[0-9.]+|[a-zA-Z0-9_-]+|[\(\)])', input)
        [tokenList.append(x.upper()) for x in tmp if not (
            str(x).strip() == '' or str(x).strip() == ',')]  # to accept ',' as delimiter
        return tokenList

class cliCommandParser(CommandParser):
    def _lexer(self, input):
        tokenList = []
        middle = input[input.find("(")+1 : input.find(")")]
        beginning = input[0 : input.find("(")]
        tmp = re.split('([.,]|[\(\)])', beginning)
        for x in tmp:
            if not (str(x).strip() == '' or str(x).strip() == ','):
                    tokenList.append(str(x).upper())
        tokenList.append("(")
        for item in middle.split(",", 1):
            tokenList.append(item)
        tokenList.append(")")
        return tokenList


if __name__ == '__main__':
    parser = CommandParser()
    cmd1 = parser.parseInputValue('OBC.TIME_MANAGEMENT.SET_TIME(1598385718)')
    print(cmd1)

    cmd2 = parser.parseInputValue('OBC.TIME_MANAgemENT.GET_TIME')
    print(cmd2)

    returnval = parser.parseReturnValue(0, 16, 8, bytearray(b'\x01\x00'), 2) # ba[0] = 01 (set time)
    print(returnval)

    returnval = parser.parseReturnValue(0, 16, 8, bytearray(b'\x00\x00@\xaa\xe1H@\x06ffA\x90\x14{'), 5) # ba[0] = 00 (set time)
    print(returnval)

    returnval = parser.parseReturnValue(0, 16, 10, bytearray(b'\x01\x00D|\x86w'), 5)
    print(returnval)
