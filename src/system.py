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
                            'args': None, # SID
                            'returns': {
                                'err': '>b',
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
	    'COMMUNICATION': {
		'port': 10,
		'subservice': {
		    'GET_TEMP': {
			'subPort': 0,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'temperature': '>u4',
                            }
                        }
                    }
		}
	    },

            'HOUSEKEEPING': {
                'port': 9,
                'subservice': {
                    'PARAMETER_REPORT': {
                        'subPort': 0,
                        'inoutInfo': {
                            'args': ['>B'],
                            'returns': {
                                'structureID': '>B',
                                'temp': '>f4',
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
                    },
                    'EPS_HARD_RESET': {
                        'subPort': 2,
                        'inoutInfo': {
                            'args': ['>u2'], # 17767
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    # Note: soft reset is done VIA CSP services - refer to docs
                    'PAUSE_EPS_DEPLOYMENT_ACTION': {
                        'subPort': 8,
                        'inoutInfo': {
                            'args': ['>B', '>u4'], # group, time
                            'returns': {
                                'err': '>b'
                            }
                        }
                    }
                }
            },

            'CLI': {
                # EPS SPECIFIC
                'port': 13, # EPS remote CLI uses port 13 unless Otherwise specified
                'subservice': {
                    'GENERAL_TELEMETERY': {
                        'subPort': 0,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'timestamp': '>u4',
                                'uptimeInS': '>f8',
                                'gs_wdt_time_left_s': '>u4',
                                'counter_wdt_gs': '>u4',
                                'mpptConverterVoltage0_mV': '>u2',
                                'mpptConverterVoltage1_mV': '>u2',
                                'mpptConverterVoltage2_mV': '>u2',
                                'mpptConverterVoltage3_mV': '>u2',
                                'curSolarPanels0_mA': '>u2',
                                'curSolarPanels1_mA': '>u2',
                                'curSolarPanels2_mA': '>u2',
                                'curSolarPanels3_mA': '>u2',
                                'curSolarPanels4_mA': '>u2',
                                'curSolarPanels5_mA': '>u2',
                                'curSolarPanels6_mA': '>u2',
                                'curSolarPanels7_mA': '>u2',
                                'vBatt_mV': '>u2',
                                'curSolar_mA': '>u2',
                                'curBattIn_mA': '>u2',
                                'curBattOut_mA': '>u2',
                                'curOutput0_mA': '>u2',
                                'curOutput1_mA': '>u2',
                                'curOutput2_mA': '>u2',
                                'curOutput3_mA': '>u2',
                                'curOutput4_mA': '>u2',
                                'curOutput5_mA': '>u2',
                                'curOutput6_mA': '>u2',
                                'curOutput7_mA': '>u2',
                                'curOutput8_mA': '>u2',
                                'curOutput9_mA': '>u2',
                                'curOutput10_mA': '>u2',
                                'curOutput11_mA': '>u2',
                                'curOutput12_mA': '>u2',
                                'curOutput13_mA': '>u2',
                                'curOutput14_mA': '>u2',
                                'curOutput15_mA': '>u2',
                                'curOutput16_mA': '>u2',
                                'curOutput17_mA': '>u2',
                                'AOcurOutput0_mA': '>u2',
                                'AOcurOutput1_mA': '>u2',
                                'outputConverterVoltage0': '>u2',
                                'outputConverterVoltage1': '>u2',
                                'outputConverterVoltage2': '>u2',
                                'outputConverterVoltage3': '>u2',
                                'outputConverterVoltage4': '>u2',
                                'outputConverterVoltage5': '>u2',
                                'outputConverterVoltage6': '>u2',
                                'outputConverterVoltage7': '>u2',
                                'outputConverterState': '>B', # 4 bits!
                                'outputStatus': '>u4',
                                'outputFaultStatus': '>u4',
                                'outputOnDelta0': '>u2',
                                'outputOnDelta1': '>u2',
                                'outputOnDelta2': '>u2',
                                'outputOnDelta3': '>u2',
                                'outputOnDelta4': '>u2',
                                'outputOnDelta5': '>u2',
                                'outputOnDelta6': '>u2',
                                'outputOnDelta7': '>u2',
                                'outputOnDelta8': '>u2',
                                'outputOnDelta9': '>u2',
                                'outputOnDelta10': '>u2',
                                'outputOnDelta11': '>u2',
                                'outputOnDelta12': '>u2',
                                'outputOnDelta13': '>u2',
                                'outputOnDelta14': '>u2',
                                'outputOnDelta15': '>u2',
                                'outputOnDelta16': '>u2',
                                'outputOnDelta17': '>u2',
                                'outputOffDelta0': '>u2',
                                'outputOffDelta1': '>u2',
                                'outputOffDelta2': '>u2',
                                'outputOffDelta3': '>u2',
                                'outputOffDelta4': '>u2',
                                'outputOffDelta5': '>u2',
                                'outputOffDelta6': '>u2',
                                'outputOffDelta7': '>u2',
                                'outputOffDelta8': '>u2',
                                'outputOffDelta9': '>u2',
                                'outputOffDelta10': '>u2',
                                'outputOffDelta11': '>u2',
                                'outputOffDelta12': '>u2',
                                'outputOffDelta13': '>u2',
                                'outputOffDelta14': '>u2',
                                'outputOffDelta15': '>u2',
                                'outputOffDelta16': '>u2',
                                'outputOffDelta17': '>u2',
                                'outputFaultCount0': '>u2',
                                'outputFaultCount1': '>u2',
                                'outputFaultCount2': '>u2',
                                'outputFaultCount3': '>u2',
                                'outputFaultCount4': '>u2',
                                'outputFaultCount5': '>u2',
                                'outputFaultCount6': '>u2',
                                'outputFaultCount7': '>u2',
                                'outputFaultCount8': '>u2',
                                'outputFaultCount9': '>u2',
                                'outputFaultCount10': '>u2',
                                'outputFaultCount11': '>u2',
                                'outputFaultCount12': '>u2',
                                'outputFaultCount13': '>u2',
                                'outputFaultCount14': '>u2',
                                'outputFaultCount15': '>u2',
                                'outputFaultCount16': '>u2',
                                'outputFaultCount17': '>u2',
                                'temp0_c': '>b',
                                'temp1_c': '>b',
                                'temp2_c': '>b',
                                'temp3_c': '>b',
                                'temp4_c': '>b',
                                'temp5_c': '>b',
                                'temp6_c': '>b',
                                'temp7_c': '>b',
                                'temp8_c': '>b',
                                'temp9_c': '>b',
                                'temp10_c': '>b',
                                'temp11_c': '>b',
                                'temp12_c': '>b',
                                'temp13_c': '>b',
                                'battState': '>B',
                                'mpptMode': '>B',
                                'battHeaterMode': '>B',
                                'battHeaterState': '>B'
                            }
                        }
                    },
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

                    ''' POWER OUTPUTS '''
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

                    ''' SOLAR PANEL INPUTS & MPPT '''
                    'SET_SINGLE_MPPT_CONV_V': {
                        'subPort': 2,
                        'inoutInfo': {
                            'args': ['>B', '>u2'], # channel, voltage (mv)
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'SET_ALL_MPPT_CONV_V': {
                        'subPort': 3,
                        'inoutInfo': {
                            'args': ['>u2', '>u2', '>u2', '>u2'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'SET_MODE_MPPT': {
                        'subPort': 4,
                        'inoutInfo': {
                            'args': ['>B'], # Hw, manual, auto, auto w/ timeout
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'SET_AUTO_TIMEOUT_MPPT': {
                        'subPort': 5,
                        'inoutInfo': {
                            'args': ['>u4'], # timeout
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },

                    ''' BATTERY HEATER '''
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
