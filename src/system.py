'''
 * Copyright (C) 2020  University of Alberta
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
'''
'''
 * @file system.py
 * @author Andrew Rooney
 * @date 2020-08-26
'''

'''
Numpy types (> for BE)
'?' boolean

'b' (signed) byte

'B' unsigned byte

'i' (signed) integer

'u' unsigned integer

'f' floating-point

'c' complex-floating point

'm' timedelta

'M' datetime

'O' (Python) objects

'S', 'a' zero-terminated bytes (not recommended)

'U' Unicode string

'V' raw data (void)
'''
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
                'port': 8, # share a port with EPS time service
                # TODO: these need a error response value
                'subservice': {
                    'GET_TIME': {
                        'subPort': 0,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'timestamp': '>u4'
                            }
                        }
                    },
                    'SET_TIME': {
                        'subPort': 1,
                        'inoutInfo': {
                            'args': ['>u4'], # timestamp
                            'returns': {
                                'err': '>b' # err
                            }
                        }
                    },
                    'GET_LAST_PPS_TIME': {
                        'what': 'Get last PPS time (EPS)',
                        'subPort': 2,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'timestampInS': '>u4',
                                'secondFraction': '>u4'
                            }
                        }
                    },
                    'GET_PRECISE_TIME': {
                        'what': 'A command to get precise time (NTP-like format)',
                        'subPort': 3,
                        'inoutInfo': {
                            'args': ['>B', '>u4', '>u4', '>u4', '>u4', '>u4', '>u4', '>u4', '>u4'], # Same as return (just reserving space)
                            'returns': {
                                'err': '>B',
                                'requestTimeInS': '>u4',
                                'requestSecondFraction': '>u4',
                                'receiveTimeInS': '>u4',
                                'receiveSecondFraction': '>u4',
                                'transmitTimeInS': '>u4',
                                'transmitSecondFraction': '>u4',
                                'receptionTimeInS': '>u4',
                                'receptionSecondFraction': '>u4'
                            }
                        }
                    }
                }
            },

            'GROUND_STATION_WDT': {
                'port': 16, # As per EPS docs
                'subservice': {
                    'RESET_WDT': {
                        'subPort': 0,
                        'inoutInfo': {
                            'args': ['>u2'], # key (see docs)
                            'returns': {
                                'err': '>B'
                            }
                        }
                    },
                    'GET_WDT_REMAINING': {
                        'subPort': 1,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>B',
                                'timeLeftInS': '>u4'
                            }
                        }
                    }
                }
            },

            'CLI': {
                # EPS SPECIFIC
                'port': 13, # EPS remote CLI uses port 13 unless Otherwise specified
                'subservice': {
                    # ALL the EPS CLI commands:
                    'SET_TELEMETERY_PERIOD': {
                        'what': 'Set telemetery collection period on EPS',
                        'subPort': 255,
                        'inoutInfo': {
                            'args': ['>u4', '>B', '>u4', '>u4'], # magicWord (refer to docs), telem. ID, period (ms), duration (s)
                            'returns': {
                                'err': '>b'
                            }
                        }
                    }
                }
            },

            'CONTROL': {
                # EPS SPECIFIC
                'port': 14,
                'subservice': {
                    'SINGLE_OUTPUT_CONTROL': {
                        'subPort': 0,
                        'inoutInfo': {
                            'args': ['>B', '>B', '>u2'], # output num., state, delay (s)
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ALL_OUTPUT_CONTROL': {
                        'subPort': 1,
                        'inoutInfo': {
                            'args': ['>u4'], # binary 10-bit
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'SET_HEATER_MODE': {
                        'what': 'Manual, or automatic',
                        'subPort': 6,
                        'inoutInfo': {
                            'args': ['>B'], # Mode (see docs)
                            'returns': {
                                'status': '>b' # 0 = success
                            }
                        }
                    },
                    'SET_HEATER_STATE': {
                        'what': 'On, or off',
                        'subPort': 7,
                        'inoutInfo': {
                            'args': ['>B', '>u2'], # state, duration (s)
                            'returns': {
                                'err': '>b'
                            }
                        }
                    }
                }
            }
        }
