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

        if tokens[self.vals.appIdx] in self.vals.APP_DICT and tokens[self.vals.appIdx + 1] == ".":
            # Matches <app>.
            self._command['dst'] = self.vals.APP_DICT[tokens[self.vals.appIdx]]
        else:
            print("No such remote or bad format")
            return None

        if tokens[self.vals.serviceIdx] in self.vals.SERVICES:
            # Matches <service>
            service = self.vals.SERVICES[tokens[self.vals.serviceIdx]]
            self._command['dport'] = service['port']

            if "subservice" not in service:
                # Then there is no subservice, skip to arg check
                if "inoutInfo" not in service:
                    print("No in/out info for service")
                    return None
                if not self.__argCheck(tokens[(self.vals.serviceIdx + 1)::], service['inoutInfo']):
                    return None
            elif tokens[self.vals.serviceIdx + 1] != ".":
                # If there is a subservice, next token must be a "."
                print("Bad format")
                return None

        else:
            print("No such service")
            return None

        if tokens[self.vals.subserviceIdx] in service['subservice']:
            subservice = service['subservice'][tokens[self.vals.subserviceIdx]]
            self._command['subservice'] = subservice['subPort']

            if "inoutInfo" not in subservice:
                print("No in/out info for subservice")
                return None
            if not self.__argCheck(tokens[(self.vals.subserviceIdx + 1)::], subservice['inoutInfo'], subservice['subPort']):
                return None
        else:
            print("No such subservice")
            return None

        return self._command


    ''' PRIVATE METHODS '''
    def __argCheck(self, args, inoutInfo, subservice=None):
        outArgs = bytearray()

        if not inoutInfo['args']:
            # Command has no arguments
            if subservice:
                # Commands has no args, but has subservice
                self._command['args'] = outArgs.extend([subservice])
            # Otherwise just put an empty byte in there
            self._command['args'] = bytearray([0])
            return True

        if args[0] != "(" and args[-1] != ")":
            print("Bad format")
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
        tmp = re.split("([a-zA-Z_-]+|[\(\)]|[0-9_.-]*)", input)
        [tokenList.append(x.upper()) for x in tmp if not str(x).strip() == ""]
        return tokenList


if __name__ == "__main__":
    parser = CommandParser()
    cmd = parser.parseInputValue("OBC.TIME_MANAGEMENT.SET_TIME(1234)")
    print(cmd)
    print(len(cmd['args']))
    cmd = parser.parseInputValue("OBC.TIME_MANAgemENT.GET_TIME")
    print(cmd)
