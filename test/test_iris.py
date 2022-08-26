'''
 * Copyright (C) 2021  University of Alberta
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
 * @file test_iris.py
 * @author Jenish Patel
 * @date 2022-06-21
'''

'''  to run > yarn test_iris -I uart '''

import numpy as np
import os

import sys
from os import path
sys.path.append("./test")

from groundstation_tester import Tester

import time

tester = Tester() #call to initialize local test class

def test_iris_init():
    tester.sendAndExpect('ex2.iris.iris_power_on', {'err': 0})

def test_iris_program_flash():
    tester.sendAndExpect('ex2.iris.iris_program_flash', {'err': 0})

def test_iris_sensor_on():
    tester.sendAndExpect('ex2.iris.iris_turn_sensors_on', {'err': 0})

def test_iris_sensor_off():
    tester.sendAndExpect('ex2.iris.iris_turn_sensors_off', {'err': 0})

def test_iris_houskeeping():
    tester.send('ex2.iris.iris_get_hk')

def test_iris_take_image_and_deliver_image():
    tester.sendAndExpect('ex2.iris.iris_take_image', {'err': 0})
    time.sleep(2)
    tester.sendAndExpect('ex2.iris.iris_deliver_image', {'err': 0})

if __name__ == '__main__':
    # test_iris_program_flash()
    # time.sleep(6)

    # test_iris_init()
    # time.sleep(2)

    test_iris_sensor_on()
    time.sleep(10)

    test_iris_houskeeping()
    # time.sleep(2)
    test_iris_take_image_and_deliver_image()
    # time.sleep(15) #change depending on image file size

    test_iris_sensor_off()

    tester.summary()