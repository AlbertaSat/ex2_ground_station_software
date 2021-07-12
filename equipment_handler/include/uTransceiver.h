/*
 * Copyright (C) 2015  University of Alberta
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
 * @file uTransceiver.c
 * @author Thomas Ganley
 * @date 2020-05-28
 */

#ifndef UTRANSCEIVER_H
#define UTRANSCEIVER_H

#include <stdint.h>
#include <string.h>

#include "i2c.h"

#define MAX_W_CMDLEN 120
#define MAX_W_ANSLEN 30
#define MAX_R_CMDLEN 30
#define MAX_R_ANSLEN 150
#define MIN_U_FREQ 435000000
#define MAX_U_FREQ 438000000

#define LETTER_E 0x45
#define LETTER_M 0x4D
#define LETTER_O 0x4F
#define BLANK_SPACE 0x20
#define CARRIAGE_R 0x0D

typedef enum {
  U_GOOD_CONFIG = 0,
  U_BAD_CONFIG = -1,
  U_BAD_PARAM = -2,
  U_BAD_ANS_CRC = -3,

  U_BAD_CMD_CRC = -4,
  U_BAD_CMD_LEN = -5,
  U_CMD_SPEC_2 = 2,
  U_CMD_SPEC_3 = 3,

  U_UNK_ERR = -10,
  IS_STUBBED_U = 0 // Used for stubbed UHF in hardware interface
} UHF_return;

typedef struct {
  uint8_t len;
  uint8_t message[MAX_W_CMDLEN];
} uhf_configStruct;

typedef struct {
  uint32_t add;
  uint8_t data[16];
} uhf_framStruct;

// Converts hex values to their ASCII characters
void convHexToASCII(int length, uint8_t* arr);
void convHexFromASCII(int length, uint8_t* arr);
uint32_t crc32_calc(size_t length, char* cmd);
int find_blankSpace(int length, char* string);

// Read and Write command functions
UHF_return UHF_genericWrite(uint8_t code, void* param);
UHF_return UHF_genericRead(uint8_t code, void* param);
UHF_return UHF_genericI2C(uint8_t format, uint8_t s_address, uint8_t len,
                          uint8_t* data, uint8_t n_read_bytes);

#endif  // UTRANSCEIVER_H
