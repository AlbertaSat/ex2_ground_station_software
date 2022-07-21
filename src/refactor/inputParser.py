from system import services, SatelliteNodes
import re
import numpy as np
from enum import Enum


# TODO: rework this whole class
# TODO: add sat_cli support
# TODO: Remove error prints and use exceptions

class inputParser:
    def __init__(self):
        self.services = services
        self.remotes = SatelliteNodes
        self.appIdx = 0
        self.serviceIdx = 2
        self.subserviceIdx = 4

    def parseInput(self, input : str):
        tokens = self.lexer(input)
        command = {}

        remote = None
        for name, member in SatelliteNodes.__members__.items():
            if name == tokens[self.appIdx]:
                remote = member.value
                break
        if remote is None:
            print('No such remote or bad format')
            return None
        command['dst'] = remote

        # TODO: shift responsibility of format checking to lexer
        if tokens[self.serviceIdx] in self.services:
            # Matches <service>
            service = self.services[tokens[self.serviceIdx]]
            command['dport'] = service['port']
            if 'subservice' not in service:
                # Then there is no subservice, skip to arg check
                if 'inoutInfo' not in service:
                    print('No in/out info for service')
                    return None
                if not self.__argCheck(
                        tokens[(self.serviceIdx + 1)::], service['inoutInfo'], command):
                    return None
            elif tokens[self.serviceIdx + 1] != '.':
                # If there is a subservice, next token must be a '.'
                print('Bad format')
                return None

        else:
            print('No such service')
            return None

        # TODO: wtf is going on here
        if tokens[self.subserviceIdx] in service['subservice']:
            subservice = service['subservice'][tokens[self.subserviceIdx]]
            command['subservice'] = subservice['subPort']

            if 'inoutInfo' not in subservice:
                print('No in/out info for subservice')
                return None
            if not self.__argCheck(tokens[(
                    self.subserviceIdx + 1)::], subservice['inoutInfo'], command, subservice['subPort']):
                return None
        else:
            print('No such subservice')
            return None

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
                    raise NotImplementedError("Variable size arg not implemented")
                else :
                    nparr = np.array([args[i]], dtype=inoutInfo['args'][i])
                outArgs.extend(nparr.tobytes())
        command['args'] = outArgs
        return command

if __name__ == '__main__':
    parser = inputParser()
    cmd1 = parser.parseInput('EX2.TIME_MANAGEMENT.SET_TIME(1598385718)')
    print(cmd1)

    cmd2 = parser.parseInput('YUK.TIME_MANAgemENT.GET_TIME')
    print(cmd2)