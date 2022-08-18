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
 * @file expected_adcs_hk.py
 * @author Jenish Patel
 * @date 2022-08-08
'''

expected_ADCS_HK = {
    'Estimated_Angular_Rate_X': [0, 1],
    'Estimated_Angular_Rate_Y': [0, 1],
    'Estimated_Angular_Rate_Z': [0, 1],
    'Estimated_Angular_Angle_X': [-180, 180],
    'Estimated_Angular_Angle_Y': [-180, 180],
    'Estimated_Angular_Angle_Z': [-180, 180],
    'Sat_Position_ECI_X': [-10000, 10000],
    'Sat_Position_ECI_Y': [-10000, 10000],
    'Sat_Position_ECI_Z': [-10000, 10000],
    'Sat_Velocity_ECI_X': [-10000, 10000],
    'Sat_Velocity_ECI_Y': [-10000, 10000],
    'Sat_Velocity_ECI_Z': [-10000, 10000],
    'Sat_Position_LLH_X': [-90, 90], # Latitude
    'Sat_Position_LLH_Y': [-180, 180], # Longitude
    'Sat_Position_LLH_Z': [0, 1],
    'ECEF_Position_X': [0, 1],
    'ECEF_Position_Y': [0, 1],
    'ECEF_Position_Z': [0, 1],
    'Coarse_Sun_Vector_X': [0, 1],
    'Coarse_Sun_Vector_Y': [0, 1],
    'Coarse_Sun_Vector_Z': [0, 1],
    'Fine_Sun_Vector_X': [0, 1],
    'Fine_Sun_Vector_Y': [0, 1],
    'Fine_Sun_Vector_Z': [0, 1],
    'Nadir_Vector_X': [0, 1],
    'Nadir_Vector_Y': [0, 1],
    'Nadir_Vector_Z': [0, 1],
    'Wheel_Speed_X': [0, 1],
    'Wheel_Speed_Y': [0, 1],
    'Wheel_Speed_Z': [0, 1],
    'Mag_Field_Vector_X': [0, 1],
    'Mag_Field_Vector_Y': [0, 1],
    'Mag_Field_Vector_Z': [0, 1],
    'TC_num': [0, 1],
    'TM_num': [0, 1],
    'CommsStat_flags_1': [0, 1],
    'CommsStat_flags_2': [0, 1],
    'CommsStat_flags_3': [0, 1],
    'CommsStat_flags_4': [0, 1],
    'CommsStat_flags_5': [0, 1],
    'CommsStat_flags_6': [0, 1],
    'Wheel1_Current': [0, 1],
    'Wheel2_Current': [0, 1],
    'Wheel3_Current': [0, 1],
    'CubeSense1_Current': [0, 1],
    'CubeSense2_Current': [0, 1],
    'CubeControl_Current3v3': [0, 1],
    'CubeControl_Current5v0': [0, 1],
    'CubeStar_Current': [0, 1],
    'CubeStar_Temp': [0, 1],
    'Magnetorquer_Current': [0, 1],
    'MCU_Temp': [0, 1],
    'Rate_Sensor_Temp_X': [0, 1],
    'Rate_Sensor_Temp_Y': [0, 1],
    'Rate_Sensor_Temp_Z': [0, 1],
}