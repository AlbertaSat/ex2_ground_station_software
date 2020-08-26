import numpy as np

class SystemValues(object):
    def __init__(self):
        self.appIdx = 0
        self.serviceIdx = 2
        self.subserviceIdx = 4

        self.APP_DICT = {
            'OBC'   :0,
            'EPS'   :4, # hard coded by manufacturer
            'ADCS'  :2,
            'COMMS' :3,
            'IAC'   :5,
            'DBG'   :7,
            'GND'   :16,
            'DEMO'  :30,
            'LAST'  :31
        }
        self.SERVICES = {
            'TIME_MANAGEMENT': {
                'port': 12,
                'subservice': {
                    'SET_TIME': {
                        'subPort': 1,
                        'inoutInfo': {
                            'args': ['>u4'], # timestamp
                            'returns': {
                                'time': '>u4'
                            }
                        }
                    },
                    'GET_TIME': {
                        'subPort': 2,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'time': '>u4'
                            }
                        }
                    }
                }
            },

            'EPS_CLI': {
                'port': 13, # EPS remote CLI uses port 13 unless Otherwise specified
            }
        }
