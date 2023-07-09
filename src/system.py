'''
 * Copyright (C) 2022  University of Alberta
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
 * @author Robert Taylor
 * @date 2022-07-21
'''

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

'var' variable-size (non-numpy). Checks the data type from elsewhere
'''


import numpy as np
from enum import Enum

SatelliteNodes = ("OBC", "EX2", 1), ("OBC", "YKS", 2), ("OBC", "ARS", 3), ("EPS", "EX2_EPS", 4), ("EPS", "YKS_EPS", 6), ("EPS", "ARS_EPS", 5)

GroundNodes = ("GND", "UHF", 16), ("GND", "SBAND", 17), ("GND", "PIPE", 24), ("GND", "BEACON", 99)

varTypes = {
    0: '<u1',
    1: '<i1',
    2: '<u2',
    4: '<u4',
    9: '<S16' #Empty means all zero or Use <V16
}

# A: this logic can be improved significantly
def getServices(system):
    """
    For a system in ['OBC', 'EPS', 'GND'], returns a dictionary of
    all services supported by that system.
    """
    outDict = dict()
    for serv in services:
        if system in services[serv]['supports']:
            outDict[serv] = services[serv]
    return outDict

obc_housekeeping = {
    'err': '>b',
    # WARNING: Avoid duplicate names in the return items below!
    #packet meta
    '###############################\r\n'+
    'packet meta\r\n'+
    '###############################\r\n'+
    'final': '<B',
    'UNIXtimestamp': '>u4',
    'dataPosition': '>u2',
    #ADCS
    '###############################\r\n'
    'ADCS\r\n'+
    '###############################\r\n'+
    'Att_Estimate_Mode': '>B',
    'Att_Control_Mode': '>B',
    'Run_Mode': '>B',
    'Flags_arr': '>V52',
    'Longitude': '>f4',
    'Latitude': '>f4',
    'Altitude': '>f4',
    'Estimated_Angular_Rate_X': '>f4',
    'Estimated_Angular_Rate_Y': '>f4',
    'Estimated_Angular_Rate_Z': '>f4',
    'Estimated_Angular_Angle_X': '>f4',
    'Estimated_Angular_Angle_Y': '>f4',
    'Estimated_Angular_Angle_Z': '>f4',
    'Sat_Position_ECI_X': '>f4',
    'Sat_Position_ECI_Y': '>f4',
    'Sat_Position_ECI_Z': '>f4',
    'Sat_Velocity_ECI_X': '>f4',
    'Sat_Velocity_ECI_Y': '>f4',
    'Sat_Velocity_ECI_Z': '>f4',
    'Sat_Position_LLH_X': '>f4',
    'Sat_Position_LLH_Y': '>f4',
    'Sat_Position_LLH_Z': '>f4',
    'ECEF_Position_X': '>i2',
    'ECEF_Position_Y': '>i2',
    'ECEF_Position_Z': '>i2',
    'Coarse_Sun_Vector_X': '>f4',
    'Coarse_Sun_Vector_Y': '>f4',
    'Coarse_Sun_Vector_Z': '>f4',
    'Fine_Sun_Vector_X': '>f4',
    'Fine_Sun_Vector_Y': '>f4',
    'Fine_Sun_Vector_Z': '>f4',
    'Nadir_Vector_X': '>f4',
    'Nadir_Vector_Y': '>f4',
    'Nadir_Vector_Z': '>f4',
    'Wheel_Speed_X': '>f4',
    'Wheel_Speed_Y': '>f4',
    'Wheel_Speed_Z': '>f4',
    'Mag_Field_Vector_X': '>f4',
    'Mag_Field_Vector_Y': '>f4',
    'Mag_Field_Vector_Z': '>f4',
    'TC_num': '>i2',
    'TM_num': '>i2',
    'CommsStat_flags_1': '<B',
    'CommsStat_flags_2': '<B',
    'CommsStat_flags_3': '<B',
    'CommsStat_flags_4': '<B',
    'CommsStat_flags_5': '<B',
    'CommsStat_flags_6': '<B',
    'Wheel1_Current': '>f4',
    'Wheel2_Current': '>f4',
    'Wheel3_Current': '>f4',
    'CubeSense1_Current': '>f4',
    'CubeSense2_Current': '>f4',
    'CubeControl_Current3v3': '>f4',
    'CubeControl_Current5v0': '>f4',
    'CubeStar_Current': '>f4',
    'CubeStar_Temp': '>f4',
    'Magnetorquer_Current': '>f4',
    'MCU_Temp': '>f4',
    'Rate_Sensor_Temp_X': '>i2',
    'Rate_Sensor_Temp_Y': '>i2',
    'Rate_Sensor_Temp_Z': '>i2',
    #Athena
    '###############################\r\n'
    'Athena\r\n'+
    '###############################\r\n'+
    'software_ver_major':'>u2',
    'software_ver_minor':'>u2',
    'software_ver_patch':'>u2',
    'MCU_core_temp': '>i2',
    'converter_temp': '>i2',
    'OBC_uptime': '>u4',
    'vol0_usage_percent': '>u1',
    'vol1_usage_percent': '>u1',
    'boot_cnt': '>u2',
    'boot_src': '>u2',
    'last_reset_reason': '<B',
    'solar_panel_supply_curr': '>u2',
    'cmds_received': '>u2',
    'heap_free' : '>u4',
    'lowest_heap_free': '>u4',

    #EPS (when fetched via hk, these values are BE)
    '###############################\r\n'
    'EPS\r\n'+
    '###############################\r\n'+
    'eps_cmd_hk': '<B',
    'eps_status_hk' : '<b',
    'eps_timestamp_hk': '>f8',
    'eps_uptimeInS_hk': '>u4',
    'eps_bootCnt_hk': '>u4',
    'wdt_gs_time_left_s': '>u4',
    'wdt_gs_counter': '>u4',
    'mpptConverterVoltage1_mV': '>u2',
    'mpptConverterVoltage2_mV': '>u2',
    'mpptConverterVoltage3_mV': '>u2',
    'mpptConverterVoltage4_mV': '>u2',
    'curSolarPanels1_mA': '>u2',
    'curSolarPanels2_mA': '>u2',
    'curSolarPanels3_mA': '>u2',
    'curSolarPanels4_mA': '>u2',
    'curSolarPanels5_mA': '>u2',
    'curSolarPanels6_mA': '>u2',
    'curSolarPanels7_mA': '>u2',
    'curSolarPanels8_mA': '>u2',
    'vBatt_mV': '>u2',
    'curSolar_mA': '>u2',
    'curBattIn_mA': '>u2',
    'curBattOut_mA': '>u2',
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
    'curOutput18_mA': '>u2',
    'AOcurOutput1_mA': '>u2',
    'AOcurOutput2_mA': '>u2',
    'outputConverterVoltage1': '>u2',
    'outputConverterVoltage2': '>u2',
    'outputConverterVoltage3': '>u2',
    'outputConverterVoltage4': '>u2',
    'outputConverterVoltage5': '>u2',
    'outputConverterVoltage6': '>u2',
    'outputConverterVoltage7': '>u2',
    'outputConverterVoltage8': '>u2',
    'outputConverterState': '<B',  # 4 bits!
    'outputStatus': '>u4',
    'outputFaultStatus': '>u4',
    'protectedOutputAccessCnt': '>u2',
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
    'outputOnDelta18': '>u2',
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
    'outputOffDelta18': '>u2',
    'outputFaultCount1': '<B',
    'outputFaultCount2': '<B',
    'outputFaultCount3': '<B',
    'outputFaultCount4': '<B',
    'outputFaultCount5': '<B',
    'outputFaultCount6': '<B',
    'outputFaultCount7': '<B',
    'outputFaultCount8': '<B',
    'outputFaultCount9': '<B',
    'outputFaultCount10': '<B',
    'outputFaultCount11': '<B',
    'outputFaultCount12': '<B',
    'outputFaultCount13': '<B',
    'outputFaultCount14': '<B',
    'outputFaultCount15': '<B',
    'outputFaultCount16': '<B',
    'outputFaultCount17': '<B',
    'outputFaultCount18': '<B',
    'temp1_c': '<b',
    'temp2_c': '<b',
    'temp3_c': '<b',
    'temp4_c': '<b',
    'temp5_c': '<b',
    'temp6_c': '<b',
    'temp7_c': '<b',
    'temp8_c': '<b',
    'temp9_c': '<b',
    'temp10_c': '<b',
    'temp11_c': '<b',
    'temp12_c': '<b',
    'temp13_c': '<b',
    'temp14_c': '<b',
    'battMode': '<B',
    'mpptMode': '<B',
    'battHeaterMode': '<B',
    'battHeaterState': '<B',
    'PingWdt_toggles': '>u2',
    'PingWdt_turnOffs': '<B',
    'thermalProtTemperature_1': '>b',
    'thermalProtTemperature_2': '>b',
    'thermalProtTemperature_3': '>b',
    'thermalProtTemperature_4': '>b',
    'thermalProtTemperature_5': '>b',
    'thermalProtTemperature_6': '>b',
    'thermalProtTemperature_7': '>b',
    'thermalProtTemperature_8': '>b',
    '###############################\r\n'
    'EPS STARTUP\r\n'+
    '###############################\r\n'+
    'eps_cmd_startup': '<B',
    'eps_status_startup': '<b',
    'eps_timestamp_startup': '>f8',
    'last_reset_reason_reg': '>u4',
    'eps_bootCnt_startup': '>u4',
    'FallbackConfigUsed': '<B',
    'rtcInit': '<B',
    'rtcClkSourceLSE': '>B',
    'flashAppInit': '>B',
    'Fram4kPartitionInit': '>b',
    'Fram520kPartitionInit': '>b',
    'intFlashPartitionInit': '>b',
    'fwUpdInit': '>B',
    'FSInit': '>b',
    'FTInit': '>b',
    'supervisorInit': '>b',
    'uart1App': '>B',
    'uart2App': '>B',
    'tmp107Init': '>b',
    #UHF
    '###############################\r\n'
    'UHF\r\n'+
    '###############################\r\n'+
    'scw1': '<B',
    'scw2': '<B',
    'scw3': '<B',
    'scw4': '<B',
    'scw5': '<B',
    'scw6': '<B',
    'scw7': '<B',
    'scw8': '<B',
    'scw9': '<B',
    'scw10': '<B',
    'scw11': '<B',
    'scw12': '<B',
    'U_frequency': '>u4',
    'pipe_t': '>u4',
    'beacon_t': '>u4',
    'audio_t': '>u4',
    'uptime': '>u4',
    'pckts_out': '>u4',
    'pckts_in': '>u4',
    'pckts_in_crc16': '>u4',
    'temperature': '>f4',
    #Sband
    '###############################\r\n'
    'Sband\r\n'+
    '###############################\r\n'+
    'S_mode': '>B',
    'PA_status': '>B',
    'S_frequency_Hz': '>u4',
    'S_scrambler': '>B',
    'S_filter': '>B',
    'S_modulation': '>B',
    'S_data_rate': '>B',
    'S_bit_order': '>B',
    'S_PWRGD': '>B',
    'S_TXL': '>B',
    'Output_Power': '>B',
    'PA_Temp': '>b',
    'Top_Temp': '>b',
    'Bottom_Temp': '>b',
    'Bat_Current_mA': '>u2',
    'Bat_Voltage_mV': '>u2',
    'PA_Current_mA': '>u2',
    'PA_Voltage_mV': '>u2',
    #Hyperion
    '###############################\r\n'
    'Hyperion Panels\r\n'+
    '###############################\r\n'+
    'Nadir_Temp1': '>b',
    'Nadir_Temp_Adc': '>b',
    'Port_Temp1': '>b',
    'Port_Temp2': '>b',
    'Port_Temp3': '>b',
    'Port_Temp_Adc': '>b',
    'Port_Dep_Temp1': '>b',
    'Port_Dep_Temp2': '>b',
    'Port_Dep_Temp3': '>b',
    'Port_Dep_Temp_Adc': '>b',
    'Star_Temp1': '>b',
    'Star_Temp2': '>b',
    'Star_Temp3': '>b',
    'Star_Temp_Adc': '>b',
    'Star_Dep_Temp1': '>b',
    'Star_Dep_Temp2': '>b',
    'Star_Dep_Temp3': '>b',
    'Star_Dep_Temp_Adc': '>b',
    'Zenith_Temp1': '>b',
    'Zenith_Temp2': '>b',
    'Zenith_Temp3': '>b',
    'Zenith_Temp_Adc': '>b',
    'Nadir_Pd1': '>B',
    'Port_Pd1': '>B',
    'Port_Pd2': '>B',
    'Port_Pd3': '>B',
    'Port_Dep_Pd1': '>B',
    'Port_Dep_Pd2': '>B',
    'Port_Dep_Pd3': '>B',
    'Star_Pd1': '>B',
    'Star_Pd2': '>B',
    'Star_Pd3': '>B',
    'Star_Dep_Pd1': '>B',
    'Star_Dep_Pd2': '>B',
    'Star_Dep_Pd3': '>B',
    'Zenith_Pd1': '>B',
    'Zenith_Pd2': '>B',
    'Zenith_Pd3': '>B',
    'Port_Voltage' : '>u2',
    'Port_Dep_Voltage' : '>u2',
    'Star_Voltage' : '>u2',
    'Star_Dep_Voltage' : '>u2',
    'Zenith_Voltage' : '>u2',
    'Port_Current' : '>u2',
    'Port_Dep_Current' : '>u2',
    'Star_Current' : '>u2',
    'Star_Dep_Current' : '>u2',
    'Zenith_Current' : '>u2',
    #Charon
    '###############################\r\n'
    'Charon Interfacing Board\r\n'+
    '###############################\r\n'+
    'gps_crc' : '>u2',
    'charon_temp1' : '>b',
    'charon_temp2' : '>b',
    'charon_temp3' : '>b',
    'charon_temp4' : '>b',
    'charon_temp5' : '>b',
    'charon_temp6' : '>b',
    'charon_temp7' : '>b',
    'charon_temp8' : '>b',
    #DFGM
    '###############################\r\n'
    'DFGM Board\r\n'+
    '###############################\r\n'+
    'Core_Voltage': '>u2',
    'Sensor_Temperature': '>u2',
    'Reference_Temperature': '>u2',
    'Board_Temperature': '>u2',
    'Positive_Rail_Voltage': '>u2',
    'Input_Voltage': '>u2',
    'Reference_Voltage': '>u2',
    'Input_Current': '>u2',
    'Reserved_1': '>u2',
    'Reserved_2': '>u2',
    'Reserved_3': '>u2',
    'Reserved_4': '>u2',
    #Northern SPIRIT Payloads
    '###############################\r\n'
    'Northern SPIRIT\r\n'+
    '###############################\r\n'+
    'ns_temp0': '>i2',
    'ns_temp1': '>i2',
    'ns_temp2': '>i2',
    'ns_temp3': '>i2',
    'eNIM0_lux': '>i2',
    'eNIM1_lux': '>i2',
    'eNIM2_lux': '>i2',
    'eNIM3_lux': '>i2',
    'ram_avail': '>i2',
    'lowest_img_num': '>i2',
    'first_blank_img_num': '>i2',
    #IRIS
    '###############################\r\n'
    'Iris Board\r\n'+
    '###############################\r\n'+
    'VIS_Temperature': '>f4',
    'NIR_Temperature': '>f4',
    'Flash_Temperature': '>f4',
    'Gate_Temperature': '>f4',
    'Image_number': '>u1',
    'Software_Version': '>u1',
    'Error_number': '>u1',
    'MAX_5V_voltage': '>u2',
    'MAX_5V_power': '>u2',
    'MAX_3V_voltage': '>u2',
    'MAX_3V_power': '>u2',
    'MIN_5V_voltage': '>u2',
    'MIN_3V_voltage': '>u2',
}

# A dictionary of all the commands available to the ground-station operators.
# CommandDocs.txt has a more readable version of this dictionary.
services = {
    'CSP': {
        'supports' : ("EPS", "OBC"),
        'port': 1,
        'subservice': {
            'PING': {
                'what': "Do a CSP ping",
                'subPort': 0,
                'inoutInfo':{
                    'args': None,
                    'returns': {
                        'err': '<b'
                    },
                },
            },
        },
    },
    'SCHEDULER': {
        'supports' : ("OBC",),
        'port': 25,
        # TODO: these need a error response value
        'subservice': {
            'SET_SCHEDULE': {
                'what': 'Returns 0 and number of cmds left in the schedule on success. Refer for schedule.h for calloc error code. Refer to rederrno.h for reliance edge error codes',
                'subPort': 0,
                'inoutInfo': {
                    'args': None,  # All scheduled commands should be stored in schedule.txt
                    'returns': {
                        'err': '>b',
                        'count': '>b'  # Returns -1 if an error occurred.
                    }
                }
            },
            'DELETE_SCHEDULE': {
                'what': 'Returns 0 on success. Refer for schedule.h for calloc error code. Refer to rederrno.h for reliance edge error codes',
                'subPort': 3,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'red_errno': '>b'  # RED errno if I/O error occurred
                    }
                }
            },
            'GET_SCHEDULE': {
                'what': 'Returns 0 and number of cmds left in the schedule on success. Refer for schedule.h for calloc error code. Refer to rederrno.h for reliance edge error codes',
                'subPort': 1,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'count': '>b',
                        'cmds': 'var'
                    }
                }
            },
        }
    },
    'SET_PIPE': {
        'supports': ("OBC",),
        'port': 0,
        'subservice' : {
            'UHF_GS_PIPE': {
                'what': 'Testing function to put an EndurSat radio being used as the ground station radio into PIPE mode',
                'subPort': 0,
                'inoutInfo': {
                    'args': None,  # test
                    'returns': {
                        'err': '>b'  # err
                    }
                }
            }
        }

    },
    'TIME_MANAGEMENT': {
        'supports' : ("OBC",),
        'port': 8,
        'subservice': {
            'GET_TIME': {
                'what': 'Get the current unix time on the OBC',
                'subPort': 10,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'timestamp': '>u4'
                    }
                }
            },
            'SET_TIME': {
            'what': 'Set the current unix time on the OBC. Set parameter to 0 to use local unix time',
                'subPort': 11,
                'inoutInfo': {
                    'args': {
                        "Time" : '>u4'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
        }
    },
    'EPS_FIRMWARE': {
        'supports' : ("EPS",),
        'port': 11,
        'subservice' : {
            'START': {
                'What': "Start new update process. New update descriptor is recorded into non-volatile memory. Set fromGoldenStorage to true if forcing to install from the golden image storage, otherwise always equal to false.",
                'subPort': 0,
                'inoutInfo': {
                    'args': {
                        "ImageType" : '<u1',
                        "TargetMcuUid0" : "<u4",
                        "TargetMcuUid1" : "<u4",
                        "TargetMcuUid2" : "<u4",
                        "ImageSize" : "<u4",
                        "fromGoldenStorage" : "<b"
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            "START_FROM_GOLDEN": {
                'What': "Start new update process from the existing golden image expecting imageType to be installed. If expected image type does not match existing golden image - error is returned. Golden image and its descriptor must exist in the file system to be successful.",
                'subPort': 1,
                'inoutInfo': {
                    'args' : {
                        "ImageType" : "<b"
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            "ABORT": {
                'What' : "Abort current update procedure. It deletes the current update descriptor from non-volatile memory.",
                'subPort': 2,
                'inoutInfo': {
                    'args' : None,
                    'returns' : {
                        'err': '>b'
                    }
                }
            },
            "INSTALL": {
                'What': "Execute installation procedure.",
                'subPort': 3,
                'inoutInfo': {
                    'args' : None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            "GET_SYSTEM_INFO": {
                'What': "Get system information including unique subsystem ID and versions of each image.",
                'subPort': 4,
                'inoutInfo': {
                    'args' : None,
                    'returns': {
                        'err': '<b',
                        'imageType': '<b',
                        'mcuUid0': "<u4",
                        'mcuUid1': "<u4",
                        'mcuUid2': "<u4",
                        'versionOfBootloaderL1Major' : '<u2',
                        'versionOfBootloaderL1Minor' : '<u2',
                        'versionOfBootloaderL1Patch' : '<u2',
                        'versionOfBootloaderL2Major' : '<u2',
                        'versionOfBootloaderL2Minor' : '<u2',
                        'versionOfBootloaderL2Patch' : '<u2',
                        'versionOfApplicationL1Major' : '<u2',
                        'versionOfApplicationL1Minor' : '<u2',
                        'versionOfApplicationPatch' : '<u2',
                        'repNameBL1' : 'V32',
                        'gitHashBL1': 'V20',
                        'repNameBL2': 'V32',
                        'gitHashBL2': 'V20',
                        'repNameAPP': 'V32',
                        'gitHashAPP': 'V20'

                    }
                }
            },
            "GET_CURRENT_STATE": {
                'What': "Return the current state of the ongoing update process.",
                'subPort' : 5,
                'inoutInfo' : {
                    'args': None,
                    'returns' : {
                        'err': '<b',
                        'state': '<b'
                    }
                }
            },
            "GET_CURRENT_UPDATE_DESCRIPTOR": {
                'What': "Return the descriptor of current update process, which includes information about what type of update is performed.",
                'subPort' : 6,
                'inoutInfo' : {
                    'args': None,
                    'returns' : {
                        'err': '<b',
                        'imageType': '<b',
                        "TargetMcuUid0" : "<u4",
                        "TargetMcuUid1" : "<u4",
                        "TargetMcuUid2" : "<u4",
                        "ImageSize" : "<u4",
                        "fromGoldenStorage" : "<b"
                    }
                }
            },
            "GET_GOLDEN_UPDATE_DESCRIPTOR": {
                'What': "Return the update descriptor of the golden image.",
                'subPort' : 7,
                'inoutInfo' : {
                    'args': None,
                    'returns' : {
                        'err': '<b',
                        'imageType': '<b',
                        "TargetMcuUid0" : "<u4",
                        "TargetMcuUid1" : "<u4",
                        "TargetMcuUid2" : "<u4",
                        "ImageSize" : "<u4",
                        "fromGoldenStorage" : "<b"
                    }
                }
            },
            "VALIDATE_SIGNATURE": {
                'What': "Perform image integrity check by checking for valid signature. Image size and CRC32 value is returned as a result. In case of invalid image signature, error invalidSignature is returned.",
                'subPort': 8,
                'inoutInfo': {
                    'args': {
                        'imageType': '<b'
                    },
                    'returns': {
                        'err': '<b',
                        'size': '<u4',
                        'crc': '<u4'
                    }
                }
            },
            "ABORT_BOOT": {
                'What': "Abort boot process. Supported only in the bootloader L2 context.",
                'subPort': 9,
                'inoutInfo': {
                    'args' : None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            "GET_GOLDEN_INFO": {
                'What': "Checks if golden image is present and is valid. Returns information of golden image.",
                'subPort': 10,
                'inoutInfo': {
                    'args' : None,
                    'returns': {
                        'err': '<b',
                        'imageType': '<b',
                        'versionMajor': "<u2",
                        'versionMinor': "<u2",
                        'versionPatch': "<u2",
                        'crc': "<u4",
                        'repName': 'V32',
                        'gitHash': 'V20'

                    }
                }
            },
            "SET_SIGNATURE_CHECKING": {
                'What': "Enables or disables signature checking which allows updating firmware with different signature. Set state is kept until reboot. Recommended update sequence: bootloader L1, bootloader L2, application. By default signature checking is enabled. Enable: 1 - enable, 0 - disable. Magic: 0x862A7E01",
                'subPort': 11,
                'inoutInfo': {
                    'args': {
                        'enable': '<b',
                        'magicKey': '<u4'
                    },
                    'returns': {
                        'err': '<b'
                    }
                }
            }
        }
    },
    'GENERAL': {
        'supports' : ("OBC",),
        'port' : 11,
        'subservice' : {
            'REBOOT': {
                'What': "Command OBC to reboot to a given more, B, A, or G for bootloader, application, or golden image respectively",
                'subPort': 0,
                'inoutInfo': {
                    'args': {
                        "Mode" : '>B'
                    },
                    'returns': {
                        'err': '>b'  # err
                    }
                }
            },
            'DEPLOY_DEPLOYABLES': {
                'what': 'Trigger burnwire. DFGM=0, UHF_P=1, UHF_Z=2, UHF_S=3, UHF_N=4. Solar panels: Port=5, Payload=6, Starboard=7. Returns instantaneous current consumption',
                'subPort': 1,
                'inoutInfo': {
                    'args': {
                        "Wire" : '>B'
                    },
                    'returns': {
                        'err': '>b',  # switch status
                        'current_mA': '>u2' # current consumed during burning
                    }
                }
            },
            'GET_SWITCH_STATUS': {
            'what': 'Query the status of all deployment switches. Returns 1 = Deployed, 0 = Undeployed',
                'subPort': 2,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',  # err status
                        'switch_DFGM' : '>b',
                        'switch_UHF_P' : '>b',
                        'switch_UHF_Z' : '>b',
                        'switch_UHF_S' : '>b',
                        'switch_UHF_N' : '>b',
                        'switch_Port' : '>b',
                        'switch_Payload' : '>b',
                        'switch_Starboard' : '>b'
                    }
                }
            },
            'GET_UHF_WATCHDOG_TIMEOUT': {
                'what': 'Get the period (in ticks) of the UHF watchdog timer on the OBC',
                'subPort': 3,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',  # err status
                        'timeout_ms': '>u4'
                    }
                }
            },
            'SET_UHF_WATCHDOG_TIMEOUT': {
                'what': 'Set the period (in ms) of the UHF watchdog timer on the OBC',
                'subPort': 4,
                'inoutInfo': {
                    'args': {
                        "Period" : '>u4'
                    },
                    'returns': {
                        'err': '>b',  # err status
                    }
                }
            },
            'GET_SBAND_WATCHDOG_TIMEOUT': {
                'what': 'Get the period (in ticks) of the S-band watchdog timer on the OBC',
                'subPort': 5,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',  # err status
                        'timeout_ms': '>u4'
                    }
                }
            },
            'SET_SBAND_WATCHDOG_TIMEOUT': {
                'what': 'Set the period (in ms) of the S-band watchdog timer on the OBC',
                'subPort': 6,
                'inoutInfo': {
                    'args': {
                        "Period" : '>u4'
                    },
                    'returns': {
                        'err': '>b',  # err status
                    }
                }
            },
            'GET_CHARON_WATCHDOG_TIMEOUT': {
                'what': 'Get the period (in ticks) of the Charon watchdog timer on the OBC',
                'subPort': 7,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',  # err status
                        'timeout_ms': '>u4'
                    }
                }
            },
            'SET_CHARON_WATCHDOG_TIMEOUT': {
                'what': 'Set the period (in ms) of the Charon watchdog timer on the OBC.',
                'subPort': 8,
                'inoutInfo': {
                    'args': {
                        "Period" : '>u4'
                    },
                    'returns': {
                        'err': '>b',  # err status
                    }
                }
            },
            'GET_ADCS_WATCHDOG_TIMEOUT': {
                'subPort': 9,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',  # err status
                        'timeout_ms': '>u4'
                    }
                }
            },
            'SET_ADCS_WATCHDOG_TIMEOUT': {
                'subPort': 10,
                'inoutInfo': {
                    'args': {
                        "Period" : '>u4'
                    },
                    'returns': {
                        'err': '>b',  # err status
                    }
                }
            },
            'GET_NS_PAYLOAD_WATCHDOG_TIMEOUT': {
                'subPort': 12,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',  # err status
                        'timeout_ms': '>u4'
                    }
                }
            },
            'SET_NS_PAYLOAD_WATCHDOG_TIMEOUT': {
                'subPort': 13,
                'inoutInfo': {
                    'args': {
                        "Period" : '>u4'
                    },
                    'returns': {
                        'err': '>b',  # err status
                    }
                }
            },
            'ENABLE_BEACON_TASK': {
                'subPort': 14,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b', # err status
                    }
                }
            },
            'DISABLE_BEACON_TASK': {
                'subPort': 15,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b', # err status
                    }
                }
            },
            'BEACON_TASK_GET_STATE': {
                'subPort': 16,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b', # err status
                        'state': '>?'
                    }
                }
            },
            'GET_SOLAR_SWITCH_STATUS': {
                'what': "Gets the status of the switch connected to the power of the solar panel currentsense ICs",
                'subPort': 17,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b', # err status
                        'state': '>b'
                    }
                }
            },
            'SET_SOLAR_SWITCH': {
                'what': "Turn the solar panel currentsense ICs on or off",
                'subPort': 18,
                'inoutInfo': {
                    'args': {
                        'state' : '>b'
                    },
                    'returns': {
                        'err': '>b', # err status
                    }
                }
            },
        }
    },
    'COMMUNICATION': {
        'supports' : ("OBC",),
        'port': 10,
        'subservice': {
            'S_GET_FREQ': {
                'what': 'Gets the S-band frequency (Hz)',
                'subPort': 1,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'frequency_Hz': '>u4',
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
            'S_GET_FW': {
                'what': 'S-band Firmware Version. XYY = X.YY',
                'subPort': 6,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Firmware Version': '>u2',
                    }
                }
            },
            'S_GET_TR': {
                'what': 'S-band Transmit Ready Indicator = {0: >2560B in buffer}',
                'subPort': 7,
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
                'subPort': 8,
                'inoutInfo': {
                    'args': {
                        "Buffer_quantity" : '>B'
                    },
                    'returns': {
                        'err': '>b',
                        'buffer': '>u2',
                    }
                }
            },
            'S_GET_HK': {
                'what': 'Gets S-band housekeeping info',
                'subPort': 9,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'S_mode': '>B',
                        'PA_status': '>B',
                        'S_frequency_Hz': '>u4',
                        'S_scrambler': '>B',
                        'S_filter': '>B',
                        'S_modulation': '>B',
                        'S_data_rate': '>B',
                        'S_bit_order': '>B',
                        'S_PWRGD': '>B',
                        'S_TXL': '>B',
                        'Output Power': '>B',
                        'Power Amplifier Temperature': '>b',
                        'Top Temperature': '>b',
                        'Bottom Temperature': '>b',
                        'Battery Current': '>u2',
                        'Battery Voltage': '>u2',
                        'Power Amplifier Current': '>u2',
                        'Power Amplifier Voltage': '>u2',
                    }
                }
            },
            'S_SOFT_RESET': {
                'what': 'Reset S-band FPGA registers to default',
                'subPort': 10,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'S_GET_FULL_STATUS': {
                'what': 'A full status of S-band non-configurable parameters',
                'subPort': 11,
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
                        'Output Power': '>B',
                        'Power Amplifier Temperature': '>b',
                        'Top Temperature': '>b',
                        'Bottom Temperature': '>b',
                        'Battery Current mA': '>u2',
                        'Battery Voltage mV': '>u2',
                        'Power Amplifier Current mA': '>u2',
                        'Power Amplifier Voltage mV': '>u2',
                    }
                }
            },
            'S_SET_FREQ': {
                'what': 'Sets the frequency of S-band (Hz)',
                'subPort': 12,
                'inoutInfo': {
                    'args': {
                        "Frequency" : '>u4'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'S_SET_CONTROL': {
                'what': 'Sets the S-band`s power amplifier write status and its mode = {0:config, 1: synch, 2:data, 3:test data}. Input: 2 binary',
                'subPort': 13,
                'inoutInfo': {
                    'args': {
                        "Status" : '>u1',
                        "Mode" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'S_SET_ENCODER': {
                'what': 'Sets the S-band encoding configuration. mod={0:QPSK, 1:OQPSK}, rate={1:half, 0:full}. Input: 4 binary',
                'subPort': 14,
                'inoutInfo': {
                    'args': {
                        "Scrambler" : '>u1',
                        "Filter" : '>u1',
                        "Modulation" : '>u1',
                        "Baudrate" : '>u1',
                        "Bit_order": '>u1',
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'S_SET_PAPOWER': {
                'what': 'Sets the power value of S-band power amplifier (24, 26, 28, 30 dBm)',
                'subPort': 15,
                'inoutInfo': {
                    'args': {
                        "Power" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'S_GET_CONFIG': {
                'what': 'A full status of S-band configurable parameters (the ones with set functions)',
                'subPort': 16,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Frequency': '>u4',
                        'Power Amplifier Power': '>u1',
                        'Power Amplifier status': '>u1',
                        'Power Amplifier mode': '>u1',
                        'Encoder scrambler': '>u1',
                        'Encoder filter': '>u1',
                        'Encoder modulation': '>u1',
                        'Encoder rate': '>u1',
                        'Encoder bit order': '>u1'
                    }
                }
            },
            'S_SET_CONFIG': {
                'what': 'Sets all the 9 S-band configurable parameters',
                'subPort': 17,
                'inoutInfo': {
                    'args': {
                        "Freq" : '>u4',
                        "PA_power" : '>u1',
                        "PA_status" : '>u1',
                        "PA_mode" : '>u1',
                        "Enc_scrambler" : '>u1',
                        "Enc_filter" : '>u1',
                        "Enc_mod" : '>u1',
                        "Enc_rate" : '>u1',
                        "Enc_bit_order" : '>u1',
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_SCW': {
                'what': 'Sets UHF status control word',
                'subPort': 20,
                'inoutInfo': {
                    'args': { #RONLY = read only parameter
                        "HFTX_RONLY" : '>u1',
                        "UART_baud" : '>u1',
                        "Reset" : '>u1',
                        "RF_mode" : '>u1',
                        "Echo" : '>u1',
                        "Beacon" : '>u1',
                        "Pipe" : '>u1',
                        "SW_mode" : '>u1',
                        "CTS_RONLY" : '>u1',
                        "SEC_RONLY" : '>u1',
                        "FRAM_RONLY" : '>u1',
                        "RFTS_RONLY" : '>u1',
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_FREQ': {
                'what': 'Sets UHF frequency (Hz)',
                'subPort': 21,
                'inoutInfo': {
                    'args': {
                        "Freq" : '>u4'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_PIPE_T': {
                'what': 'Sets UHF PIPE timeout period',
                'subPort': 22,
                'inoutInfo': {
                    'args': {
                        "Timeout" : '>u4'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_BEACON_T': {
                'what': 'Sets UHF beacon message transmission period',
                'subPort': 23,
                'inoutInfo': {
                    'args': {
                        "Period" : ">u4"
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_AUDIO_T': {
                'what': 'Sets UHF audio beacon period b/w transmissions',
                'subPort': 24,
                'inoutInfo': {
                    'args': {
                        "Period" : '>u4'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_PARAMS': {
                'what': 'Sets UHF freq, pipe_t, beacon_t, audio_t parameters. Input:4',
                'subPort': 25,
                'inoutInfo': {
                    'args': {
                        "Freq" : '>u4',
                        "pipe_t" : '>u4',
                        "beacon_t" : '>u4',
                        "audio_t" : '>u4'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_RESTORE': {
                'what': 'Restore UHF default values',
                'subPort': 26,
                'inoutInfo': {
                    'args': {
                        "Set_1_to_confirm" : '>u1' #Safety precaution
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_LOW_PWR': {
                'what': 'Puts UHF TRX into low power mode',
                'subPort': 27,
                'inoutInfo': {
                    'args': {
                        "Set_1_to_confirm" : '>u1' #Safety precaution
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_DESTINATION': {
                'what': 'Sets UHF destination callsign',
                'subPort': 28,
                'inoutInfo': {
                    'args': {
                        "Callsign" : '>S6'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_SOURCE': {
                'what': 'Sets UHF source callsign',
                'subPort': 29,
                'inoutInfo': {
                    'args': {
                        "Callsign" : '>S6'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_MORSE': {
                'what': 'Sets UHF morse code callsign (max 36)',
                'subPort': 30,
                'inoutInfo': {
                    'args': {
                        "Callsign" : '>S36'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_MIDI': {
                'what': 'Sets UHF MIDI audio beacon (max 36 notes)',
                'subPort': 31,
                'inoutInfo': {
                    # increase packet size and switch to >U108
                    'args': {
                        "Beacon" : '>S60'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_BEACON_MSG': {
                'what': 'Sets UHF beacon message (max 98)',
                'subPort': 32,
                'inoutInfo': {
                    #TODO Switch to >U97 after packet configuration
                    'args': {
                        "Beacon" : '>S60'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_I2C': {
                'what': 'Sets UHF I2C address (22 | 23)',
                'subPort': 33,
                'inoutInfo': {
                    'args': {
                        "Address" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_WRITE_FRAM': {
                'what': 'Sets UHF FRAM address and write 16-byte data',
                'subPort': 34,
                'inoutInfo': {
                    'args': {
                        "Address" : '>u4',
                        "Data" : '>S16'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SECURE': {
                'what': 'Puts UHF TRX into secure mode',
                'subPort': 35,
                'inoutInfo': {
                    'args': {
                        "Set_1_to_confirm" : '>u1' #Safety precaution
                    },
                    'returns': {
                        'err': '>b',
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
                        'HFXT': '>u1',
                        'UartBaud': '>u1',
                        'Reset': '>u1',
                        'RF Mode': '>u1',
                        'Echo': '>u1',
                        'BCN': '>u1',
                        'PIPE': '>u1',
                        'Bootloader': '>u1',
                        'CTS': '>u1',
                        'SEC': '>u1',
                        'FRAM': '>u1',
                        'RFTS': '>u1',
                        'Frequency': '>u4',
                        'PIPE timeout': '>u4',
                        'Beacon period': '>u4',
                        'Audio trans. period': '>u4',
                        'Uptime': '>u4',
                        'Packets out': '>u4',
                        'Packets in': '>u4',
                        'Packets in CRC16': '>u4',
                        'Temperature': '>f',
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
                        'Destination': '>S6',
                        'Source': '>S6',
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
                        'Morse': '>S36',
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
                        'MIDI': '>S60',
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
                        'Beacon Message': '>S60',
                    }
                }
            },
            'UHF_GET_FRAM': {
                'what': 'Reads the FRAM data',
                'subPort': 41,
                'inoutInfo': {
                    'args': {
                        "FRAM" : '>u4' #TODO: Better name
                    },
                    'returns': {
                        'err': '>b',
                        'FRAM': '>S16',
                    }
                }
            },
            'UHF_SET_ECHO': {
                'what': 'Starts echo over UART',
                'subPort': 42,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_BCN': {
                'what': 'Set the communication to the beacon mode',
                'subPort': 43,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_PIPE': {
                'what': 'Set the communication to the PIPE(transparent) mode',
                'subPort': 44,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_GET_SECURE_KEY': {
                'what': 'Gets the key for secure mode',
                'subPort': 45,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Secure Key': '>u4',
                    }
                }
            },
            'UHF_GET_SWVER': {
                'what': 'Gets the UHF firmware version',
                'subPort': 46,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'ver_XYZ': '>u2',
                    }
                }
            },
            'UHF_GET_PLDSZ': {
                'what': 'Gets UHF device payload size',
                'subPort': 47,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'size_B': '>u2',
                    }
                }
            },
            'UHF_SET_CRC16_ENABLE': {
                'what': 'Set whether UHF frame CRC16s are enabled',
                'subPort': 48,
                'inoutInfo': {
                    'args': {
                        'enabled':'>?',
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'UHF_SET_RF_MODE': {
                'what': 'Set mode of uhf communications as defined in UHF user manual',
                'subPort': 49,
                'inoutInfo': {
                    'args': {
                        'mode':'>b',
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
        }
    },

    'CONFIGURATION': {
        'supports' : ("EPS",),
        'port': 9,  # As per EPS docs
        'subservice': {
            'GET_ACTIVE_CONFIG': {
                'what': 'Gets config values in active mode for a specific type',
                'subPort': 0,
                'inoutInfo': {
                    'args': {
                        "id" : '<u2',
                        "type_id" : '<u1'
                    },
                    'returns': {
                        'err': '>B',
                        'type': '<u1',
                        'Value': 'var' #In command parser it gets the data type from the return value for 'type'
                    }
                }
            },
            'GET_MAIN_CONFIG': {
                'what': 'Gets config values in main mode for a specific type',
                'subPort': 1,
                'inoutInfo': {
                    'args': {
                        "id" : '<u2',
                        "type_id" : '<u1'
                    },
                    'returns': {
                        'err': '>B',
                        'type': '<u1',
                        'Value': 'var' #See comment for active
                    }
                }
            },
            'GET_FALLBACK_CONFIG': {
                'what': 'Gets config values in fallback mode for a specific type',
                'subPort': 2,
                'inoutInfo': {
                    'args': {
                        "id" : '<u2',
                        "type_id" : '<u1'
                    },
                    'returns': {
                        'err': '>B',
                        'type': '<u1',
                        'Value': 'var' #See comment for active
                    }
                }
            },
            'GET_DEFAULT_CONFIG': {
                'what': 'Gets config values in default mode for a specific type',
                'subPort': 3,
                'inoutInfo': {
                    'args': {
                        "id" : '<u2',
                        "type_id" : '<u1'
                    },
                    'returns': {
                        'err': '>B',
                        'type': '<u1',
                        'Value': 'var' #See comment for active
                    }
                }
            },
            'SET_CONFIG': {
                'what': 'Sets the configuration',
                'subPort': 4,
                'inoutInfo': {
                    'args': {
                        "id" : '<u2',
                        "type_id" : '<u1',
                        "Config" : 'var'
                    },
                    'returns': {
                        'err': '>B',
                    }
                }
            },
            'LOAD_MAIN2ACTIVE': {
                'what': 'Load main configuration from file into active',
                'subPort': 5,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>B'
                    }
                }
            },
            'LOAD_FALLBACK2ACTIVE': {
                'what': 'Load fallback configuration from file into active',
                'subPort': 6,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>B'
                    }
                }
            },
            'LOAD_DEFAULT2ACTIVE': {
                'what': 'Load default configuration from file into active',
                'subPort': 7,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>B'
                    }
                }
            },
            'UNLOCK_CONFIG': {
                'what': 'Unlock configuration for saving',
                'subPort': 8,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>B'
                    }
                }
            },
            'LOCK_CONFIG': {
                'what': 'Lock configuration from saving',
                'subPort': 9,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>B'
                    }
                }
            },
            'SAVE_ACTIVE2MAIN': {
                'what': 'Save active configuration to main file',
                'subPort': 10,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>B'
                    }
                }
            },
            'SAVE_ACTIVE2FALLBACK': {
                'what': 'Save active configuration to fallback file',
                'subPort': 11,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>B'
                    }
                }
            },
            'ELEVATE_ACCESS': {
                'what': 'Elevates access role. Key is in the docs',
                'subPort': 12,
                'inoutInfo': {
                    'args': {
                        "Role" : '<u1',
                        "Key" : '<u4'
                    },
                    'returns': {
                        'err': '>B'
                    }
                }
            },
            'GET_STATUS': {
                'what': 'Gets status and errors info',
                'subPort': 13,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>B',
                        'isInitialized': '<u1',
                        'isLocked': '<u1',
                        'isFallbackConfigurationLoaded': '<u1',
                        'isMainConfigurationLoaded': '<u1',
                        'wasFallbackRequested': '<u1',
                        'initSource': '<u1',
                        'currAccessRole': '<u1',
                        'totalNumofErrors': '<u1',
                        'numOfParameterDoesNotExistErrors': '<u1',
                        'numOfInvalidParameterTypeErrors': '<u1',
                        'numOfValidationFailErrors': '<u1',
                        'numOfStorageFailErrors': '<u1',
                        'numOfNotInitializedErrors': '<u1',
                        'numOfNotLoadedOnInitErrors': '<u1',
                        'numOfLockedErrors': '<u1',
                        'numOfAccessDeniedErrors': '<u1',
                        'numOfWrongPasswordErrors': '<u1',
                        'numOfUnknownErrors': '<u1',
                    }
                }
            },
        }
    },
    'HOUSEKEEPING': {
        'supports' : ("OBC",),
        'port': 17,
        'subservice': {
            'GET_HK': {
                'what': 'Fetch system-wide housekeeping. Input: limit, before_id, before_time',
                'subPort': 0,
                'inoutInfo': {
                    'args': {
                        "Limit" : '>u2',
                        "Before_id" : '>u2',
                        "Before_time" : '>u4'
                    },
                    'returns' : obc_housekeeping
                }
            },
            'SET_MAX_FILES': {
                'what': 'Set max number of hk entries to store',
                'subPort': 1,
                'inoutInfo': {
                    'args': {
                        "Max" : '<u2'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'GET_MAX_FILES': {
                'what': 'Get max number of hk entries to store',
                'subPort': 2,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'max': '>u2'
                    }
                }
            },
            'GET_INSTANT_HK': {
                'what': 'Fetch system-wide housekeeping right now',
                'subPort': 3,
                'inoutInfo': {
                    'args': None,
                    'returns': obc_housekeeping
                }
            },
            'GET_LATEST_HK': {
                'what' : "Fetch latest system-wide housekeeping",
                'subPort': 4,
                'inoutInfo': {
                    'args': None,
                    'returns': obc_housekeeping
                }
            }
        }
    },

    'GROUND_STATION_WDT': {
        'supports' : ("EPS",),
        'port': 16,  # As per EPS docs
        'subservice': {
            'RESET_WDT': {
                'what': 'Resets the ground station watchdog timer. See docs for key value',
                'subPort': 0,
                'inoutInfo': {
                    'args': {
                        "Key" : '<u2'
                    },
                    'returns': {
                        'err': '>B'
                    }
                }
            },
            'GET_WDT_REMAINING': {
                'what': 'Gets GS watchdog time left in seconds',
                'subPort': 1,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>B',
                        'timeLeftInS': '<u4'
                    }
                }
            },
            'CLEAR_WDT_RESET_MARK': {
                'what': 'Clears GS watchdog reset mark. See docs for key value',
                'subPort': 2,
                'inoutInfo': {
                    'args': {
                        "Key" : '<u2'
                    },
                    'returns': {
                        'err': '>B',
                    }
                }
            },
            'CHECK_STARTUP_POST_RESET': {
                'what': 'Checks if startup happened after GS watchdog reset',
                'subPort': 3,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>B',
                        'startupAfterGsWdt': '?',
                    }
                }
            }
        }
    },

    'EPS_RESET': {
        'supports' : ("EPS",),
        'port': 15,  # As per EPS docs
        'subservice': {
            'EPS_HARD_RESET': {
                'what': 'Does a hard reset on EPS (Resets the config) Not recommended to use by the operator. Key value is 17767',
                'subPort': 1,
                'inoutInfo': {
                    'args': {
                        "Key" : '<u2'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
        }
    },

    'REBOOT': {
        'supports' : ("EPS",),
        'port': 4,  # As per EPS CSP docs
        # EPS soft reset
        # no subPort (command ID) needed.
        'subservice':{
            'SOFT': {
                'what': 'Does a soft reset on EPS (reboot) Not recommended to use by the operator. Key value is 491527 or 2147975175',
                'subPort': 128,
                'inoutInfo': {
                    'args': {
                        "Key" : '<u4'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            }
        }
        # magic number 0x80078007 must be sent with csp port 4 and no subPort number
    },

    'TM_CLI': {
        'supports' : ("EPS",),
        'port': 7,  # EPS remote CLI uses port 13 unless Otherwise specified #TODO: Does 7 mean otherwise specified?
        'subservice': {
            'GENERAL_TELEMETRY': {
                'what': 'Gets the general housekeeping telemetry data',
                'subPort': 0,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        # When fetched via eps CPS command, these values are LE
                        'status': '>b',
                        'timestamp': '<f8',
                        'uptimeInS': '<u4',
                        'bootCnt': '<u4',
                        'gs_wdt_time_left_s': '<u4',
                        'counter_wdt_gs': '<u4',
                        'mpptConverterVoltage1_mV': '<u2',
                        'mpptConverterVoltage2_mV': '<u2',
                        'mpptConverterVoltage3_mV': '<u2',
                        'mpptConverterVoltage4_mV': '<u2',
                        'curSolarPanels1_mA': '<u2',
                        'curSolarPanels2_mA': '<u2',
                        'curSolarPanels3_mA': '<u2',
                        'curSolarPanels4_mA': '<u2',
                        'curSolarPanels5_mA': '<u2',
                        'curSolarPanels6_mA': '<u2',
                        'curSolarPanels7_mA': '<u2',
                        'curSolarPanels8_mA': '<u2',
                        'vBatt_mV': '<u2',
                        'curSolar_mA': '<u2',
                        'curBattIn_mA': '<u2',
                        'curBattOut_mA': '<u2',
                        'curOutput1_mA': '<u2',
                        'curOutput2_mA': '<u2',
                        'curOutput3_mA': '<u2',
                        'curOutput4_mA': '<u2',
                        'curOutput5_mA': '<u2',
                        'curOutput6_mA': '<u2',
                        'curOutput7_mA': '<u2',
                        'curOutput8_mA': '<u2',
                        'curOutput9_mA': '<u2',
                        'curOutput10_mA': '<u2',
                        'curOutput11_mA': '<u2',
                        'curOutput12_mA': '<u2',
                        'curOutput13_mA': '<u2',
                        'curOutput14_mA': '<u2',
                        'curOutput15_mA': '<u2',
                        'curOutput16_mA': '<u2',
                        'curOutput17_mA': '<u2',
                        'curOutput18_mA': '<u2',
                        'AOcurOutput1_mA': '<u2',
                        'AOcurOutput2_mA': '<u2',
                        'outputConverterVoltage1': '<u2',
                        'outputConverterVoltage2': '<u2',
                        'outputConverterVoltage3': '<u2',
                        'outputConverterVoltage4': '<u2',
                        'outputConverterVoltage5': '<u2',
                        'outputConverterVoltage6': '<u2',
                        'outputConverterVoltage7': '<u2',
                        'outputConverterVoltage8': '<u2',
                        'outputConverterState': '<B',  # 4 bits!
                        'outputStatus': '<u4',
                        'outputFaultStatus': '<u4',
                        'protectedOutputAccessCnt': '<u2',
                        'outputOnDelta1': '<u2',
                        'outputOnDelta2': '<u2',
                        'outputOnDelta3': '<u2',
                        'outputOnDelta4': '<u2',
                        'outputOnDelta5': '<u2',
                        'outputOnDelta6': '<u2',
                        'outputOnDelta7': '<u2',
                        'outputOnDelta8': '<u2',
                        'outputOnDelta9': '<u2',
                        'outputOnDelta10': '<u2',
                        'outputOnDelta11': '<u2',
                        'outputOnDelta12': '<u2',
                        'outputOnDelta13': '<u2',
                        'outputOnDelta14': '<u2',
                        'outputOnDelta15': '<u2',
                        'outputOnDelta16': '<u2',
                        'outputOnDelta17': '<u2',
                        'outputOnDelta18': '<u2',
                        'outputOffDelta1': '<u2',
                        'outputOffDelta2': '<u2',
                        'outputOffDelta3': '<u2',
                        'outputOffDelta4': '<u2',
                        'outputOffDelta5': '<u2',
                        'outputOffDelta6': '<u2',
                        'outputOffDelta7': '<u2',
                        'outputOffDelta8': '<u2',
                        'outputOffDelta9': '<u2',
                        'outputOffDelta10': '<u2',
                        'outputOffDelta11': '<u2',
                        'outputOffDelta12': '<u2',
                        'outputOffDelta13': '<u2',
                        'outputOffDelta14': '<u2',
                        'outputOffDelta15': '<u2',
                        'outputOffDelta16': '<u2',
                        'outputOffDelta17': '<u2',
                        'outputOffDelta18': '<u2',
                        'outputFaultCount1': '<B',
                        'outputFaultCount2': '<B',
                        'outputFaultCount3': '<B',
                        'outputFaultCount4': '<B',
                        'outputFaultCount5': '<B',
                        'outputFaultCount6': '<B',
                        'outputFaultCount7': '<B',
                        'outputFaultCount8': '<B',
                        'outputFaultCount9': '<B',
                        'outputFaultCount10': '<B',
                        'outputFaultCount11': '<B',
                        'outputFaultCount12': '<B',
                        'outputFaultCount13': '<B',
                        'outputFaultCount14': '<B',
                        'outputFaultCount15': '<B',
                        'outputFaultCount16': '<B',
                        'outputFaultCount17': '<B',
                        'outputFaultCount18': '<B',
                        'temp1_c': '<b',
                        'temp2_c': '<b',
                        'temp3_c': '<b',
                        'temp4_c': '<b',
                        'temp5_c': '<b',
                        'temp6_c': '<b',
                        'temp7_c': '<b',
                        'temp8_c': '<b',
                        'temp9_c': '<b',
                        'temp10_c': '<b',
                        'temp11_c': '<b',
                        'temp12_c': '<b',
                        'temp13_c': '<b',
                        'temp14_c': '<b',
                        'battMode': '<B',
                        'mpptMode': '<B',
                        'battHeaterMode': '<B',
                        'battHeaterState': '<B',
                        'PingWdt_toggles': '<u2',
                        'PingWdt_turnOffs': '<B'
                    }
                }
            },
            # ALL the EPS CLI commands:
            'SET_TELEMETERY_PERIOD': {
                'what': 'Set telemetery collection period on EPS. Magicword is in the docs',
                'subPort': 255,
                'inoutInfo': {
                    'args': {
                        "Magicword" : '<u4',
                        "Telem_ID" : '<B',
                        "Period" : '<u4',
                        "Duration" : '<u4'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            # EPS Startup Telemetry
            'STARTUP_TELEMETRY': {
                'what': 'Get the startup telemetry from the EPS',
                'subPort': 1,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        # When fetched via eps CPS command, these values are LE
                        #'cmd': '>b',
                        'status': '>b',
                        'timestamp': '<f8',
                        'last_reset_reason_reg': '<u4',
                        'bootCnt': '<u4',
                        'FallbackConfigUsed': '<B',
                        'rtcInit': '<B',
                        'rtcClkSourceLSE': '<B',
                        'Fram4kPartitionInit': '>b',
                        'Fram520kPartitionInit': '>b',
                        'intFlashPartitionInit': '>b',
                        'FSInit': '>b',
                        'FTInit': '>b',
                        'supervisorInit': '>b',
                        'uart1App': '<B',
                        'uart2App': '<B',
                        'tmp107Init': '>b'
                    }
                }
            }
        }
    },

    'CONTROL': {
        'supports' : ("EPS",),
        'port': 14,
        'subservice': {
            # POWER OUTPUTS
            'SINGLE_OUTPUT_CONTROL': {
                'what': 'Turns on/off a power output channel (with a defined delay)',
                'subPort': 0,
                'inoutInfo': {
                    # output num., state, delay (s)
                    'args': {
                        "Channel" : '<B',
                        "State" : '<B',
                        "Delay" : '<u2'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ALL_OUTPUT_CONTROL': {
                'what': 'Sets all ouputs status at once (nth bit -> nth channel. 18 bit binary integer',
                'subPort': 1,
                'inoutInfo': {
                    'args': {
                        "StateMask" : '<u4'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'SINGLE_OUTPUT_CONTROL_NORMAL_BATT': {
                'what': 'Set the output channels mode on normal battery mode',
                'subPort': 9,
                'inoutInfo': {
                    # output num., state, delay (s)
                    'args': {
                        "Channel" : '<B',
                        "State" : '<B',
                        "Delay" : '<u2'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },

            # SOLAR PANEL INPUTS & MPPT
            'SET_SINGLE_MPPT_CONV_V': {
                'what': 'Sets single MPPT converter voltage. Voltage is in mv',
                'subPort': 2,
                'inoutInfo': {
                    'args': {
                        "Channel" : '<B',
                        "Voltage" : '<u2'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'SET_ALL_MPPT_CONV_V': {
                'what': 'Sets all MPPT converter voltage at once',
                'subPort': 3,
                'inoutInfo': {
                    'args': {
                        "v1" : '<u2',
                        "v2" : '<u2',
                        "v3" : '<u2',
                        "v4" : '<u2',
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'SET_MODE_MPPT': {
                'what': 'Sets MPPT mode. 0-Hw, 1-manual, 2-auto, 3-auto w/ timeout',
                'subPort': 4,
                'inoutInfo': {
                    'args': {
                        "Mode" : '<B'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'SET_AUTO_TIMEOUT_MPPT': {
                'what': 'Sets MPPT auto timeout period',
                'subPort': 5,
                'inoutInfo': {
                    'args': {
                        "Timeout" : '<u4'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },

            # BATTERY HEATER
            'SET_HEATER_MODE': {
                'what': 'Manual, or automatic. See docs for mode values', #TODO: Put the mode values here
                'subPort': 6,
                'inoutInfo': {
                    'args': {
                        "Mode" : '<B'
                    },
                    'returns': {
                        'status': '>b'
                    }
                }
            },
            'SET_HEATER_STATE': {
                'what': 'On, or off. Duration in seconds', #TODO: What number is on or off?
                'subPort': 7,
                'inoutInfo': {
                    'args': {
                        "State" : '<B',
                        "Duration" : '<u2'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            }
        }
    },
    'UPDATER' : {
        'supports' : ("OBC",),
        'port': 12,
        'subservice': {
            'INITIALIZE_UPDATE': {
                'what' : 'Start update procedure. Provide address, size, crc. Not intended for operator use. Use updater program',
                'subPort': 0,
                'inoutInfo': {
                    'args': {
                        "Address" : '>u4',
                        "Size" : '>u4',
                        "CRC" : '>u2'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'PROGRAM_BLOCK': {
                'what' : 'Program a single block of data. Not intended for operator use. Use updater program',
                'subPort': 1,
                'inoutInfo': {
                    'args': { #TODO: Better names
                        "Arg1" : '>u4',
                        "Arg2" : '>u4'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'GET_PROGRESS' : {
                'what' : 'Get update progress. Not intended for operator use. Use updater program',
                'subPort' : 2,
                'inoutInfo' : {
                    'args' : None,
                    'returns' : {
                        'err' : '>b',
                        'start_addr' : '>u4',
                        'next_addr' : ">u4",
                        'crc' : '>u2'
                    }
                }
            },
            'ERASE_APP' : {
                'what' : 'Erase working image. Not intended for operator use. Use updater program',
                'subPort' : 3,
                'inoutInfo' : {
                    'args' : None,
                    'returns' : {
                        'err' : '>b'
                    }
                }
            },
            'VERIFY_APP' : {
                'what' : 'Verify crc of working image. Not intended for operator use. Use updater program',
                'subPort' : 4,
                'inoutInfo' : {
                    'args' : None,
                    'returns' : {
                        'err' : '>b'
                    }
                }
            },
            'VERIFY_GOLDEN' : {
                'what' : 'Verify crc of golden image',
                'subPort' : 5,
                'inoutInfo' : {
                    'args' : None,
                    'returns' : {
                        'err' : '>b'
                    }
                }
            }
        }
    },

    'LOGGER': {
        'supports' : ("OBC",),
        'port': 13,
        'subservice': {
            'GET_FILE': {
                'what': 'Get contents of log file',
                'subPort': 0,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'log': '>S500',
                    }
                }
            },
            'GET_OLD_FILE': {
                'what': 'Get contents of old log file',
                'subPort': 1,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'log': '>S500',
                    }
                }
            },
            'SET_FILE_SIZE': {
                'what': 'Set the size of the logger files.',
                'subPort': 3,
                'inoutInfo': {
                    'args': {
                        "Size" : '>u4'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'GET_FILE_SIZE': {
                'what': 'Get the size of the logger files.',
                'subPort': 2,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'size': '>u4'
                    }
                }
            }
        }
    },
    'CLI' : {
        'supports' : ("OBC",),
        'port': 24,
        'subservice': {
            'SEND_CMD': {
                'what': 'Send command over the sat_cli. Not intended for operator use. Use sat_cli program',
                'subPort': 0,
                'inoutInfo': {
                    'args': {
                        "Len" : "B",
                        "Command" : "a128"
                    },
                    'returns': {
                        "status": '>b',
                        "resp": "a128"
                    }
                }
            }
        }
    },
    'ADCS': { # refer to the adcs service
        'supports' : ("OBC",),
        'port': 18,
        'subservice': {
            'ADCS_RESET': {
                'what': 'Forces ADCS to perform a reset.',
                'subPort': 0,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_RESET_LOG_POINTER': {
                'what': 'Resets TLM log pointer to log buffer (from where LastLogEvent TLM is returned).',
                'subPort': 1,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_ADVANCE_LOG_POINTER': {
                'what': 'Advances TLM log pointer to log buffer (form where LastLogEvent TLM is returned).',
                'subPort': 2,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_RESET_BOOT_REGISTERS': {
                'what': 'Resets boot counter, state, and cause registers',
                'subPort': 3,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_FORMAT_SD_CARD': {
                'what': 'Formats SD card.',
                'subPort': 4,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_ERASE_FILE': {
                'what': 'Erases file by file type and counter. Alternatively, can erase all files in SD card.',
                'subPort': 5,
                'inoutInfo': {
                    'args': {
                        "File_type" : '>u1',
                        "File_counter" : '>u1',
                        "Erase_all" : '>u1'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_LOAD_FILE_DOWNLOAD_BLOCK': {
                'what': 'Fill download buffer with file contents specified by file type, counter, offset and length.',
                'subPort': 6,
                'inoutInfo': {
                    'args': {
                        "File_type" : '>u1',
                        "File_counter" : '>u1',
                        "Offset" : '>u4',
                        "Block_length" : '>u2'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_ADVANCE_FILE_LIST_READ_POINTER': {
                'what':  'Advances file list read pointer.',
                'subPort': 7,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_INITIATE_FILE_UPLOAD': {
                'what': 'Initiates file upload to destination (Table 20, F/W Ref. Manual) with block size specified.',
                'subPort': 8,
                'inoutInfo': {
                    'args': {
                        "File_dest" : '>u1',
                        "Block_size" : '>u1'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_FILE_UPLOAD_PACKET': {
                'what': 'Sends 20-byte file message. Include packet number and file bytes to be sent.',
                'subPort': 9,
                'inoutInfo': {
                    'args': {
                        "Packet_num" : '>u2',
                        "File_bytes" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                        'file_bytes': '>b'
                    }
                }
            },
            'ADCS_FINALIZE_UPLOAD_BLOCK': {
                'what': 'Finalizes uploaded file block at specified destination (Table 20, F/W Ref. Manual), offset, and block length. Executed after hole map is complete.',
                'subPort': 10,
                'inoutInfo': {
                    'args': {
                        "File_dest" : '>u2',
                        "Offset" : '>u4',
                        "Block_length" : '>u2'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_RESET_UPLOAD_BLOCK': {
                'what': 'Resets the hole map for the upload block.',
                'subPort': 11,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_RESET_FILE_LIST_READ_POINTER': {
                'what': 'Resets file list read pointer.',
                'subPort': 12,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_INITIATE_DOWNLOAD_BURST': {
                'what': 'Initiates download burst. ADCS begins to send 20-byte packets. Specify message length, and hole map polling. Executed after download block is ready.',
                'subPort': 13,
                'inoutInfo': {
                    'args': {
                        "Msg_len" : '>u1',
                        "Ignore_hole_map" : '>?'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_GET_NODE_IDENTIFICATION': {
                'what': 'Returns identification for this node: type, interface, firmware versions, and runtime in s and ms.',
                'subPort': 14,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Node_Type': '>u1',
                        'Interface_Ver': '>u1',
                        'Major_Firm_Ver': '>u1',
                        'Minor_Firm_Ver': '>u1',
                        'Runtime_S': '>u2',
                        'Runtime_Ms': '>u2'
                    }
                }
            },
            'ADCS_GET_BOOT_PROGRAM_STAT': {
                'what': 'Returns boot and running program status: reset cause, boot cause (Table 29 and 30 F/W Ref. Manual), boot counter, program index and firmware version',
                'subPort': 15,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Mcu_Reset_Cause': '>u1',
                        'Boot_Cause': '>u1',
                        'Boot_Count': '>u2',
                        'Boot_Idx': '>u1',
                        'Major_Firm_Ver': '>u1',
                        'Minor_Firm_Ver': '>u1'
                    }
                }
            },
            'ADCS_GET_BOOT_INDEX': {
                'what': 'Returns program index and boot status (Tables 31 and 33 F/W Ref. Manual)',
                'subPort': 16,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Program_Idx': '>u1',
                        'Boot_Stat': '>u1',
                    }
                }
            },
            'ADCS_GET_LAST_LOGGED_EVENT': {
                'what': 'Returns last logged event time, ID and parameter (relative to pointer -- use advance/reset log pointer commands).',
                'subPort': 17,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Time': '>u4',
                        'Event_Id': '>u1',
                        'Event_Param': '>u1'
                    }
                }
            },
            'ADCS_GET_SD_FORMAT_PROGRESS': {
                'what': 'Returns SD format and/or erase all progress.',
                'subPort': 18,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'FormT_Busy': '>?',
                        'Erase_All_Busy': '>?',
                    }
                }
            },
            'ADCS_GET_TC_ACK': {
                'what': 'Returns last TC ID, processed flag, TC error status (Table 40 F/W Ref. Manual) and index.',
                'subPort': 19,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Last_Tc_Id': '>u1',
                        'Tc_Processed': '>?',
                        'Tc_Err_Stat': '>b',
                        'Tc_Param_Err_Index': '>B'
                    }
                }
            },
            'ADCS_GET_FILE_DOWNLOAD_BUFFER': {
                'what': 'Returns file download buffer with packet count and 20-byte packet.',
                'subPort': 20,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Packet_Count': '>u2',
                        'File': '>u4', #TODO: array
                    }
                }
            },
            'ADCS_GET_FILE_DOWNLOAD_BLOCK_STAT': {
                'what': 'Returns ready flag, msg length and hole map parameter error flag, CRC16 checksum, and block length of download block.',
                'subPort': 21,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Ready': '>?',
                        'Param_Err': '>?',
                        'Crc16_Checksum': '>u2',
                        'Length': '>u2'
                    }
                }
            },
            'ADCS_GET_FILE_INFO': {
                'what': 'Returns file type, update flag, counter, size, date/time, CRC16 checksum.',
                'subPort': 22,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Type': '>u1',
                        'Updating': '>?',
                        'File_Counter': '>u1',
                        'Size': '>u4',
                        'Time': '>u4',
                        'Crc16_Checksum': '>u2'
                    }
                }
            },
            'ADCS_GET_INIT_UPLOAD_STAT': {
                'what': 'Returns status of upload initiation.',
                'subPort': 23,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Busy': '>?',
                    }
                }
            },
            'ADCS_GET_FINALIZE_UPLOAD_STAT': {
                'what': 'Returns busy and error flag regarding upload finalization status.',
                'subPort': 24,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Busy': '>?',
                        'Error': '>?'
                    }
                }
            },
            'ADCS_GET_UPLOAD_CRC16_CHECKSUM': {
                'what': 'Returns upload CRC16 checksum.',
                'subPort': 25,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Checksum': '>u2'
                    }
                }
            },
            'ADCS_GET_SRAM_LATCHUP_COUNT': {
                'what': 'Returns SRAM1 and SRAM2 latchup counts.',
                'subPort': 26,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Sram1': '>u2',
                        'Sram2': '>u2'
                    }
                }
            },
            'ADCS_GET_EDAC_ERR_COUNT': {
                'what': 'Returns single, double, and multiple SRAM upsets.',
                'subPort': 27,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Single_Sram': '>u2',
                        'Double_Sram': '>u2',
                        'Multi_Sram': '>u2'
                    }
                }
            },
            'ADCS_GET_COMMS_STAT': {
                'what': 'Returns TC counter, TLM request counter, TC buffer overrun flag, and UART, I2C, and CAN error flags.',
                'subPort': 28,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'TC_num': '>u2',
                        'TM_num': '>u2',
                        'TC_Buffer_Overrun': '<B',
                        'UART_Error': '<B',
                        'UART_Incomplete': '<B',
                        'I2C_TLM_Err': '<B',
                        'I2C_TC_Buffer_Err': '<B',
                        'CAN_TC_Buffer_Err': '<B',

                    }
                }
            },
            'ADCS_SET_CACHE_EN_STATE': {
                'what': 'Sets cache enabled state.',
                'subPort': 29,
                'inoutInfo': {
                    'args': {
                        "State" : '>?'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_SRAM_SCRUB_SIZE': {
                'what': 'Set SRAM scrubbing size.',
                'subPort': 30,
                'inoutInfo': {
                    'args': {
                        "Size" : '>u2'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_UNIXTIME_SAVE_CONFIG': {
                'what' : "when: [1 = now, 2 = on update, 4 = periodically], period",
                'subPort': 31,
                'inoutInfo': {
                    'args': {
                        "When" : '>u1',
                        "period" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_HOLE_MAP': {
                'what': 'Sets file upload hole map (up to 8 arrays of 16 bytes).',
                'subPort': 32,
                'inoutInfo': {
                    'args': {
                        "Hole_Map" : '>u1',
                        "Hole_Map_Num" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                        'Hole_Map': '>u1'
                    }
                }
            },
            'ADCS_SET_UNIX_T': {
                'what': 'Sets the Unix Time.',
                'subPort': 33,
                'inoutInfo': {
                    'args': {
                        "Unix_T" : '>u4',
                        "Count_Millis" : '>u2'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_GET_CACHE_EN_STATE': {
                'what': 'Returns cache enabled state.',
                'subPort': 34,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'En_State': '>?'
                    }
                }
            },
            'ADCS_GET_SRAM_SCRUB_SIZE': {
                'what': 'Returns SRAM scrubbing size.',
                'subPort': 35,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Size': '>u2'
                    }
                }
            },
            'ADCS_GET_UNIXTIME_SAVE_CONFIG': {
                'what': 'Returns Unix Time save configuration: when: [1 = now, 2 = on update, 4 = periodically], and period',
                'subPort': 36,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'When': '>u1',
                        'Period': '>u1'
                    }
                }
            },
            'ADCS_GET_HOLE_MAP': {
                'what': 'Returns file upload hole map: ',
                'subPort': 37,
                'inoutInfo': {
                    'args': {
                        "Hole_Map_Num" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                        'Hole_Map': '>u1',
                    }
                }
            },
            'ADCS_GET_UNIX_T': {
                'what': 'Returns the Unix Time in (in s and ms) saved on the ADCS.',
                'subPort': 38,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Unix_t': '>u4',
                        'Count_Ms': '>u2'
                    }
                }
            },
            'ADCS_CLEAR_ERR_FLAGS': {
                'what': 'Clears ADCS error flags.',
                'subPort': 39,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_BOOT_INDEX': {
                'what': 'Selects which program to boot (Table 63 F/W Ref. Manual).',
                'subPort': 40,
                'inoutInfo': {
                    'args': {
                        "Index" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_RUN_SELECTED_PROGRAM': {
                'what': 'Runs selected program -- forces the bootloader to run internal flash program.',
                'subPort': 41,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_READ_PROGRAM_INFO': {
                'what': 'Requests program CRC and length, use ADCS_GET_PROGRAM_INFO to read.',
                'subPort': 42,
                'inoutInfo': {
                    'args': {
                        "Index" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_COPY_PROGRAM_INTERNAL_FLASH': {
                'what': 'Copies program at index (Table 66, F/W Ref. Manual), with option to overwrite the bootloader.',
                'subPort': 43,
                'inoutInfo': {
                    'args': {
                        "Index" : '>u1',
                        "Overwrite_flag" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_GET_BOOTLOADER_STATE': {
                'what': 'Return status flags for bootloader.',
                'subPort': 44,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Uptime_S': '>u2',
                        'SRAM1_En': '>u1',
                        'SRAM2_En': '>u1',
                        'SRAM_Latch_Err_Un_Re': '>u1',
                        'SRAN_Latch_Err_Re': '>u1',
                        'SD_Card_Init_Err': '>u1',
                        'SD_Card_Read_Err': '>u1',
                        'SD_Card_Write_Err': '>u1',
                        'Ext_Flash_Err': '>u1',
                        'Int_Flash_Err': '>u1',
                        'EEPROM_Err': '>u1',
                        'Boot_Reg_Corrupt': '>u1',
                        'Comms_Err': '>u1'
                    }
                }
            },
            'ADCS_GET_PROGRAM_INFO': {
                'what': 'Returns program index, reading flag, file syze (bytes) and CRC16 checksum.',
                'subPort': 45,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Index': '>u1',
                        'Busy': '>?',
                        'File_Size': '>u4',
                        'Crc16_Checksum': '>u2'
                    }
                }
            },
            'ADCS_COPY_INTERNAL_FLASH_PROGRESS': {
                'what': 'Progress of copy to internal flash operation -- returns busy and error flags.',
                'subPort': 46,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Error': '>?',
                        'Busy': '>?',
                    }
                }
            },
            'ADCS_DEPLOY_MAGNETOMETER_BOOM': {
                "what" : "Actuation timeout in seconds",
                'subPort': 47,
                'inoutInfo': {
                    'args': {
                        "Actuation_timeout" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_ENABLED_STATE': {
                'what': 'Set emabled state and control loop behaviour (Table 75, F/W Ref. Manual).',
                'subPort': 48,
                'inoutInfo': {
                    'args': {
                        "State" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_CLEAR_LATCHED_ERRS': {
                'what': 'Clear ADCS and/or HK error flags.',
                'subPort': 49,
                'inoutInfo': {
                    'args': { #TODO: Better names
                        "ADCS_Err_Flags" : '>?',
                        "HK_Err_Flags" : '>?'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_ATTITUDE_CONTROL_MODE': {
                'what': 'Sets control mode (Table 78 F/W Ref. Manual), and control timeout duration (0xFFFF for inf timeout).',
                'subPort': 50,
                'inoutInfo': {
                    'args': {
                        "Control_mode" : '>u1',
                        "Timeout" : '>u2'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_ATTITUDE_ESTIMATE_MODE': {
                'what': 'Sets estimation mode (Table 80 F/W Ref. Manual).',
                'subPort': 51,
                'inoutInfo': {
                    'args': {
                        "Est_Mode" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_TRIGGER_ADCS_LOOP': {
                'what': 'Trigger ADCS to perform one iteration of the control loop (only when Run Mode is triggered).',
                'subPort': 52,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_TRIGGER_ADCS_LOOP_SIM': {
                'what': 'Trigger ADCS to perform one iteration of the control loop only with simulated sensor data.',
                'subPort': 53,
                'inoutInfo': {
                    'args': None, #TODO: sim_sensor_data type ?
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_ASGP4_RUN_MODE': {
                'what': 'Sets ASGP4 run mode -- (GPS augmented SGP4 not used, use SGP4 commands instead!).',
                'subPort': 54,
                'inoutInfo': {
                    'args': {
                        "Mode" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_TRIGGER_ASGP4': {
                'what': 'Trigger ASGP4 process -- (GPS augmented SGP4 not used, use SPG4 commands instead!).',
                'subPort': 55,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_MTM_OP_MODE': {
                'what': 'Set magnetometer mode (Table 90 F/W Ref. Manual).',
                'subPort': 56,
                'inoutInfo': {
                    'args': {
                        "Mtm_Mde" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_CNV2JPG': {
                'what': 'Convert raw/bmp files to JPG',
                'subPort': 57,
                'inoutInfo': {
                    'args': {
                        "Src_File_Ctr" : '>u1',
                        "Qual_Factor" : '>u1',
                        "White_Bal" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SAVE_IMG': {
                'what': 'Save and capture image from CubeSense or CubeStar cameras to SD card with specified size (Tables 95 and 96 F/W Ref. Manual).',
                'subPort': 58,
                'inoutInfo': {
                    'args': {
                        "Cam_Select" : '>u1',
                        "Img_Size" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },

            'ADCS_SET_MAGNETORQUER_OUTPUT': {
                'what': 'Set X, Y, and Z magnetorquer duty cycles [0 - +/-800]. Only valid of Control Mode is None.',
                'subPort': 59,
                'inoutInfo': {
                    'args': {
                        "Mtq_X" : '>i2',
                        "Mtq_Y" : '>i2',
                        "Mtq_Z" : '>i2'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_WHEEL_SPEED': {
                'what': 'Set wheel speed rpm [0 - +/-8000]. Only valid if Control Mode is None.',
                'subPort': 60,
                'inoutInfo': {
                    'args': {
                        "Wheel_X" : '>i2',
                        "Wheel_Y" : '>i2',
                        "Wheel_Z" : '>i2'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SAVE_CONFIG': {
                'what': 'Saves current configuration to flash memory.',
                'subPort': 61,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SAVE_ORBIT_PARAMS': {
                'what': 'Saves current orbit parameters to flash memory.',
                'subPort': 62,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_GET_CURRENT_STATE': {
                'what': 'Gets full ADCS state (Table 149 F/W Ref. Manual).',
                'subPort': 63,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'att_estimate_mode': '>B',
                        'att_ctrl_mode': '>B',
                        'run_mode': '>B',
                        'ASGP4_mode': '>B',
                        'Cubectrl_Sig_En': '>B',
                        'Cubectrl_Mtr_En': '>B',
                        'Cube1_En': '>B',
                        'Cubesns2_En': '>B',
                        'Cubewhl1_En': '>B',
                        'Cubewhl2_En': '>B',
                        'Cubewhl3_En': '>B',
                        'Cubestr_En': '>B',
                        'GPS_Rx_En': '>B',
                        'GPS_LNA_Pwr_En': '>B',
                        'Mtr_Drvr_En': '>B',
                        'Sun_Abv_Lcl_Hrzn': '>B',
                        'CubeSense1_Comms_Err': '>B',
                        'CubeSense2_Comms_Err': '>B',
                        'Cubectrl_Sig_Comms_Err': '>B',
                        'Cubectrl_Mtr_Comms_Err': '>B',
                        'CubeWheel1_Comms_Err': '>B',
                        'CubeWheel2_Comms_Err': '>B',
                        'CubeWheel3_Comms_Err': '>B',
                        'CubeStar_Comms_Err': '>B',
                        'Mtm_Rng_Err': '>B',
                        'Cam1_SRAM_Ov': '>B',
                        'Cam1_3V3_Ov': '>B',
                        'Cam1_Busy_Err': '>B',
                        'Cam1_Det_Err': '>B',
                        'Sun_Snsr_Rng_Err': '>B',
                        'Cam2_SRAM_Ov': '>B',
                        'Cam2_3V3_Ov': '>B',
                        'Cam2_Busy_Err': '>B',
                        'Cam2_Det_Err': '>B',
                        'Ndir_Snsr_Rng_Err': '>B',
                        'Rate_Snsr_Rng_Err': '>B',
                        'Whl_Spd_Rng_Err': '>B',
                        'Crs_Sun_Snsr_Err': '>B',
                        'Strtrckr_Mtch_Err': '>B',
                        'Strtrckr_Ov_Det': '>B',
                        'Orbt_Param_Invld': '>B',
                        'Cnfg_Invld': '>B',
                        'Ctrl_Mde_Invld': '>B',
                        'Estmtr_Chng_Invld': '>B',
                        'Mtm_Smpl_Mode': '>B',
                        'Mag_Fld_Diff': '>B',
                        'Node_Recov_Err': '>B',
                        'CubeSense1_Runtm_Err': '>B',
                        'CubeSense2_Runtm_Err': '>B',
                        'Cubectrl_Sgnl_Runtm_Err': '>B',
                        'Cubectrl_Mtr_Runtm_Err': '>B',
                        'CubeWhl1_Runtm_Err': '>B',
                        'CubeWhl2_Runtm_Err': '>B',
                        'CubeWhl3_Runtm_Err': '>B',
                        'Cubestr_Runtm_Err': '>B',
                        'Mtm__Err': '>B',
                        'Rate_Snsr_Fail': '>B',
                        'est_roll_angle': '>f4',
                        'est_pitch_angle': '>f4',
                        'est_yaw_angle': '>f4',
                        'est_quaternion_x': '>i2',
                        'est_quaternion_y': '>i2',
                        'est_quaternion_z': '>i2',
                        'est_angular_rate_x': '>f4',
                        'est_angular_rate_y': '>f4',
                        'est_angular_rate_z': '>f4',
                        'ECI_pos_x': '>f4',
                        'ECI_pos_y': '>f4',
                        'ECI_pos_z': '>f4',
                        'ECI_vel_x': '>f4',
                        'ECI_vel_y': '>f4',
                        'ECI_vel_z': '>f4',
                        'Latitude': '>f4',
                        'Longitude': '>f4',
                        'Altitude': '>f4',
                        'ecef_pos_x': '>i2',
                        'ecef_pos_y': '>i2',
                        'ecef_pos_z': '>i2'
                    }
                }
            },
            'ADCS_GET_JPG_CNV_PROGESS': {
                'what': 'Returns JPG conversion progress.',
                'subPort': 64,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Percentage': '>u1',
                        'Result': '>u1',
                        'File_Counter': '>u1'
                    }
                }
            },
            'ADCS_GET_CUBEACP_STATE': {
                'what': 'Returns flags regarding ACP state.',
                'subPort': 65,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Cnfg_Load_Err': '>u1',
                        'Orbt_Param_Load_Err': '>u1',
                        'Sys_Cnfg_Load_Err': '>u1',
                        'SD_Crd_Init_Err': '>u1',
                        'SD_Crd_Rd_Err': '>u1',
                        'SD_Crd_Wrt_Err': '>u1',
                    }
                }
            },
            'ADCS_GET_SAT_POS_LLH': {
                'what': 'Returns LLH (WGS-84) satellite position.',
                'subPort': 66,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Latitude': '>i2',
                        'Longitude': '>i2',
                        'Altitude': '>u2',
                    }
                }
            },
            'ADCS_GET_EXECUTION_TIMES': {
                'what': 'Returns execution times of ACP functions (Table 155 F/W Ref. Manual).',
                'subPort': 67,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Adcs_Update': '>u2',
                        'Sensor_Comm': '>u2',
                        'SGP4_propag': '>u2',
                        'IGRF_model': '>u2'
                    }
                }
            },
            'ADCS_GET_ACP_LOOP_STAT': {
                'what': 'Returns time (ms) since start of loop and execution point (Table 168 F/W Ref. Manual).',
                'subPort': 68,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Time': '>u2',
                        'Execution_point': '>u1'
                    }
                }
            },
            'ADCS_GET_IMG_SAVE_PROGRESS': {
                'what': 'Returns image save progress.',
                'subPort': 69,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Percentage': '>u1',
                        'Status': '>u1'
                    }
                }
            },
            'ADCS_GET_MEASUREMENTS': {
                'what': 'Returns calibrated sensor measurements (Table 150 F/W Ref. Manual).',
                'subPort': 70,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Magnetic_field_X': '>f4',
                        'Magnetic_field_Y': '>f4',
                        'Magnetic_field_Z': '>f4',
                        'Coarse_Sun_X': '>f4',
                        'Coarse_Sun_Y': '>f4',
                        'Coarse_Sun_Z': '>f4',
                        'Sun_X': '>f4',
                        'Sun_Y': '>f4',
                        'Sun_Z': '>f4',
                        'Nadir_X': '>f4',
                        'Nadir_Y': '>f4',
                        'Nadir_Z': '>f4',
                        'Angular_Rate_X': '>f4',
                        'Angular_Rate_Y': '>f4',
                        'Angular_Rate_Z': '>f4',
                        'Wheel_Speed_X': '>f4',
                        'Wheel_Speed_Y': '>f4',
                        'Wheel_Speed_Z': '>f4',
                        'Star1b_X': '>f4',
                        'Star1b_Y': '>f4',
                        'Star1b_Z': '>f4',
                        'Star1o_X': '>f4',
                        'Star1o_Y': '>f4',
                        'Star1o_Z': '>f4',
                        'Star2b_X': '>f4',
                        'Star2b_Y': '>f4',
                        'Star2b_Z': '>f4',
                        'Star2o_X': '>f4',
                        'Star2o_Y': '>f4',
                        'Star2o_Z': '>f4',
                        'Star3b_X': '>f4',
                        'Star3b_Y': '>f4',
                        'Star3b_Z': '>f4',
                        'Star3o_X': '>f4',
                        'Star3o_Y': '>f4',
                        'Star3o_Z': '>f4',
                    }
                }
            },
            'ADCS_GET_ACTUATOR': {
                'what': 'Returns actuator commands on-time.',
                'subPort': 71,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Magnetorquer_X_ms/1000': '>f4',
                        'Magnetorquer_Y_ms/1000': '>f4',
                        'Magnetorquer_Z_ms/1000': '>f4',
                        'Wheel_Speed_X': '>f4',
                        'Wheel_Speed_Y': '>f4',
                        'Wheel_Speed_Z': '>f4',
                    }
                }
            },
            'ADCS_GET_ESTIMATION': {
                'what': 'Returns estimation meta-data (Table 152 F/W Ref. Manual).',
                'subPort': 72,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Igrf_magnetic_field_X': '>f4',
                        'Igrf_magnetic_field_Y': '>f4',
                        'Igrf_magnetic_field_Z': '>f4',
                        'Sun_X': '>f4',
                        'Sun_Y': '>f4',
                        'Sun_Z': '>f4',
                        'Gyro_bias_X': '>f4',
                        'Gyro_bias_Y': '>f4',
                        'Gyro_bias_Z': '>f4',
                        'Innovation_X': '>f4',
                        'Innovation_Y': '>f4',
                        'Innovation_Z': '>f4',
                        'Quaternion_Err_X': '>f4',
                        'Quaternion_Err_Y': '>f4',
                        'Quaternion_Err_Z': '>f4',
                        'Quaternion_Covar_X': '>f4',
                        'Quaternion_Covar_X': '>f4',
                        'Quaternion_Covar_X': '>f4',
                        'Angular_Rate_Covar_X': '>f4',
                        'Angular_Rate_Covar_Y': '>f4',
                        'Angular_Rate_Covar_Z': '>f4',
                    }
                }
            },
            'ADCS_GET_ASGP4': {
                'what': 'Get ASGP4 TLEs. (Not using GPS-augmented SGP4, use SGP4 commands instead!).',
                'subPort': 73,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Epoch': '>f4',
                        'Inclination': '>f4',
                        'RAAN': '>f4',
                        'ECC': '>f4',
                        'AOP': '>f4',
                        'MA': '>f4',
                        'MM': '>f4',
                        'Bstar': '>f4',
                    }
                }
            },
            'ADCS_GET_RAW_SENSOR': {
                'what': 'Returns raw sensor measurements (Table 153 F/W Ref. Manual).',
                'subPort': 74,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Cam1_Centroid_X': '>i2',
                        'Cam1_Centroid_Y': '>i2',
                        'Cam1_Capture_Stat': '>u1',
                        'Cam1_Detect_Result': '>u1',
                        'Cam2_Centroid_X': '>i2',
                        'Cam2_Centroid_Y': '>i2',
                        'Cam2_Capture_Stat': '>u1',
                        'Cam2_Detect_Result': '>u1',
                        'Css_1': '>u1',
                        'Css_2': '>u1',
                        'Css_3': '>u1',
                        'Css_4': '>u1',
                        'Css_5': '>u1',
                        'Css_6': '>u1',
                        'Css_7': '>u1',
                        'Css_8': '>u1',
                        'Css_9': '>u1',
                        'Css_10': '>u1',
                        'MTM_X': '>i2',
                        'MTM_Y': '>i2',
                        'MTM_Z': '>i2',
                        'Rate_X': '>i2',
                        'Rate_Y': '>i2',
                        'Rate_Z': '>i2',

                    }
                }
            },
            'ADCS_GET_RAW_GPS': {
                'what': 'Returns raw GPS data (Table 158 F/W Ref. Manual).',
                'subPort': 75,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Sol_Stat': '>u1',
                        'Tracked_Sats': '>u1',
                        'UsedInSol_Sats': '>u1',
                        'Xyz_Lof_Count': '>u1',
                        'Range_Log_Count': '>u1',
                        'Response_Msg': '>u1',
                        'Reference_Week': '>u2',
                        'Time': '>u4',
                        'X_Pos': '>i4',
                        'X_Vel': '>i2',
                        'Y_Pos': '>i4',
                        'Y_Vel': '>i2',
                        'Z_Pos': '>i4',
                        'Z_Vel': '>i2',
                        'Pos_Std_Dev_X': '>f4',
                        'Pos_Std_Dev_Y': '>f4',
                        'Pos_Std_Dev_Z': '>f4',
                        'Vel_Std_Dev_X': '>u1',
                        'Vel_Std_Dev_Y': '>u1',
                        'Vel_Std_Dev_Z': '>u1',
                    }
                }
            },
            'ADCS_GET_STAR_TRACKER': {
                'what': 'Return raw Star Tracker measurements (Table 159 F/W Ref. Manual).',
                'subPort': 76,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Detected_Stars': '>u1',
                        'Img_noise': '>u1',
                        'Invalid_stars': '>u1',
                        'Identified_stars': '>u1',
                        'Identification_mode': '>u1',
                        'Img_dark_val': '>u1',
                        'flags_arr': '>O20',
                        'Sample_T': '>u2',
                        'Star1_Confidence': '>u1',
                        'Star1_magnitude': '>u2',
                        'Star1_Catalouge_Num': '>u2',
                        'Star1_Centroid_X': '>i2',
                        'Star1_Centroid_Y': '>i2',
                        'Star2_Confidence': '>u1',
                        'Star2_magnitude': '>u2',
                        'Star2_Catalouge_Num': '>u2',
                        'Star2_Centroid_X': '>i2',
                        'Star2_Centroid_Y': '>i2',
                        'Star3_Confidence': '>u1',
                        'Star3_magnitude': '>u2',
                        'Star3_Catalouge_Num': '>u2',
                        'Star3_Centroid_X': '>i2',
                        'Star3_Centroid_Y': '>i2',
                        'Capture_T': '>u2',
                        'Detect_T': '>u2',
                        'Identification_T': '>u2',
                        'Estimated_Rate_X': '>f4',
                        'Estimated_Rate_Y': '>f4',
                        'Estimated_Rate_Z': '>f4',
                        'Estimated_Att_X': '>f4',
                        'Estimated_Att_Y': '>f4',
                        'Estimated_Att_Z': '>f4',
                    }
                }
            },
            'ADCS_GET_MTM2_MEASUREMENTS': {
                'what': 'Return raw secondary magnetometer measuremnets.',
                'subPort': 77,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Mag_X': '>i2',
                        'Mag_Y': '>i2',
                        'Mag_Z': '>i2',
                    }
                }
            },
            'ADCS_GET_POWER_TEMP': {
                'what': 'Returns power and temperature measurements (Table 154 F/W Ref. Manual).',
                'subPort': 78,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Cubesense1_3v3_I': '>f4',
                        'Cubesense1_CamSram_I': '>f4',
                        'Cubesense2_3v3_I': '>f4',
                        'Cubesense2_CamSram_I': '>f4',
                        'Cubecontrol_3v3_I': '>f4',
                        'cubecontrol_5v_I': '>f4',
                        'Cubecontrol_vBat_I': '>f4',
                        'wheel1_I': '>f4',
                        'wheel2_I': '>f4',
                        'wheel3_I': '>f4',
                        'Cubestar_I': '>f4',
                        'Magnetorquer_I': '>f4',
                        'Cubestar_Temp': '>f4',
                        'MCU_temp': '>f4',
                        'MTM_temp': '>f4',
                        'MTM2_temp': '>f4',
                        'Rate_Sensor_Temp_X': '>i2',
                        'Rate_Sensor_Temp_Y': '>i2',
                        'Rate_Sensor_Temp_Z': '>i2',
                    }
                }
            },
            'ADCS_SET_POWER_CONTROL': {
                'what': 'Control power to selected components (Table 185 F/W Ref. Manual).',
                'subPort': 79,
                'inoutInfo': {
                    'args': {
                        "CubeCtrl_Sig_Pwr_Sel" : '>u1',
                        "CubeCtrl_Mtr_Pwr_Sel" : '>u1',
                        "CubeSense1_Pwr_Sel" : '>u1',
                        "CubeSense2_Pwr_Sel" : '>u1',
                        "CubeStar_Pwr_Sel" : '>u1',
                        "CubeWheel1_Pwr_Sel" : '>u1',
                        "CubeWheel2_Pwr_Sel" : '>u1',
                        "CubeWheel3_Pwr_Sel" : '>u1',
                        "Mtr_Pwr" : '>u1',
                        "GPS_Pwr" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_GET_POWER_CONTROL': {
                'what': 'Returns component power [0 = OFF, 1 = ON, 2 = Kept same]',
                'subPort': 80,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'CubeCTRLSgn': '>u1',
                        'CubeCTRLMtr': '>u1',
                        'CubeSense1': '>u1',
                        'CubeSense2': '>u1',
                        'CubeStar': '>u1',
                        'CubeWheel1': '>u1',
                        'CubeWheel2': '>u1',
                        'CubeWheel3': '>u1',
                        'Motor': '>u1',
                        'GPS': '>u1',
                    }
                }
            },
            'ADCS_SET_ATTITUDE_ANGLE': {
                'what' : "CHECK DATA SHEET BEFORE USE. xyz ORDER MAY BE WRONG",
                'subPort': 81,
                'inoutInfo': {
                    'args': {
                        'x' : '>f4',
                        'y' : '>f4',
                        'z' : '>f4'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_GET_ATTITUDE_ANGLE': {
                'what': 'Returns commanded attitude angles',
                'subPort': 82,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'X': '>f4',
                        'Y': '>f4',
                        'Z': '>f4'
                    }
                }
            },
            'ADCS_SET_TRACK_CONTROLLER': {
                'what': 'Sets target reference for tracking control mode (Table 186 F/W Ref. Manual).',
                'subPort': 83,
                'inoutInfo': {
                    'args': {
                        'Geocentric_Long' : '>f4',
                        'Geocentric_Lat' : '>f4',
                        'Geocentric_Alt' : '>f4'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_GET_TRACK_CONTROLLER': {
                'what': 'Returns target reference for tracking control mode (Table 186 F/W Ref. Manual).',
                'subPort': 84,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Geocentric_Long' : '>f4',
                        'Geocentric_Lat' : '>f4',
                        'Geocentric_Alt' : '>f4'
                    }
                }
            },
            'ADCS_SET_LOG_CONFIG': {
                "what" : "Hex file assumed for file with name 'file name'",
                'subPort': 85,
                'inoutInfo': {
                    'args': {
                        "Period" : '>u2',
                        "Destination" : '>B',
                        "Log" : '>B',
                        "File_name" : '>S30'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_GET_LOG_CONFIG': {
                'what': 'Returns log config of selected log',
                'subPort': 86,
                'inoutInfo': {
                    'args': {
                        "Log" : '>B'
                    },
                    'returns': {
                        'err': '>b',
                        'Flags_arr': '>V80',
                        'Period': '>u2',
                        'Dest': '>u1',
                        'Log': '>u1'
                    }
                }
            },
            'ADCS_SET_INERTIAL_REF': {
                'what': 'Set reference unit vector for inertial pointing control mode.',
                'subPort': 87,
                'inoutInfo': {
                    'args': {
                        "x" : '>f4',
                        "y" : '>f4',
                        "z" : '>f4'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_GET_INERTIAL_REF': {
                'what': 'Returns reference unit vector for interial pointing control mode.',
                'subPort': 88,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'X': '>f4',
                        'Y': '>f4',
                        'Z': '>f4'
                    }
                }
            },
            'ADCS_SET_SGP4_ORBIT_PARAMS': {
                'what': 'Set SGP4 orbit parameters. Use SAVE_ORBIT_PARAMS to save to flash.',
                'subPort': 89,
                'inoutInfo': {
                    'args': {
                        "inclination" : '>f8',
                        "eccentricity" : '>f8',
                        "RAAN" : '>f8',
                        "AOP" : '>f8',
                        "Bstar" : '>f8',
                        "mean_motion" : '>f8',
                        "mean_anomaly" : '>f8',
                        "epoch" : '>f8',
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_GET_SGP4_ORBIT_PARAMS': {
                'what': 'Returns SGP4 orbit parameters saved on ADCS.',
                'subPort': 90,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Inclination': '>f8',
                        'ECC': '>f8',
                        'RAAN': '>f8',
                        'AOP': '>f8',
                        'Bstar': '>f8',
                        'MM': '>f8',
                        'MA': '>f8',
                        'Epoch': '>f8'
                    }
                }
            },
            'ADCS_SET_SYSTEM_CONFIG': {
                'what': 'Set ADCS system config -- DO NOT EXECUTE UNLESS CONSULTED WITH CUBESPACE',
                'subPort': 91,
                'inoutInfo': {
                    'args': {
                        'Acp_Type': '>u1',
                        'Special_Ctrl_Sel': '>u1',
                        'CC_sig_ver': '>u1',
                        'CC_motor_ver': '>u1',
                        'CS1_ver': '>u1',
                        'CS2_ver': '>u1',
                        'CS1_cam': '>u1',
                        'CS2_cam': '>u1',
                        'CubeStar_Ver': '>u1',
                        'GPS': '>u1',
                        'Include_MTM2': '>?',
                        'MTQ_max_dipole_X': '>f4',
                        'MTQ_max_dipole_Y': '>f4',
                        'MTQ_max_dipole_Z': '>f4',
                        'MTQ_ontime_res': '>f4',
                        'MTQ_max_ontime': '>f4',
                        'RW_max_torque_X': '>f4',
                        'RW_max_torque_Y': '>f4',
                        'RW_max_torque_Z': '>f4',
                        'RW_max_moment_X': '>f4',
                        'RW_max_moment_Y': '>f4',
                        'RW_max_moment_Z': '>f4',
                        'RW_inertia_X': '>f4',
                        'RW_inertia_Y': '>f4',
                        'RW_inertia_Z': '>f4',
                        'RW_torque_inc': '>f4',
                        'MTM1_bias_d1_X': '>f4',
                        'MTM1_bias_d1_Y': '>f4',
                        'MTM1_bias_d1_Z': '>f4',
                        'MTM1_bias_d2_X': '>f4',
                        'MTM1_bias_d2_Y': '>f4',
                        'MTM1_bias_d2_Z': '>f4',
                        'MTM1_sens_s1_X': '>f4',
                        'MTM1_sens_s1_Y': '>f4',
                        'MTM1_sens_s1_Z': '>f4',
                        'MTM1_sens_s2_X': '>f4',
                        'MTM1_sens_s2_Y': '>f4',
                        'MTM1_sens_s2_Z': '>f4',
                        'MTM2_bias_d1_X': '>f4',
                        'MTM2_bias_d1_Y': '>f4',
                        'MTM2_bias_d1_Z': '>f4',
                        'MTM2_bias_d2_X': '>f4',
                        'MTM2_bias_d2_Y': '>f4',
                        'MTM2_bias_d2_Z': '>f4',
                        'MTM2_sens_s1_X': '>f4',
                        'MTM2_sens_s1_Y': '>f4',
                        'MTM2_sens_s1_Z': '>f4',
                        'MTM2_sens_s2_X': '>f4',
                        'MTM2_sens_s2_Y': '>f4',
                        'MTM2_sens_s2_Z': '>f4',
                        'CC_Signal_Port': '>u1',
                        'CC_Signal_Pin': '>u1',
                        'CC_Motor_Port': '>u1',
                        'CC_Motor_Pin': '>u1',
                        'CC_Common_Port': '>u1',
                        'CC_Common_Pin': '>u1',
                        'CS1_Port': '>u1',
                        'CS1_Pin': '>u1',
                        'CS2_Port': '>u1',
                        'CS2_Pin': '>u1',
                        'CubeStar_Port': '>u1',
                        'CubeStar_Pin': '>u1',
                        'CW1_Port': '>u1',
                        'CW1_Pin': '>u1',
                        'CW2_Port': '>u1',
                        'CW2_Pin': '>u1',
                        'CW3_Port': '>u1',
                        'CW3_Pin': '>u1',
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_GET_SYSTEM_CONFIG': {
                'what': 'Returns the hard-coded system configuration (Tabbles 201-207 F/W Ref. Manual).',
                'subPort': 92,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Acp_Type': '>u1',
                        'Special_Ctrl_Sel': '>u1',
                        'CC_sig_ver': '>u1',
                        'CC_motor_ver': '>u1',
                        'CS1_ver': '>u1',
                        'CS2_ver': '>u1',
                        'CS1_cam': '>u1',
                        'CS2_cam': '>u1',
                        'CubeStar_Ver': '>u1',
                        'GPS': '>u1',
                        'Include_MTM2': '>?',
                        'MTQ_max_dipole_X': '>f4',
                        'MTQ_max_dipole_Y': '>f4',
                        'MTQ_max_dipole_Z': '>f4',
                        'MTQ_ontime_res': '>f4',
                        'MTQ_max_ontime': '>f4',
                        'RW_max_torque_X': '>f4',
                        'RW_max_torque_Y': '>f4',
                        'RW_max_torque_Z': '>f4',
                        'RW_max_moment_X': '>f4',
                        'RW_max_moment_Y': '>f4',
                        'RW_max_moment_Z': '>f4',
                        'RW_inertia_X': '>f4',
                        'RW_inertia_Y': '>f4',
                        'RW_inertia_Z': '>f4',
                        'RW_torque_inc': '>f4',
                        'MTM1_bias_d1_X': '>f4',
                        'MTM1_bias_d1_Y': '>f4',
                        'MTM1_bias_d1_Z': '>f4',
                        'MTM1_bias_d2_X': '>f4',
                        'MTM1_bias_d2_Y': '>f4',
                        'MTM1_bias_d2_Z': '>f4',
                        'MTM1_sens_s1_X': '>f4',
                        'MTM1_sens_s1_Y': '>f4',
                        'MTM1_sens_s1_Z': '>f4',
                        'MTM1_sens_s2_X': '>f4',
                        'MTM1_sens_s2_Y': '>f4',
                        'MTM1_sens_s2_Z': '>f4',
                        'MTM2_bias_d1_X': '>f4',
                        'MTM2_bias_d1_Y': '>f4',
                        'MTM2_bias_d1_Z': '>f4',
                        'MTM2_bias_d2_X': '>f4',
                        'MTM2_bias_d2_Y': '>f4',
                        'MTM2_bias_d2_Z': '>f4',
                        'MTM2_sens_s1_X': '>f4',
                        'MTM2_sens_s1_Y': '>f4',
                        'MTM2_sens_s1_Z': '>f4',
                        'MTM2_sens_s2_X': '>f4',
                        'MTM2_sens_s2_Y': '>f4',
                        'MTM2_sens_s2_Z': '>f4',
                        'CC_Signal_Port': '>u1',
                        'CC_Signal_Pin': '>u1',
                        'CC_Motor_Port': '>u1',
                        'CC_Motor_Pin': '>u1',
                        'CC_Common_Port': '>u1',
                        'CC_Common_Pin': '>u1',
                        'CS1_Port': '>u1',
                        'CS1_Pin': '>u1',
                        'CS2_Port': '>u1',
                        'CS2_Pin': '>u1',
                        'CubeStar_Port': '>u1',
                        'CubeStar_Pin': '>u1',
                        'CW1_Port': '>u1',
                        'CW1_Pin': '>u1',
                        'CW2_Port': '>u1',
                        'CW2_Pin': '>u1',
                        'CW3_Port': '>u1',
                        'CW3_Pin': '>u1',
                    }
                }
            },
            'ADCS_SET_MTQ_CONFIG': {
                'what': 'Set magnetorquer axes. Keep default (values found in ADCS Flight Config sheet).',
                'subPort': 93,
                'inoutInfo': {
                    'args': {
                        "Mag1_axis" : '>u1',
                        "Mag2_axis" : '>u1',
                        "Mag3_axis" : '>u1'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'ADCS_SET_RW_CONFIG': {
                'what': 'Sets wheel axes (Table 180 F/W Ref. Manual).',
                'subPort': 94,
                'inoutInfo': {
                    'args': {
                        "RW1_axis" : '>u1',
                        "RW2_axis" : '>u1',
                        "RW3_axis" : '>u1',
                        "RW4_axis" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_RATE_GYRO': {
                'what': 'Set rate gyro config parameters. Keep default (values provided in ADCS Flight Config Sheet).',
                'subPort': 95,
                'inoutInfo': {
                    'args': {
                        "Gyro1_axis" : '>u1',
                        "Gyro2_axis" : '>u1',
                        "Gyro3_axis" : '>u1',
                        "X_sensor_offset" : '>f4',
                        "Y_sensor_offset" : '>f4',
                        "Z_sensor_offset" : '>f4',
                        "Rate_Sensor_Mult" : '>u1',
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_CSS_CONFIG': {
                "what" : "CSS relative scale floats cannot be negative!",
                'subPort': 96,
                'inoutInfo': {
                    'args': {
                        "CSS1_axis" : '>B',
                        "CSS2_axis" : '>B',
                        "CSS3_axis" : '>B',
                        "CSS4_axis" : '>B',
                        "CSS5_axis" : '>B',
                        "CSS6_axis" : '>B',
                        "CSS7_axis" : '>B',
                        "CSS8_axis" : '>B',
                        "CSS9_axis" : '>B',
                        "CSS10_axis" : '>B',
                        "CSS1_rel_scale" : '>f4',
                        "CSS2_rel_scale" : '>f4',
                        "CSS3_rel_scale" : '>f4',
                        "CSS4_rel_scale" : '>f4',
                        "CSS5_rel_scale" : '>f4',
                        "CSS6_rel_scale" : '>f4',
                        "CSS7_rel_scale" : '>f4',
                        "CSS8_rel_scale" : '>f4',
                        "CSS0_rel_scale" : '>f4',
                        "CSS10_rel_scale" : '>f4',
                        "CSS_threshold" : '>B'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_STAR_TRACK_CONFIG': {
                'what': 'Star Tracker not used.',
                'subPort': 97,
                'inoutInfo': {
                    'args': { #TODO Better names
                        "Float1" : '>f4',
                        "Float2" : '>f4',
                        "Float3" : '>f4',
                        "Arg1" : '>u2',
                        "Arg2" : '>u2',
                        "Arg3" : '>u1',
                        "Arg4" : '>u1',
                        "Arg5" : '>u1',
                        "Arg6" : '>u2',
                        "Arg7" : '>u1',
                        "Arg8" : '>u1',
                        "Arg9" : '>u1',
                        "Float4" : '>f4',
                        "Float5" : '>f4',
                        "Float6" : '>f4',
                        "Float7" : '>f4',
                        "Float8" : '>f4',
                        "Float9" : '>f4',
                        "Float10" : '>f4',
                        "Arg10" : '>u1',
                        "Arg11" : '>u1',
                        "Arg12" : '>u1',
                        "Arg13" : '>u?',
                        "Arg14" : '>u?',
                        "Arg15" : '>u1',

                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_CUBESENSE_CONFIG': {
                'what': 'Set CubeSense config parameters (Table 189 F/W Ref. Manual). Cam1 parameters to be kept default -- Cam2 TBD in orbit.',
                'subPort': 98,
                'inoutInfo': {
                    'args': {
                        "Config" : '>S30'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_MTM_CONFIG': {
                'what': 'Sets the magnetometer configuration parameters. Input: Angle xyz (floats), channel_offset xyz (floats), sensitivity matrix (s11,s22,s33,s12,s13,s21,s23,s31,s32)',
                'subPort': 99,
                'inoutInfo': {
                    'args': {
                        "angle_x" : '>f4',
                        "angle_y" : '>f4',
                        "angle_z" : '>f4',
                        "channel_x" : '>f4',
                        "channel_y" : '>f4',
                        "channel_z" : '>f4',
                        "s11" : '>f4',
                        "s22" : '>f4',
                        "s33" : '>f4',
                        "s12" : '>f4',
                        "s13" : '>f4',
                        "s21" : '>f4',
                        "s23" : '>f4',
                        "s31" : '>f4',
                        "s32" : '>f4',
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_DETUMBLE_CONFIG': {
                'what': 'Set control parameters for Detumbling mode. Values TBD from sims and/or commissioning.',
                'subPort': 100,
                'inoutInfo': {
                    'args': {
                        "Detumble_Spin_Gain" : '>f4',
                        "Detumble_Damp_Gain" : '>f4',
                        "Ref_Spin_Rate" : '>f4',
                        "Fast_Bdot_Detumble_Gain" : '>f4',
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_YWHEEL_CONFIG': {
                'what': 'Set control parameters for Y-wheel control mode. Values TBD from sims and commissioning.',
                'subPort': 101,
                'inoutInfo': {
                    'args': {
                        "Ymoment_Ctrl_Gain" : '>f4',
                        "Ymoment_Damp_Gain" : '>f4',
                        "Ymoment_Prop_Gain" : '>f4',
                        "Ymoment_Deriv_Gain" : '>f4',
                        "Ref_Wheel_Moment" : '>f4',
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_RWHEEL_CONFIG': {
                'what': 'Set control parameters for reaction wheel mode. Values TBD from sims and/or commissioning.',
                'subPort': 102,
                'inoutInfo': {
                    'args': {
                        "RWheel_Prop_Gain" : '>f4',
                        "RWheel_Deriv_Gain" : '>f4',
                        "YWheel_Bias_Moment" : '>f4',
                        "Sun_Point_Facet" : '>B',
                        "Auto_Ctrl_Transit" : '>B'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_TRACKING_CONFIG': {
                'what': 'Set control parameters for tracking mode. Values TBD from sims and/or commissioning.',
                'subPort': 103,
                'inoutInfo': {
                    'args': {
                        "Track_Prop_Gain" : '>f4',
                        "Track_Deriv_Gain" : '>f4',
                        "Track_Intgrl_Gain" : '>f4',
                        "Trgt_Track_Facet" : '>B'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_MOI_MAT': {
                'what': 'Sets satellite moment of inertia matrix.',
                'subPort': 104,
                'inoutInfo': {
                    'args': {
                        "Ixx" : '>f4',
                        "Iyy" : '>f4',
                        "Izz" : '>f4',
                        "Ixy" : '>f4',
                        "Ixz" : '>f4',
                        "Iyz" : '>f4',
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_ESTIMATION_CONFIG': {
                'what': 'Sets estimation noise covariance and sensor mask (Table 200 F/W Ref. Manual). Consult with CubeSpace before executing.',
                'subPort': 105,
                'inoutInfo': {
                    'args': {
                        "Mtm_Rt_Fltr_Sys_Noise" : '>f4',
                        "EKF_Sys_Noise" : '>f4',
                        "CSS_Msrmnt_Noise" : '>f4',
                        "Sun_Snsr_Msrmnt_Noise" : '>f4',
                        "Ndr_Snsr_Msrmnt_Noise" : '>f4',
                        "Mtm_Snsr_Msrmnt_Noise" : '>f4',
                        "Strtrckr_Msrmnt_Noise" : '>f4',
                        "Use_Sun_Sensor" : '>u1',
                        "Use_Nadir_Sensor" : '>u1',
                        "Use_CSS" : '>u1',
                        "Use_Star_Tracker" : '>u1',
                        "Ndr_Snsr_Trmntr_Tst" : '>u1',
                        "Auto_Mtm_Rcvry" : '>u1',
                        "Mtm_Sel1" : '>u1',
                        "Mtm_Sel2" : '>u1', # MTM selection done by ORing with last two elements in select_arr
                        "Mtm_Mode" : '>u1',
                        "Auto_Est_Trans" : '>u1',
                        "Cam_Sample_Period" : '>u1'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_USERCODED_SETTING': {
                'what': 'Set user-coded estimation and control modes.',
                'subPort': 106,
                'inoutInfo': {
                    'args': {
                        "User_Ctrlr_Set" : '>O20',
                        "User_Estim_Set" : '>020'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_SET_ASGP4_SETTING': {
                'what': 'Set ASGP4 settings (Not using GPS-augmented SGP4, use SGP4 commands instead!).',
                'subPort': 107,
                'inoutInfo': {
                    'args': {
                        "Float1" : '>f4',
                        "Float2" : '>f4',
                        "Float3" : '>f4',
                        "Float4" : '>f4',
                        "Float5" : '>f4',
                        "Float6" : '>f4',
                        "Float7" : '>f4',
                        "Arg1" : '>u1',
                        "Float8" : '>f4',
                        "Float9" : '>f4',
                        "Arg2" : '>u1',
                        "Float10" : '>f4',
                        "Float11" : '>f4',
                        "Arg3" : '>u1',
                        "Float12" : '>f4',
                        "Float13" : '>f4',
                        "Arg4" : '>u2',
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_GET_FULL_CONFIG': {
                'what': 'Returns ADCS full config (Table 192 F/W Ref. Manual).',
                'subPort': 108,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'MTQ_x': '>B',
                        'MTQ_y': '>B',
                        'MTQ_z': '>B',
                        'RW1': '>B',
                        'RW2': '>B',
                        'RW3': '>B',
                        'RW4': '>B',
                        'gyro_x': '>B',
                        'gyro_y': '>B',
                        'gyro_z': '>B',
                        'sensor_offset_x': '>f4',
                        'sensor_offset_y': '>f4',
                        'sensor_offset_z': '>f4',
                        'rate_sensor_mult': '>B',
                        'css_config1': '>B',
                        'css_config2': '>B',
                        'css_config3': '>B',
                        'css_config4': '>B',
                        'css_config5': '>B',
                        'css_config6': '>B',
                        'css_config7': '>B',
                        'css_config8': '>B',
                        'css_config9': '>B',
                        'css_config10': '>B',
                        'css_relscale1': '>f4',
                        'css_relscale2': '>f4',
                        'css_relscale3': '>f4',
                        'css_relscale4': '>f4',
                        'css_relscale5': '>f4',
                        'css_relscale6': '>f4',
                        'css_relscale7': '>f4',
                        'css_relscale8': '>f4',
                        'css_relscale9': '>f4',
                        'css_relscale10': '>f4',
                        'css_threshold': '>B',
                        'cs1_mnt_angle_x': '>f4',
                        'cs1_mnt_angle_y': '>f4',
                        'cs1_mnt_angle_z': '>f4',
                        'cs1_detect_th': '>B',
                        'cs1_auto_adjust': '>?',
                        'cs1_exposure_t': '>u2',
                        'cs1_boresight_x': '>f4',
                        'cs1_boresight_y': '>f4',
                        'cs2_mnt_angle_x': '>f4',
                        'cs2_mnt_angle_y': '>f4',
                        'cs2_mnt_angle_z': '>f4',
                        'cs2_detect_th': '>B',
                        'cs2_auto_adjust': '>?',
                        'cs2_exposure_t': '>u2',
                        'cs2_boresight_x': '>f4',
                        'cs2_boresight_y': '>f4',
                        'nadir_max_deviate': '>B',
                        'nadir_max_bad_edge': '>B',
                        'nadir_max_radius': '>B',
                        'nadir_min_radius': '>B',
                        'cam1_area_1_x_min': '>u2',
                        'cam1_area_1_x_max': '>u2',
                        'cam1_area_1_y_min': '>u2',
                        'cam1_area_1_y_max': '>u2',
                        'cam1_area_2_x_min': '>u2',
                        'cam1_area_2_x_max': '>u2',
                        'cam1_area_2_y_min': '>u2',
                        'cam1_area_2_y_max': '>u2',
                        'cam1_area_3_x_min': '>u2',
                        'cam1_area_3_x_max': '>u2',
                        'cam1_area_3_y_min': '>u2',
                        'cam1_area_3_y_max': '>u2',
                        'cam1_area_4_x_min': '>u2',
                        'cam1_area_4_x_max': '>u2',
                        'cam1_area_4_y_min': '>u2',
                        'cam1_area_4_y_max': '>u2',
                        'cam1_area_5_x_min': '>u2',
                        'cam1_area_5_x_max': '>u2',
                        'cam1_area_5_y_min': '>u2',
                        'cam1_area_5_y_max': '>u2',
                        'cam2_area_1_x_min': '>u2',
                        'cam2_area_1_x_max': '>u2',
                        'cam2_area_1_y_min': '>u2',
                        'cam2_area_1_y_max': '>u2',
                        'cam2_area_2_x_min': '>u2',
                        'cam2_area_2_x_max': '>u2',
                        'cam2_area_2_y_min': '>u2',
                        'cam2_area_2_y_max': '>u2',
                        'cam2_area_3_x_min': '>u2',
                        'cam2_area_3_x_max': '>u2',
                        'cam2_area_3_y_min': '>u2',
                        'cam2_area_3_y_max': '>u2',
                        'cam2_area_4_x_min': '>u2',
                        'cam2_area_4_x_max': '>u2',
                        'cam2_area_4_y_min': '>u2',
                        'cam2_area_4_y_max': '>u2',
                        'cam2_area_5_x_min': '>u2',
                        'cam2_area_5_x_max': '>u2',
                        'cam2_area_5_y_min': '>u2',
                        'cam2_area_5_y_max': '>u2',
                        'MTM1_mount_angle_x': '>f4',
                        'MTM1_mount_angle_y': '>f4',
                        'MTM1_mount_angle_z': '>f4',
                        'MTM1_channel_offset_x': '>f4',
                        'MTM1_channel_offset_y': '>f4',
                        'MTM1_channel_offset_z': '>f4',
                        'MTM1_sensitivity_mat_1': '>f4',
                        'MTM1_sensitivity_mat_2': '>f4',
                        'MTM1_sensitivity_mat_3': '>f4',
                        'MTM1_sensitivity_mat_4': '>f4',
                        'MTM1_sensitivity_mat_5': '>f4',
                        'MTM1_sensitivity_mat_6': '>f4',
                        'MTM1_sensitivity_mat_7': '>f4',
                        'MTM1_sensitivity_mat_8': '>f4',
                        'MTM1_sensitivity_mat_9': '>f4',
                        'MTM2_mount_angle_x': '>f4',
                        'MTM2_mount_angle_y': '>f4',
                        'MTM2_mount_angle_z': '>f4',
                        'MTM2_channel_offset_x': '>f4',
                        'MTM2_channel_offset_y': '>f4',
                        'MTM2_channel_offset_z': '>f4',
                        'MTM2_sensitivity_mat_1': '>f4',
                        'MTM2_sensitivity_mat_2': '>f4',
                        'MTM2_sensitivity_mat_3': '>f4',
                        'MTM2_sensitivity_mat_4': '>f4',
                        'MTM2_sensitivity_mat_5': '>f4',
                        'MTM2_sensitivity_mat_6': '>f4',
                        'MTM2_sensitivity_mat_7': '>f4',
                        'MTM2_sensitivity_mat_8': '>f4',
                        'MTM2_sensitivity_mat_9': '>f4',
                        'cubestar_mounting_angle_x': '>f4',
                        'cubestar_mounting_angle_y': '>f4',
                        'cubestar_mounting_angle_z': '>f4',
                        'cubestar_exposure_t': '>u2',
                        'cubestar_analog_gain': '>u2',
                        'cubestar_detect_th': '>B',
                        'cubestar_star_th': '>B',
                        'cubestar_max_star_matched': '>B',
                        'cubestar_detect_timeout_t': '>u2',
                        'cubestar_max_pixel': '>B',
                        'cubestar_min_pixel': '>B',
                        'cubestar_err_margin': '>B',
                        'cubestar_delay_t': '>u2',
                        'cubestar_centroid_x': '>f4',
                        'cubestar_centroid_y': '>f4',
                        'cubestar_focal_len': '>f4',
                        'cubestar_radical_distor_1': '>f4',
                        'cubestar_radical_distor_2': '>f4',
                        'cubestar_tangent_distor_1': '>f4',
                        'cubestar_tangent_distor_2': '>f4',
                        'cubestar_window_wid': '>B',
                        'cubestar_track_margin': '>B',
                        'cubestar_valid_margin': '>B',
                        'cubestar_module_en': '>?',
                        'cubestar_loc_predict_en': '>?',
                        'cubestar_search_wid': '>B',
                        'detumble_spin_gain': '>f4',
                        'detumble_damping_gain': '>f4',
                        'detumble_spin_rate': '>f4',
                        'detumble_fast_bDot': '>f4',
                        'ywheel_control_gain': '>f4',
                        'ywheel_damping_gain': '>f4',
                        'ywheel_proportional_gain': '>f4',
                        'ywheel_derivative_gain': '>f4',
                        'ywheel_reference': '>f4',
                        'rwheel_proportional_gain': '>f4',
                        'rwheel_derivative_gain': '>f4',
                        'rwheel_bias_moment': '>f4',
                        'rwheel_sun_point_facet': '>B',
                        'rwheel_auto_transit': '>?',
                        'tracking_proportional_gain': '>f4',
                        'tracking_derivative_gain': '>f4',
                        'tracking_integral_gain': '>f4',
                        'tracking_target_facet': '>B',
                        'MoI_config_diag_x': '>f4',
                        'MoI_config_diag_y': '>f4',
                        'MoI_config_diag_z': '>f4',
                        'MoI_config_nondiag_x': '>f4',
                        'MoI_config_nondiag_y': '>f4',
                        'MoI_config_nondiag_z': '>f4',
                        'est_MTM_rate_noise': '>f4',
                        'est_EKF_noise': '>f4',
                        'est_CSS_noise': '>f4',
                        'est_sun_sensor_noise': '>f4',
                        'est_nadir_sensor_noise': '>f4',
                        'est_MTM_noise': '>f4',
                        'est_star_track_noise': '>f4',
                        'est_select_arr_1': '>B',
                        'est_select_arr_2': '>B',
                        'est_select_arr_3': '>B',
                        'est_select_arr_4': '>B',
                        'est_select_arr_5': '>B',
                        'est_select_arr_6': '>B',
                        'est_select_arr_7': '>B',
                        'est_select_arr_8': '>B',
                        'est_MTM_mode': '>B',
                        'est_MTM_select': '>B',
                        'est_cam_sample_period': '>B',
                        'asgp4_inclination': '>f4',
                        'asgp4_RAAN': '>f4',
                        'asgp4_ECC': '>f4',
                        'asgp4_AoP': '>f4',
                        'asgp4_time': '>f4',
                        'asgp4_pos': '>f4',
                        'asgp4_max_pos_err': '>f4',
                        'asgp4_filter': '>B',
                        'asgp4_xp': '>f4',
                        'asgp4_yp': '>f4',
                        'asgp4_gps_rollover': '>B',
                        'asgp4_pos_sd': '>f4',
                        'asgp4_vel_sd': '>f4',
                        'asgp4_min_stat': '>B',
                        'asgp4_time_gain': '>f4',
                        'asgp4_max_lag': '>f4',
                        'asgp4_min_samples': '>u2',
                        'usercoded_controller': '>V48',
                        'usercoded_estimator': '>V48'
                    }
                }
            },
            'ADCS_DOWNLOAD_FILE_LIST_TO_OBC': {
                'what': 'Saves information about files stored on the ADCS to the OBC. File name VOL0:/adcs/adcs_file_list.txt',
                'subPort': 109,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'ADCS_DOWNLOAD_FILE_TO_OBC': {
                'what': 'Saves a file from the ADCS to the OBC. Inputs: type, counter, size, and OBC file name. (Be patient and check the log for return.)',
                'subPort': 110,
                'inoutInfo': {
                    'args': {
                        "Type" : '>B',
                        "Counter" : '>B',
                        "Size" : '>u4',
                        "File_name" : '>S30'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
        }
    },
    'DFGM': {
        'supports' : ("OBC",),
        'port': 19,
        'subservice': {
            'DFGM_RUN': {
                'what': 'Record DFGM data for specified number of seconds.',
                'subPort': 0,
                'inoutInfo': {
                    'args': {
                        "Seconds" : '>u4'
                    },
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'DFGM_START': {
                'what': 'Start recording DFGM data',
                'subPort': 1,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'DFGM_STOP': {
                'what': 'Stop recording DFGM data.',
                'subPort': 2,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'DFGM_GET_HK': {
                'subPort': 3,
                'inoutInfo': {
                    'what': 'Fetch housekeeping data for the DFGM payload.',
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Core Voltage': '>u2',
                        'Sensor Temperature': '>u2',
                        'Reference Temperature': '>u2',
                        'Board Temperature': '>u2',
                        'Positive Rail Voltage': '>u2',
                        'Input Voltage': '>u2',
                        'Reference Voltage': '>u2',
                        'Input Current': '>u2',
                        'Reserved 1': '>u2',
                        'Reserved 2': '>u2',
                        'Reserved 3': '>u2',
                        'Reserved 4': '>u2',
                    }
                }
            }
        }
    },
    "FTP_COMMAND": {
        'supports' : ("OBC",),
        'port': 20,
        'subservice': {
            'GET_FILE_SIZE': {
                'subPort': 0,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'size': '>u8',
                    }
                }
            },
            'REQUEST_BURST_DOWNLOAD': {
                'subPort': 1,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'mtime': '>u4',
                        'ctime': '>u4',
                    }
                }
            },
            'FTP_DATA_PACKET': {
                'subPort': 2,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'req_id': '>u4',
                        'size': '>u4',
                        'blocknum': '>u2',
                        'data': 'var'
                    }
                }
            },
            'FTP_START_UPLOAD': {
                'subPort': 3,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'FTP_UPLOAD_PACKET': {
                'subPort': 4,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
        }
    },
    'NS_PAYLOAD': {
        'supports' : ("OBC",),
        'port': 22,
        'subservice': {
            'UPLOAD_ARTWORK': {
                'what': 'Send artwork from the OBC to the payload. Input: file name, limited to 7 chars!',
                'subPort': 0,
                'inoutInfo': {
                    'args': {
                        "FIlename" : '>S10'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'CAPTURE_IMAGE': {
                'what': 'Tell the payload to display artwork and capture an image.',
                'subPort': 1,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'confirmation_err': '>B'
                    }
                }
            },
            'CONFIRM_DOWNLINK': {
                'what': 'Let the payload know that the last image it took was received by the ground and can be deleted.',
                'subPort': 2,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },

            'GET_HEARTBEAT': {
                'what': 'Receive a ping (char h) from the payload',
                'subPort': 3,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'heartbeat': '>S1'
                    }
                }
            },
            'GET_FLAG': {
                'what': 'Get the status of a payload flag. Input: flag/subcode decimal value. flag/subcode BYTE! Do not use a char',
                'subPort': 4,
                'inoutInfo': {
                    'args': {
                        "Flag" : '>B'
                    },
                    'returns': {
                        'err': '>b',
                        'flag_stat': '>B'
                    }
                }
            },
            'GET_FILENAME': {
                'what': 'Get a desired image/artwork file name. Input: subcode demimal value. subcode BYTE! Do not use a char',
                'subPort': 5,
                'inoutInfo': {
                    'args': {
                        "Subcode" : '>B'
                    },
                    'returns': {
                        'err': '>b',
                        'filename': '>S11'
                    }
                }
            },
            'GET_TELEMETRY': {
                'what': 'Get telemetry data from the payload',
                'subPort': 6,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'temp0': '>i2',
                        'temp1': '>i2',
                        'temp2': '>i2',
                        'temp3': '>i2',
                        'eNIM0_lux': '>i2',
                        'eNIM1_lux': '>i2',
                        'eNIM2_lux': '>i2',
                        'eNIM3_lux': '>i2',
                        'ram_avail': '>i2',
                        'lowest_img_num': '>i2',
                        'first_blank_img_num': '>i2'
                    }
                }
            },
            'GET_SW_VERSION': {
                'what': 'Get payload software version.',
                'subPort': 7,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'version': '>S7'
                    }
                }
            },
            'DOWNLOAD_IMAGE': {
                'what': 'Download payload image to OBC',
                'subPort': 8,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'CLEAR_SD_CARD': {
                'what': 'Clear NIM\'s sd card',
                'subPort': 9,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'RESET_MCU': {
                'what': 'Reset NIM\'s MCU',
                'subPort': 10,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'NV_START': {
                'what': 'Start transmitting voice data from filename. Blocksize should be a multiple of the blocksize of the codec and reasonably large (max 512)',
                'subPort': 11,
                'inoutInfo': {
                    'args': {
                        "Repeats": '>u2',
                        "Blocksize": '>u2',
                        "Filename" : '>S128'
                    },
                    'returns': {
                        'err': '>b',
                    }
                }
            },
            'NV_STOP': {
                'what': 'Stop transmitting voice data',
                'subPort': 12,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                    }
                }
            },
        },
    },
    'IRIS': {
        'supports' : ("OBC",),
        'port': 23,
        'subservice': {
            'IRIS_POWER_ON': {
                'what': "Send command to OBC to tell EPS to turn on power",
                'subPort': 0,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'IRIS_POWER_OFF': {
                'what': "Send command to OBC to tell EPS to turn off power",
                'subPort': 1,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'IRIS_TURN_SENSORS_ON': {
                'what': "Send command to OBC to tell Iris to turn on image sensors",
                'subPort': 2,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'IRIS_TURN_SENSORS_OFF': {
                'what': "Send command to OBC to tell Iris to turn off image sensors",
                'subPort': 3,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'IRIS_TAKE_IMAGE': {
                'what': "Tell Iris to take a picture",
                'subPort': 4,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'IRIS_DELIVER_IMAGE': {
                'what': "Tell OBC to perform image transfer from Iris and store those images into SD card",
                'subPort': 5,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'IRIS_COUNT_IMAGES': {
                'what': "Tell Iris to send number of images stored in SD card",
                'subPort': 6,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'IRIS_PROGRAM_FLASH': {
                'what': "Tell OBC to start programming Iris using provided binary file on the SD card",
                'subPort': 7,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'Number of Images': '>u',
                    }
                }
            },
            'IRIS_GET_HK': {
                'what': "Tell Iris to send housekeeping data",
                'subPort': 8,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b',
                        'VIS_Temperature': '>f4',
                        'NIR_Temperature': '>f4',
                        'Flash_Temperature': '>f4',
                        'Gate_Temperature': '>f4',
                        'Image_number': '>u1',
                        'Software_Version': '>u1',
                        'Error_number': '>u1',
                        'MAX_5V_voltage': '>u2',
                        'MAX_5V_power': '>u2',
                        'MAX_3V_voltage': '>u2',
                        'MAX_3V_power': '>u2',
                        'MIN_5V_voltage': '>u2',
                        'MIN_3V_voltage': '>u2',
                    }
                }
            },
            'IRIS_DELIVER_LOG': {
                'what': "Tell OBC to perform log transfer from Iris and store it into SD card",
                'subPort': 9,
                'inoutInfo': {
                    'args': None,
                    'returns': {
                        'err': '>b'
                    }
                }
            },
            'IRIS_SET_TIME': {
                'what': "Initialize Iris RTC from ground station via OBC",
                'subPort': 10,
                'inoutInfo': {
                    'args': {"new_iris_time": '>u4'},
                    'returns': {
                        'err': '>b'
                    }
                }
            }
        },
    },
    'BEACON_RX': {
        'supports' : ("GND",),
        'port': 1,
        'subservice': {
            'BEACON_PCKT_1': {
                'what': "Struct definition for beacon packet 1 decoding",
                'subPort': 1,
                'inoutInfo':{
                    'args': None,
                    'returns': {
                        "time": '>u4',
                        "packet_number": '>u1',
                        "switch_stat": '>u1',
                        "eps_mode": '>u1',
                        "battery_voltage": '>u2',
                        "battery_input_current": '>u2',
                        "current_channel_1": '>u2',
                        "current_channel_2": '>u2',
                        "current_channel_3": '>u2',
                        "current_channel_4": '>u2',
                        "current_channel_5": '>u2',
                        "current_channel_6": '>u2',
                        "current_channel_7": '>u2',
                        "current_channel_8": '>u2',
                        "current_channel_9": '>u2',
                        "current_channel_10": '>u2',
                        "output_status": '>u2',
                        "output_faults_1": '>u1',
                        "output_faults_2": '>u1',
                        "output_faults_3": '>u1',
                        "output_faults_4": '>u1',
                        "output_faults_5": '>u1',
                        "output_faults_6": '>u1',
                        "output_faults_7": '>u1',
                        "output_faults_8": '>u1',
                        "output_faults_9": '>u1',
                        "output_faults_10": '>u1',
                        "EPS_boot_count": '>u2',
                        "eps_last_reset_reason": '>u1',
                        "gs_wdt_time": '>u4',
                        "gs_wdt_cnt": '>u1',
                        "obc_wdt_toggles": '>u1',
                        "obc_wdt_turnoffs": '>u1',
                    },
                },
            },
            'BEACON_PCKT_2': {
                'what': "Struct definition for beacon packet 2 decoding",
                'subPort': 2,
                'inoutInfo':{
                    'args': None,
                    'returns': {
                        "time": '>u4',
                        "packet_number": '>u1',
                        "temp_1": '>i1',
                        "temp_2": '>i1',
                        "temp_3": '>i1',
                        "temp_4": '>i1',
                        "temp_5": '>i1',
                        "temp_6": '>i1',
                        "temp_7": '>i1',
                        "temp_8": '>i1',
                        "temp_9": '>i1',
                        "temp_10": '>i1',
                        "temp_11": '>i1',
                        "temp_12": '>i1',
                        "temp_13": '>i1',
                        "temp_14": '>i1',
                        "temp_15": '>i1',
                        "temp_16": '>i1',
                        "temp_17": '>i1',
                        "angular_rate_X": '>i1',
                        "angular_rate_Y": '>i1',
                        "angular_rate_Z": '>i1',
                        "adcs_control_mode": '>i1',
                        "uhf_uptime": '>u4',
                        "obc_boot_count": '>u2',
                        "obc_last_reset_reason": '>u1',
                        "obc_uptime": '>u4',
                        "solar_panel_supply_current": '>u1',
                        "obc_software_version": '>u1',
                        "cmds_received": '>u2',
                    }
                }
            }
        }
    }
}
