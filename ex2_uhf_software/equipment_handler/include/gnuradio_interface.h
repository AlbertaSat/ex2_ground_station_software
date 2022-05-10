/*
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
 */
/**
 * @file gnuradio_interface.h
 * @author Josh Lazaruk
 * @date 2022-03-16
 */

#ifndef gnuradio_interface_H
#define gnuradio_interface_H

#include <stdint.h>
#include <stdbool.h>

uint16_t crc16(char* pData, int length);

bool i2c_package_for_radio(char *command, uint8_t command_len);

#endif
