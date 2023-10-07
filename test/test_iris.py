"""
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
"""
"""
 * @file test_iris.py
 * @author Jenish Patel
 * @date 2022-06-21
"""

"""  to run > yarn test_iris -I uart """

import numpy as np
import os

import sys
from os import path

sys.path.append("./test")

from testLib import testLib as test

import time

test = test()  # call to initialize local test class


# TODO: Need to further discuss with Iris on what other kinds of tests
# are needed


def test_iris_init():
    test.send("ex2.iris.iris_power_on")


def test_iris_program_flash():
    test.send("ex2.iris.iris_program_flash")


def test_iris_sensor_on():
    test.send("ex2.iris.iris_turn_sensors_on")


def test_iris_sensor_off():
    test.send("ex2.iris.iris_turn_sensors_off")


def test_iris_houskeeping():
    test.send("ex2.iris.iris_get_hk")


def test_iris_take_image_and_deliver_image():
    test.send("ex2.iris.iris_take_image")
    time.sleep(3)
    test.send("ex2.iris.iris_deliver_image")


def test_program_iris():
    raise NotImplementedError


if __name__ == "__main__":
    test_iris_program_flash()
    time.sleep(8)

    # test_iris_init()
    # time.sleep(5)

    test_iris_sensor_on()
    time.sleep(10)

    test_iris_houskeeping()
    time.sleep(2)
    test_iris_take_image_and_deliver_image()
    time.sleep(10)  # change depending on image file size

    test_iris_sensor_off()
    time.sleep(5)

    test.summary()
