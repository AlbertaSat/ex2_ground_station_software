class SystemValues(object):
    def __init__(self):
        self.APP_DICT = {
            "OBC"   :0,
            "EPS"   :1,
            "ADCS"  :2,
            "COMMS" :3,
            "GND"   :16,
            "DEMO"  :30,
            "LAST"  :31
        }
        self.SERVICES = {
            "VERIFICATION":         {"port": 8},
            "HK":                   {"port": 9},
            "EVENT":                {"port": 10},
            "FUNCTION_MANAGEMENT":  {"port": 11},
            "TIME_MANAGEMENT": {
                "port": 12,
                "subservice": {
                    "SET_TIME": 0
                }
            }
        }
