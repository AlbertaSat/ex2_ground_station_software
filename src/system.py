class SystemValues(object):
    def __init__(self):
        self.APP_DICT = {
            "OBC"   :0,
            "EPS"   :1,
            "ADCS"  :2,
            "COMMS" :3,
            "IAC"   :5,
            "GND"   :16,
            "DBG"   :7,
            "DEMO"  :30,
            "LAST"  :31
        }
        self.SERVICES = {
            "VERIFICATION": {"port": 1},
            "HK": {"port": 3,
                    "subservice": {
                        "HK_PARAMETERS_REPORT": 25
                    }
            },
            "EVENT": {"port": 5},
            "FUNCTION_MANAGEMENT": {"port": 8},
            "TIME_MANAGEMENT": {
                "port": 12,
                "subservice": {
                    "SET_TIME": 1,
                    "GET_TIME": 2
                }
            },
            "SCHEDULING": {"port": 11},
            "LARGE_DATA": {"port": 13},
            "MASS_STORAGE": {"port": 15},
            "TEST": {"port": 17},
            "SU_MNLP": {"port": 18},
        }

      
