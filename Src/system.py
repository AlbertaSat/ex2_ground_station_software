import numpy as np

class SystemValues(object):
    def __init__(self):
        self.appIdx = 0
        self.serviceIdx = 2
        self.subserviceIdx = 4

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
                            "args": [">u4"], # Big endian (>), unsigned, 4 bytes
                            "returns": {
                                "time": np.uint32
                            }
                        }
                    },
                    "GET_TIME": {
                        "subPort": 2,
                        "inoutInfo": {
                            "args": None,
                            "returns": {
                                "time": np.uint32
                            }
                        }
                    }
                }
            }
        }
