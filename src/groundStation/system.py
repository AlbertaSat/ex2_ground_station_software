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
            'OBC': 1,
            'EPS': 4,  # hard coded by manufacturer
            'ADCS': 2,
            'COMMS': 3,
            'IAC': 5,
            'DBG': 7,
            'GND': 16,
            'DEMO': 30,
            'LAST': 31
        }
        self.SERVICES = {
            'TIME_MANAGEMENT': {
                'port': 8,  # share a port with EPS time service
                # TODO: these need a error response value
                'subservice': {
                    'GET_TIME': {
                        'subPort': 0,
                        'inoutInfo': {
                            'args': None,  # SID
                            'returns': {
                                'err': '>b',
                                'timestamp': '>u4'
                            }
                        }
                    },
                    'SET_TIME': {
                        'subPort': 1,
                        'inoutInfo': {
                            'args': ['>u4'],  # timestamp
                            'returns': {
                                'err': '>b'  # err
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
                            # Same as return (just reserving space)
                            'args': ['>B', '>u4', '>u4', '>u4', '>u4', '>u4', '>u4', '>u4', '>u4'],
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
                    'S_GET_FREQ': {
			'what': 'Gets the S-band frequency (MHz)',
                        'subPort': 1,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'frequency': '>f4',
                            }
                        }
                    },
                    'S_GET_CONTROL': {
			'what': 'Gets the S-band`s power amplifier write status and its mode = {0:configuration, 1: synchronization, 2:data, 3:test data}',
                        'subPort': 2,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'status': '>u1',
                                'mode': '>u1',
                            }
                        }
                    },
                    'S_GET_ENCODER': {
			'what': 'Gets the S-band encoding configuration. mod={0:QPSK, 1:OQPSK}, rate={0:half, 1:full}',
                        'subPort': 3,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'scrambler': '>u1',
                                'filter': '>u1',
                                'modulation': '>u1',
                                'rate': '>u1',
                            }
                        }
                    },
                    'S_GET_PAPOWER': {
			'what': 'Gets the power value of S-band power amplifier',
                        'subPort': 4,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Power Amplifier Power': '>u1',
                            }
                        }
                    },
                    'S_GET_STATUS': {
			'what': 'Checks if the power of S-band power aamplifier is good and if the frequency lock is achieved',
                        'subPort': 5,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'PWRGD': '>u1',
                                'TXL': '>u1',
                            }
                        }
                    },
                    'S_GET_TR': {
			'what': 'S-band Transmit Ready Indicator = {0: >2560B in buffer}',
                        'subPort': 6,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Transmit Ready': '>i4',
                            }
                        }
                    },
                    'S_GET_BUFFER': {
			'what': 'Gets the pointer to the buffer quantity in S-band. Input = {0:Count, 1:Underrun, 2:Overrun}',
                        'subPort': 7,
                        'inoutInfo': {
                            'args': ['>B'],
                            'returns': {
                                'err': '>b',
                                'pointer': '>u2',
                            }
                        }
                    },
                    'S_GET_HK': {
			'what': 'Gets S-band housekeeping info',
                        'subPort': 8,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Output Power': '>f',
                                'Power Amplifier Temperature': '>f',
                                'Top Temperature': '>f',
                                'Bottom Temperature': '>f',
                                'Battery Current': '>f',
                                'Battery Voltage': '>f',
                                'Power Amplifier Current': '>f',
                                'Power Amplifier Voltage': '>f',
                            }
                        }
                    },
                    'S_SOFT_RESET': {
			'what': 'Reset S-band FPGA registers to default',
                        'subPort': 9,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'S_GET_FULL_STATUS': {
			'what': 'A full status of S-band non-configurable parameters',
                        'subPort': 10,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'PWRGD': '>u1',
                                'TXL': '>u1',
                                'Transmit Ready': '>i4',
                                'Buffer Count': '>u2',
                                'Buffer Underrun': '>u2',
                                'Buffer Overrun': '>u2',
                                'Output Power': '>f',
                                'Power Amplifier Temperature': '>f',
                                'Top Temperature': '>f',
                                'Bottom Temperature': '>f',
                                'Battery Current': '>f',
                                'Battery Voltage': '>f',
                                'Power Amplifier Current': '>f',
                                'Power Amplifier Voltage': '>f',
                                'Firmware Version': '>f',
                            }
                        }
                    },
                    'S_SET_FREQ': {
			'what': 'Sets the frequency of S-band (MHz)',
                        'subPort': 11,
                        'inoutInfo': {
                            'args': ['>f'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'S_SET_CONTROL': {
			'what': 'Sets the S-band`s power amplifier write status and its mode = {0:config, 1: synch, 2:data, 3:test data}. Input: 2 binary',
                        'subPort': 12,
                        'inoutInfo': {
                            'args': ['>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'S_SET_ENCODER': {
			'what': 'Sets the S-band encoding configuration. mod={0:QPSK, 1:OQPSK}, rate={0:half, 1:full}. Input: 4 binary',
                        'subPort': 13,
                        'inoutInfo': {
                            'args': ['>u1', '>u1', '>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'S_SET_PAPOWER': {
			'what': 'Sets the power value of S-band power amplifier (24, 26, 28, 30 dBm)',
                        'subPort': 14,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'S_GET_CONFIG': {
			'what': 'A full status of S-band configurable parameters (the ones with set functions)',
                        'subPort': 15,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Frequency': '>f',
                                'Power Amplifier Power': '>u1',
                                'Power Amplifier status': '>u1',
                                'Power Amplifier mode': '>u1',
                                'Encoder scrambler': '>u1',
                                'Encoder filter': '>u1',
                                'Encoder modulation': '>u1',
                                'Encoder rate': '>u1',
                            }
                        }
                    },
                    'S_SET_CONFIG': {
			'what': 'Sets all the 8 S-band configurable parameters (freq PA_power PA_status PA_mode Enc_scrambler Enc_filter Enc_mod Enc_rate)',
                        'subPort': 16,
                        'inoutInfo': {
                            'args': ['>f', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_STATUS_CTRL': {
			'what': 'Sets UHF status control word (12 binary bits)',
                        'subPort': 20,
                        'inoutInfo': {
                            'args': ['>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_FREQ': {
			'what': 'Sets UHF frequency (MHz)',
                        'subPort': 21,
                        'inoutInfo': {
                            'args': ['>u4'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_PIPE_T': {
			'what': 'Sets UHF pipe timeout period',
                        'subPort': 22,
                        'inoutInfo': {
                            'args': ['>u2'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_BEACON_T': {
			'what': 'Sets UHF beacon message transmission period',
                        'subPort': 23,
                        'inoutInfo': {
                            'args': ['>u2'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_AUDIO_T': {
			'what': 'Sets UHF audio beacon period b/w transmissions',
                        'subPort': 24,
                        'inoutInfo': {
                            'args': ['>u2'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_PARAMS': {
			'what': 'Sets UHF freq, pipe_t, beacon_t, audio_t parameters. Input:4',
                        'subPort': 25,
                        'inoutInfo': {
                            'args': ['>u4', '>u2', '>u2', '>u2'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_RESTORE': {
			'what': 'Restore UHF default values',
                        'subPort': 26,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Confirm': '>u1',
                            }
                        }
                    },
                    'UHF_LOW_PWR': {
			'what': 'Puts UHF TRX into low power mode',
                        'subPort': 27,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Status': '>u1',
                            }
                        }
                    },
                    'UHF_SET_DESTINATION': {
			'what': 'Sets UHF destination callsign',
                        'subPort': 28,
                        'inoutInfo': {
                            'args': ['>U6'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_SOURCE': {
			'what': 'Sets UHF source callsign',
                        'subPort': 29,
                        'inoutInfo': {
                            'args': ['>U6'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_MORSE': {
			'what': 'Sets UHF morse code callsign (max 36)',
                        'subPort': 30,
                        'inoutInfo': {
                            'args': ['>U36'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_MIDI': {
			'what': 'Sets UHF MIDI audio beacon (max 36)',
                        'subPort': 31,
                        'inoutInfo': {
                            'args': ['>U36'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_BEACON_MSG': {
			'what': 'Sets UHF beacon message (max 120)',
                        'subPort': 32,
                        'inoutInfo': {
                            'args': ['>u1', '>U36'],  # Switch to 120 after packet configuration
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_I2C': {
			'what': 'Sets UHF I2C address (22 | 23)',
                        'subPort': 33,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_WRITE_FRAM': {
			'what': 'Sets UHF FRAM address and write 16-byte data',
                        'subPort': 34,
                        'inoutInfo': {
                            'args': ['>u4', '>U16'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SECURE': {
			'what': 'Puts UHF TRX into secure mode',
                        'subPort': 35,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Status': '>u1',
                            }
                        }
                    },
                    'UHF_GET_FULL_STAT': {
			'what': 'Returns the fulla status of all the UHF non-configurable parameters',
                        'subPort': 36,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'RFTS': '>u1',
                                'FRAM': '>u1',
                                'SEC': '>u1',
                                'CTS': '>u1',
                                'Boot': '>u1',
                                'Pipe': '>u1',
                                'BCN': '>u1',
                                'Echo': '>u1',
                                'RF Mode1': '>u1',  # Use table 9 to improve
                                'RF Mode2': '>u1',
                                'RF Mode3': '>u1',
                                'Reset': '>u1',
                                'Frequency': '>u4',
                                'PIPE timeout': '>u2',
                                'Beacon period': '>u2',
                                'Audio trans. period': '>u2',
                                'Uptime': '>u4',
                                'Packets out': '>u4',
                                'Packets in': '>u4',
                                'Packets in CRC16': '>u4',
                                'Temperature': '>f',
                                'Low power status': '>u1',
                                'Firmware Version': '>u1',
                                'Payload Size': '>u2',
                                'Secure key': '>u4',
                            }
                        }
                    },
                    'UHF_GET_CALLSIGN': {
			'what': 'Gets UHF destination and source callsign',
                        'subPort': 37,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Destination': '>U6',
                                'Source': '>U6',
                            }
                        }
                    },
                    'UHF_GET_MORSE': {
			'what': 'Gets UHF morse callsign',
                        'subPort': 38,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Morse': '>U36',
                            }
                        }
                    },
                    'UHF_GET_MIDI': {
			'what': 'Gets UHF MIDI audio beacon',
                        'subPort': 39,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'MIDI': '>U36',
                            }
                        }
                    },
                    'UHF_GET_BEACON_MSG': {
			'what': 'Gets the beacon message',
                        'subPort': 40,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Beacon Message': '>U36',  # Switch to 120 after configuration
                            }
                        }
                    },
                    'UHF_GET_FRAM': {
			'what': 'Reads the FRAM data',
                        'subPort': 41,
                        'inoutInfo': {
                            'args': None,  # no address?
                            'returns': {
                                'err': '>b',
                                'FRAM': '>U16',
                            }
                        }
                    },
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
                                'current': '>f4',
                                'voltage': '>f4',
                                'temperature': '>f4',
                            }
                        }
                    }
                }
            },

            'GROUND_STATION_WDT': {
                'port': 16,  # As per EPS docs
                'subservice': {
                    'RESET_WDT': {
                        'subPort': 0,
                        'inoutInfo': {
                            'args': ['>u2'],  # key (see docs)
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
                            'args': ['>u2'],  # 17767
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    # Note: soft reset is done VIA CSP services - refer to docs
                    'PAUSE_EPS_DEPLOYMENT_ACTION': {
                        'subPort': 8,
                        'inoutInfo': {
                            'args': ['>B', '>u4'],  # group, time
                            'returns': {
                                'err': '>b'
                            }
                        }
                    }
                }
            },

            'CLI': {
                # EPS SPECIFIC
                'port': 13,  # EPS remote CLI uses port 13 unless Otherwise specified
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
                                'outputConverterState': '>B',  # 4 bits!
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
                            # magicWord (refer to docs), telem. ID, period
                            # (ms), duration (s)
                            'args': ['>u4', '>B', '>u4', '>u4'],
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
                            # output num., state, delay (s)
                            'args': ['>B', '>B', '>u2'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ALL_OUTPUT_CONTROL': {
                        'subPort': 1,
                        'inoutInfo': {
                            'args': ['>u4'],  # binary 10-bit
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },

                    ''' SOLAR PANEL INPUTS & MPPT '''
                    'SET_SINGLE_MPPT_CONV_V': {
                        'subPort': 2,
                        'inoutInfo': {
                            'args': ['>B', '>u2'],  # channel, voltage (mv)
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
                            # Hw, manual, auto, auto w/ timeout
                            'args': ['>B'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'SET_AUTO_TIMEOUT_MPPT': {
                        'subPort': 5,
                        'inoutInfo': {
                            'args': ['>u4'],  # timeout
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
                            'args': ['>B'],  # Mode (see docs)
                            'returns': {
                                'status': '>b'  # 0 = success
                            }
                        }
                    },
                    'SET_HEATER_STATE': {
                        'what': 'On, or off',
                        'subPort': 7,
                        'inoutInfo': {
                            'args': ['>B', '>u2'],  # state, duration (s)
                            'returns': {
                                'err': '>b'
                            }
                        }
                    }
                }
            }
        }
