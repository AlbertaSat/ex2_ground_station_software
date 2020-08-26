import numpy as np
import re
from system import SystemValues


class CommandParser(object):

    def __init__(self):
        # Contructor
        self.vals = SystemValues()


    ''' PUBLIC METHODS '''
    def parseInputValue(self, input):
        tokens = self.__lexer(input)
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
                if not self.__argCheck(tokens[(self.vals.serviceIdx + 1)::], service['inoutInfo']):
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
            if not self.__argCheck(tokens[(self.vals.subserviceIdx + 1)::], subservice['inoutInfo'], subservice['subPort']):
                return None
        else:
            print('No such subservice')
            return None

        return self._command


    def parseReturnValue(self, src, dst, dport, data, length):
        try:
            sender = [x for x in self.vals.APP_DICT if self.vals.APP_DICT[x] == src][0]
            dest = [x for x in self.vals.APP_DICT if self.vals.APP_DICT[x] == dst][0]
            service = [x for x in self.vals.SERVICES if self.vals.SERVICES[x]['port'] == dport][0]
        except IndexError as e:
            print("ERROR: bad header information")
            return None

        idx = 0
        outputObj = {}
        subservice = {}

        if service and ('subservice' in self.vals.SERVICES[service]) and length > 0:
            subservice = [self.vals.SERVICES[service]['subservice'][x] for x in self.vals.SERVICES[service]['subservice'] if self.vals.SERVICES[service]['subservice'][x]['subPort'] == data[idx]][0]
            idx += 1

        if 'inoutInfo' not in subservice:
            # error: check system SystemValues
            return None

        returns = subservice['inoutInfo']['returns']
        for retVal in returns:
            outputObj[retVal] = np.frombuffer(data, dtype=returns[retVal], count=1, offset=idx)[0]
            idx += np.dtype(returns[retVal]).itemsize

        return outputObj


    ''' PRIVATE METHODS '''
    def __argCheck(self, args, inoutInfo, subservice=None):
        outArgs = bytearray()

        if not inoutInfo['args']:
            # Command has no arguments
            if subservice:
                # Commands has no args, but has subservice
                outArgs.extend([subservice])
                self._command['args'] = outArgs
                return True
            # Otherwise just put an empty byte in there
            self._command['args'] = bytearray([0])
            return True

        if args[0] != '(' and args[-1] != ')':
            print('Bad format')
            return None

        args.pop(0)
        args.pop(-1)
        if len(args) != len(inoutInfo['args']):
            print('Wrong # of args')
            return None
        if subservice:
            outArgs.extend([subservice])

        for i in range(0, len(args)):
            if inoutInfo['args'][i]:
                nparr = np.array([args[i]], dtype=inoutInfo['args'][i])
                outArgs.extend(nparr.tobytes())
        self._command['args'] = outArgs
        return True

    def __lexer(self, input):
        tokenList = []
        tmp = re.split('([a-zA-Z_-]+|[\(\)]|[0-9_.-]*)', input)
        [tokenList.append(x.upper()) for x in tmp if not str(x).strip() == '']
        return tokenList


if __name__ == '__main__':
    parser = CommandParser()
    cmd1 = parser.parseInputValue('OBC.TIME_MANAGEMENT.SET_TIME(1598385718)')
    print(cmd1)
    cmd2 = parser.parseInputValue('OBC.TIME_MANAgemENT.GET_TIME')
    print(cmd2)
    cmd1['args'][0] = 0x02 # change this to 'getTime'
    parser.parseReturnValue(0, 4, 12, cmd1['args'], 5)
