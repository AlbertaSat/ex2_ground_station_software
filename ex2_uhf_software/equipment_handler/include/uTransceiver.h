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
#ifdef IS_SATELLITE
#include "uhf_uart.h"
#include "uhf_i2c.h"
#include "logger/logger.h"
#endif
#include "uhf.h"

// Max lengths for ESTTC strings
#define MAX_UHF_W_CMDLEN 120
#define MAX_UHF_W_ANSLEN 30
#define MAX_UHF_R_CMDLEN 30
#define MAX_UHF_R_ANSLEN 160
#define MIN_U_FREQ 435000000
#define MAX_U_FREQ 438000000

#define LETTER_E 0x45
#define LETTER_M 0x4D
#define LETTER_O 0x4F
#define BLANK_SPACE 0x20
#define CARRIAGE_R 0x0D

// Defines for Status Control Word (SCW)
#define UHF_UARTBAUD_9600 0
#define UHF_UARTBAUD_19200 2
#define UHF_UARTBAUD_115200 3
#define UHF_RESETBIT_CLEAR 0
#define UHF_RESETBIT_SET 1
#define UHF_RFMODE0 0
#define UHF_RFMODE1 1
#define UHF_RFMODE2 2
#define UHF_RFMODE3 3
#define UHF_RFMODE4 4
#define UHF_RFMODE5 5
#define UHF_RFMODE6 6
#define UHF_RFMODE7 7
#define UHF_ECHO_ON 1
#define UHF_ECHO_OFF 0
#define UHF_BCN_ON 1
#define UHF_BCN_OFF 0
#define UHF_PIPE_ON 1
#define UHF_PIPE_OFF 0
#define UHF_BOOT_MODE 1
#define UHF_APP_MODE 0

#define UHF_SCW_HFTX_INDEX 0
#define UHF_SCW_UARTBAUD_INDEX 1
#define UHF_SCW_RESET_INDEX 2
#define UHF_SCW_RFMODE_INDEX 3
#define UHF_SCW_ECHO_INDEX 4
#define UHF_SCW_BCN_INDEX 5
#define UHF_SCW_PIPE_INDEX 6
#define UHF_SCW_BOOT_INDEX 7
#define UHF_SCW_CTS_INDEX 8
#define UHF_SCW_SEC_INDEX 9
#define UHF_SCW_FRAM_INDEX 10
#define UHF_SCW_RFTS_INDEX 11

#define UHF_SCW_CMD 0
#define UHF_FREQ_CMD 1
#define UHF_UPTIME_CMD 2
#define UHF_TPCKT_CMD 3
#define UHF_RPCKT_CMD 4
#define UHF_RPCKTER_CMD 5
#define UHF_PIPET_CMD 6
#define UHF_BCNT_CMD 7
#define UHF_AUDIOT_CMD 8
#define UHF_DFLT_CMD 9
#define UHF_TEMP_CMD 10
#define UHF_AX25_CMD 239
#define UHF_LOWPWR_CMD 244
#define UHF_DSTCAL_CMD 245
#define UHF_SRCCAL_CMD 246
#define UHF_MORSECAL_CMD 247
#define UHF_MIDIBCN_CMD 248
#define UHF_SWVER_CMD 249
#define UHF_PLDSZ_CMD 250
#define UHF_BCNMSG_CMD 251
#define UHF_I2CADR_CMD 252
#define UHF_FRAM_CMD 253
#define UHF_SECURE_CMD 255
#define UHF_FW_CMD

#define UHF_WRITE_ANSLEN_SCW 17
#define UHF_WRITE_ANSLEN_FREQ 13
#define UHF_WRITE_ANSLEN_PIPET 13
#define UHF_WRITE_ANSLEN_BCNT 13
#define UHF_WRITE_ANSLEN_AUDIOT 13
#define UHF_WRITE_ANSLEN_DFLT 12
#define UHF_WRITE_ANSLEN_AX25 13
#define UHF_WRITE_ANSLEN_GENI2C 77
#define UHF_WRITE_ANSLEN_LOWPWR 13
#define UHF_WRITE_ANSLEN_SRCCAL 13
#define UHF_WRITE_ANSLEN_DSTCAL 13
#define UHF_WRITE_ANSLEN_MORSECAL 13
#define UHF_WRITE_ANSLEN_MIDIBCN 18
#define UHF_WRITE_ANSLEN_BCNMSG 13
#define UHF_WRITE_ANSLEN_I2CADR 15
#define UHF_WRITE_ANSLEN_FRAM 13
#define UHF_WRITE_ANSLEN_SECURE 13
#define UHF_WRITE_ANSLEN_FW 20 // TODO: Verify through testing

#define UHF_READ_ANSLEN_SCW 23
#define UHF_READ_ANSLEN_FREQ 23
#define UHF_READ_ANSLEN_UPTIME 23
#define UHF_READ_ANSLEN_TPCKT 23
#define UHF_READ_ANSLEN_RPCKT 23
#define UHF_READ_ANSLEN_RPCKTER 23
#define UHF_READ_ANSLEN_PIPET 23
#define UHF_READ_ANSLEN_BCNT 23
#define UHF_READ_ANSLEN_AUDIOT 23
#define UHF_READ_ANSLEN_TEMP 17
#define UHF_READ_ANSLEN_AX25 5
#define UHF_READ_ANSLEN_LOWPWR 15
#define UHF_READ_ANSLEN_SRCCAL 19
#define UHF_READ_ANSLEN_DSTCAL 19
#define UHF_READ_ANSLEN_MORSECAL 51
#define UHF_READ_ANSLEN_MIDIBCN 123
#define UHF_READ_ANSLEN_SWVER 39
#define UHF_READ_ANSLEN_PLDSZ 17
#define UHF_READ_ANSLEN_BCNMSG 160
#define UHF_READ_ANSLEN_FRAM 43
#define UHF_READ_ANSLEN_SECURE 21


typedef struct {
    uint8_t len;
    uint8_t message[MAX_UHF_W_CMDLEN];
} uhf_configStruct;

typedef struct {
    uint32_t add;
    uint8_t data[16];
} uhf_framStruct;

// Converts hex values to their ASCII characters

void convHexToASCII(int length, uint8_t *arr);
void convHexFromASCII(int length, uint8_t *arr);
uint32_t crc32_calc(size_t length, uint8_t *cmd);
int find_blankSpace(int length, uint8_t *string);

// Read and Write command functions
UHF_return UHF_genericWrite(uint8_t code, void *param);
UHF_return UHF_genericRead(uint8_t code, void *param);
UHF_return UHF_genericI2C(uint8_t format, uint8_t s_address, uint8_t len, uint8_t *data, uint8_t n_read_bytes);
UHF_return UHF_firmwareUpdate(uint8_t *line, uint8_t line_length);

#endif // UTRANSCEIVER_H
