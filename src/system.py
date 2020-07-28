class SystemValues(object):
    def __init__(self):
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

      
