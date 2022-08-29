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

import time

test = test() #call to initialize local test class


# TODO: Need to further discuss with Iris on what other kinds of tests
#are needed

def test_iris_on():
    test.send('ex2.iris.iris_power_on')

def test_iris_off():
    test.send('ex2.iris.iris_power_off')

def test_iris_program_flash():
    test.send('ex2.iris.iris_program_flash')

def test_iris_sensor_on():
    test.send('ex2.iris.iris_turn_sensors_on')

def test_iris_sensor_off():
    test.send('ex2.iris.iris_turn_sensors_off')

def test_iris_houskeeping():
    test.send('ex2.iris.iris_get_hk')

def test_iris_take_image():
    test.send('ex2.iris.iris_take_image')

def test_iris_deliver_images():
    test.send('ex2.iris.iris_deliver_image')

def test_program_iris():
    raise NotImplementedError

def test_iris_deliver_logs():
    tester.sendAndExpect('ex2.iris.iris_deliver_log', {'err': 0})

def test_iris_set_time():
    cmd = "ex2.iris.iris_set_time({:d})"
    cmd = cmd.format(int(time.time()))
    tester.sendAndExpect(cmd, {'err': 0})

def test_iris_set_config(logger, method, nand, res, sat):
    tester.sendAndExpect('ex2.iris.iris_set_config(0,0,0,{:d},{:d})'.format(res, sat), {'err': 0})


def scenario_iris_firmware_update_and_housekeeping_retrieval():
    test_program_iris()
    time.sleep(5)     

    test_iris_on()
    time.sleep(5)

    test_iris_houskeeping()
    time.sleep(1)

    test_iris_off()

def scenario_iris_take_picture_direct_method():
    test_iris_on()
    time.sleep(5)

    test_iris_sensor_on()
    time.sleep(10)

    test_iris_set_config(0, 1, 0, 1280, 4)
    time.sleep(2)

    test_iris_take_image()
    time.sleep(1)

    test_iris_deliver_images()
    time.sleep(10)

    test_iris_sensor_off()
    time.sleep(2)

    test_iris_off()

def scenario_iris_take_picture_nand_method():
    test_iris_on()
    time.sleep(5)

    test_iris_sensor_on()
    time.sleep(10)

    test_iris_set_config(0, 0, 0, 1280, 4)
    time.sleep(2)

    test_iris_take_image()
    time.sleep(1)

    test_iris_take_image()
    time.sleep(1)

    test_iris_sensor_off()
    time.sleep(2)

    test_iris_deliver_images()
    time.sleep(10)

    test_iris_off()

def scenario_iris_deliver_images_after_power_cycle():
    test_iris_on()
    time.sleep(5)

    test_iris_sensor_on()
    time.sleep(10)

    test_iris_set_config(0, 0, 0, 1280, 4)
    time.sleep(2)

    test_iris_take_image()
    time.sleep(1)

    test_iris_take_image()
    time.sleep(1)

    test_iris_sensor_off()
    time.sleep(2)

    test_iris_off()
    time.sleep(10)

    test_iris_on()
    time.sleep(5)

    test_iris_deliver_images()
    time.sleep(10)

    test_iris_off()

def scenario_iris_get_logs():
    test_iris_on()
    time.sleep(5)

    test_iris_set_time()
    time.sleep(1)

    test_iris_houskeeping()
    time.sleep(1)

    test_iris_sensor_on()
    time.sleep(10)

    test_iris_set_config(0, 0, 0, 640, 0)
    time.sleep(2)

    test_iris_take_image()
    time.sleep(1)

    test_iris_houskeeping()
    time.sleep(1)

    test_iris_sensor_off()
    time.sleep(2)

    test_iris_deliver_logs()
    time.sleep(10)

    # Use below bash command to properly format log file
    # tr -d '\0' <iris_log.txt >iris_new_log.txt

    test_iris_off()

def scenario_iris_format_nand:
    test_iris_on()
    time.sleep(5)

    test_iris_set_config(0, 0, 1, 1280, 4)
    time.sleep(2)

    test_iris_off()

def scenario_iris_disable_logger:
    test_iris_on()
    time.sleep(5)

    test_iris_set_config(1, 0, 0, 1280, 4)
    time.sleep(2)

    test_iris_off()

    
if __name__ == '__main__':
    # scenario_iris_firmware_update_and_housekeeping_retrieval()
    # scenario_iris_take_picture_direct_method()
    # scenario_iris_take_picture_nand_method()
    # scenario_iris_deliver_images_after_power_cycle()
    # scenario_iris_get_logs()
    # scenario_iris_disable_logger()
    # scenario_iris_format_nand()

    tester.summary()
