class SystemValues(object):
    def __init__(self):
        self.APP_DICT = {
            "OBC"   :1,
            "EPS"   :2,
            "ADCS"  :3,
            "COMMS" :4,
            "IAC"   :5,
            "GND"   :6,
            "DBG"   :7,
            "DEMO"  :8,
            "LAST"  :9
        }
        self.SERVICES = {
            "VERIFICATION":         {"port": 8},
            "HK": {
                "port": 9,
                "subservice": {
                    "HK_PARAMETERS_REPORT": 25
                    }
                },
            "EVENT":                {"port": 5},
            "FUNCTION_MANAGEMENT":  {"port": 8},
            "TIME_MANAGEMENT": {
                "port": 9,
                "subservice": {
                    "SET_TIME": 1
                }
            },
            "SCHEDULING": {"port": 11},
            "LARGE_DATA": {"port": 13},
            "MASS_STORAGE": {"port": 15},
            "TEST": {"port": 17},
            "SU_MNLP": {"port": 18},
        }

      
