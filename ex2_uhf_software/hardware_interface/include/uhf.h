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
 * @file uhf.c
 * @author Arash Yazdani, Dustin Wagner
 * @date 2020-10-26
 */

#ifndef UHF_HAL_H
#define UHF_HAL_H

#include <csp/csp.h>
#include <inttypes.h>

#ifdef IS_SATELLITE
#include "services.h"
#endif

#define MAX_W_CMDLEN 120
#define SCW_LEN 12

typedef enum {
    U_GOOD_CONFIG = 0,
    U_UART_SUCCESS = 9,
    U_I2C_SUCCESS = 10,
    U_ANS_SUCCESS = 11,
    U_FW_UPDATE_SUCCESS = 18,

    // Returned at the Equipment Handler level
    U_BAD_CONFIG = 1,
    U_BAD_PARAM = 2,
    U_BAD_ANS_CRC = 3,

    // Standard error answers from the UHF transceiver.
    // See EnduroSat UHF Transceiver Type II Manual
    U_ERR = 4,
    U_BAD_CMD_CRC = 5,
    U_BAD_CMD_LEN = 6,

    // Received error answer 2 or 3. Specific to command that was sent.
    // See EnduroSat UHF Transceiver Type II User Manual
    U_ERR_2 = 7,
    U_ERR_3 = 8,

    // Received if UART/I2C functions fail on Athena
    U_UART_FAIL = 12,
    U_I2C_FAIL = 13,

    // Received during a firmware update command
    U_ERR_FB = 14, // Memory error
    U_ERR_FW = 15, // Error while storing the firmware line
    U_ERR_CHKSUM = 16, // Corrupted firmware line
    U_ERR_FC = 17,

    // Returned by software if the transceiver is in PIPE mode,
    // meaning it cannot respond to commands
    U_I2C_IN_PIPE = 19,

    // Unknown error occured
    U_UNKOWN = 20,

    // Returned in HAL if UHF is stubbed
    IS_STUBBED_U = 0
} UHF_return;

typedef struct __attribute__((packed)) {
    uint32_t freq;
    uint32_t pipe_t;
    uint32_t beacon_t;
    uint32_t audio_t;
} UHF_Settings;

typedef struct __attribute__((packed)) {
    uint8_t scw[SCW_LEN];
    UHF_Settings set;
    uint32_t uptime;
    uint32_t pckts_out;
    uint32_t pckts_in;
    uint32_t pckts_in_crc16;
    float temperature;
} UHF_Status;

/*slightly modified version of UHF_Status to be more compatible with hk service
reformats nested struct*/
typedef struct __attribute__((packed)) {
    uint8_t scw[SCW_LEN];
    uint32_t freq;
    uint32_t pipe_t;
    uint32_t beacon_t;
    uint32_t audio_t;
    uint32_t uptime;
    uint32_t pckts_out;
    uint32_t pckts_in;
    uint32_t pckts_in_crc16;
    float temperature;
} UHF_housekeeping;

typedef struct __attribute__((packed)) {
    uint8_t addr;
} UHF_Address;

typedef struct {
    uint8_t len;
    uint8_t message[MAX_W_CMDLEN];
} UHF_configStruct;

typedef struct {
    uint32_t addr; // address
    uint8_t data[16];
} UHF_framStruct;

typedef struct __attribute__((packed)) {
    UHF_configStruct dest;
    UHF_configStruct src;
} UHF_Call_Sign;

typedef struct __attribute__((packed)) {
    UHF_configStruct morse;
    UHF_configStruct MIDI;
    UHF_configStruct message;
} UHF_Beacon;

UHF_return HAL_UHF_setSCW(uint8_t *U_scw);
UHF_return HAL_UHF_setFreq(uint32_t U_freq);
UHF_return HAL_UHF_setPipeT(uint32_t U_pipe_t);
UHF_return HAL_UHF_setBeaconT(uint32_t U_beacon_t);
UHF_return HAL_UHF_setAudioT(uint32_t U_audio_t);
UHF_return HAL_UHF_restore(uint8_t U_restore);
UHF_return HAL_UHF_lowPwr(uint8_t U_low_pwr);
UHF_return HAL_UHF_setDestination(UHF_configStruct U_dest);
UHF_return HAL_UHF_setSource(UHF_configStruct U_src);
UHF_return HAL_UHF_setMorse(UHF_configStruct U_morse);
UHF_return HAL_UHF_setMIDI(UHF_configStruct U_MIDI);
UHF_return HAL_UHF_setBeaconMsg(UHF_configStruct U_beacon_msg);
UHF_return HAL_UHF_setI2C(uint8_t U_I2C_add);
UHF_return HAL_UHF_setFRAM(UHF_framStruct U_FRAM);
UHF_return HAL_UHF_secure(uint8_t U_secure);

UHF_return HAL_UHF_getSCW(uint8_t *U_scw);
UHF_return HAL_UHF_getFreq(uint32_t *U_freq);
UHF_return HAL_UHF_getUptime(uint32_t *U_uptime);
UHF_return HAL_UHF_getPcktsOut(uint32_t *U_pckts_out);
UHF_return HAL_UHF_getPcktsIn(uint32_t *U_pckts_in);
UHF_return HAL_UHF_getPcktsInCRC16(uint32_t *U_pckts_in_crc16);
UHF_return HAL_UHF_getPipeT(uint32_t *U_pipe_t);
UHF_return HAL_UHF_getBeaconT(uint32_t *U_beacon_t);
UHF_return HAL_UHF_getAudioT(uint32_t *U_audio_t);
UHF_return HAL_UHF_getTemp(float *U_temperature);
UHF_return HAL_UHF_getLowPwr(uint8_t *U_low_pwr);
UHF_return HAL_UHF_getDestination(UHF_configStruct *U_dest);
UHF_return HAL_UHF_getSource(UHF_configStruct *U_src);
UHF_return HAL_UHF_getMorse(UHF_configStruct *U_morse);
UHF_return HAL_UHF_getMIDI(UHF_configStruct *U_MIDI);
UHF_return HAL_UHF_getPayload(uint16_t *U_payload_size);
UHF_return HAL_UHF_getBeaconMsg(UHF_configStruct *U_beacon_msg);
UHF_return HAL_UHF_getFRAM(UHF_framStruct *U_FRAM);
UHF_return HAL_UHF_getSecureKey(uint32_t *U_secure);

UHF_return UHF_getHK(UHF_housekeeping *uhf_hk);
UHF_return UHF_convert_endianness(UHF_housekeeping *uhf_hk);

#endif /* UHF_HAL_H */
