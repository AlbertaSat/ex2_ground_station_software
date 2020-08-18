import numpy as np

class SystemValues(object):
    def __init__(self):
        self._appIdx = 0
        self._serviceIdx = 2
        self._subserviceIdx = 4

        self.APP_DICT = {
            "OBC"   :0,
            "EPS"   :1,
            "ADCS"  :2,
            "COMMS" :3,
            "IAC"   :5,
            "DBG"   :7,
            "GND"   :16,
            "DEMO"  :30,
            "LAST"  :31
        }
        self.SERVICES = {
            "VERIFICATION": {"port": 8},
            "HK": {
                "port": 9,
                "subservice": {
                    "HK_PARAMETERS_REPORT": 0
                }
            },
            "EVENT": {"port": 10},
            "FUNCTION_MANAGEMENT": {"port": 11},
            "TIME_MANAGEMENT": {
                "port": 12,
                "subservice": {
                    "SET_TIME": {
                        "subPort": 1,
                        "inoutInfo": {
                            "args": [">u4"],
                            "returns": {
                                "time": np.uint32
                            }
                        }
                    },
                    "GET_TIME": 2
                }
            }
        }

    def lexer(self, input):
        tokenList = []
        tmp = re.split("([a-zA-Z]+|[\(\)]|[0-9_.-]*)", input)
        [tokenList.append(x) for x in tmp if not str(x).strip() == ""]
        return tokenList


    def parseInputValue(self, tokens):
        command = {}
        if tokens[self._appIdx] in self.APP_DICT and tokens[self._appIdx + 1] == ".":
            # Matches <app>.
            command.dst = self.APP_DICT[tokens[self._appIdx]]
        else:
            print("No such remote or bad format")
            return None

        if tokens[self._serviceIdx] in self.SERVICES:
            # Matches <service>
            service = self.SERVICES[tokens[self._serviceIdx]]
            command.port = service.port
            if "subservice" not in service:
                # Then there is no subservice, skip to arg check
                if "inoutInfo" not in service:
                    print("No in/out info for service")
                    return None
                self.argCheck(tokens[(self._serviceIdx + 1)::], service.inoutInfo)
            elif tokens[self._serviceIdx + 1] != ".":
                # If there is a subservice, next token must be a "."
                print("Bad format")
                return None
        else:
            print("No such service")
            return None

        if tokens[self._subserviceIdx] in self.SERVICES[service].subservice:
            subservice = self.SERVICES[service].subservice[tokens[self._subserviceIdx]]
            command.subservice = subservice.subPort
            if "inoutInfo" not in subservice:
                print("No in/out info for subservice")
                return None
            self.argCheck(tokens[(self._subserviceIdx + 1)::], subservice.inoutInfo, subservice.subPort)
        else:
            print("No such subservice")
            return None

    def argCheck(self, args, inoutInfo, subservice=None):
        outArgs = bytearray()
        if args[0] != "(" and args[-1] != ")":
            print("Bad format")
            return None
        if subservice:
            outArgs.extend([subservice])

        for i in range(1, len(args) - 1):
            if inoutInfo.args[i - 1]:
                nparr = np.array([args[i]], dtype=inoutInfo.args[i - 1])
                outArgs.extend(nparr.tobytes())

        print(outArgs)

if __name__ == "__main__":
    vals = SystemValues()
    vals.parseInputValue(vals.lexer("OBC.TIME_MANAGEMENT.SET_TIME(1234)"))
