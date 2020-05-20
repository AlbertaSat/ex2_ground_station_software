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
            "VERIFICATION"       :1,
            "HK"                 :3,
            "EVENT"              :5,
            "FUNCTION_MANAGEMENT":8,
            "TIME_MANAGEMENT"    :9,
            "SCHEDULING"         :11,
            "LARGE_DATA"         :13,
            "MASS_STORAGE"       :15,
            "TEST"               :17,
            "SU_MNLP"            :18,
        }
