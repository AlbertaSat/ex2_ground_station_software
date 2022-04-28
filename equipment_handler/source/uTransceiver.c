/*
 * Copyright (C) 2015  University of Alberta
 *
 * This program is free software; you can redistribute it
 * and/or modify it under the terms of the GNU General
 * Public License as published by the Free Software
 * Foundation; either version 2 of the License, or (at your
 * option) any later version.
 *
 * This program is distributed in the hope that it will be
 * useful, but WITHOUT ANY WARRANTY; without even the
 * implied warranty of MERCHANTABILITY or FITNESS FOR A
 * PARTICULAR PURPOSE.  See the GNU General Public License
 * for more details.
 */

/**
 * @file uTransceiver.c
 * @author Thomas Ganley, Nicholas Sorensen
 * @date 2020-05-28
 */

#include "uTransceiver.h"

// TODO: Firmware update command
// TODO: Combine send code into single function?
// TODO: Write UART function
// TODO: Add error logging

static char i2c_address_small_digit_ascii = '2'; // Stores the second digit of the i2c address (in hex)
bool enter_pipe_mode = false;

static uint32_t crc32_calc(size_t length, char *cmd);
static int find_blankSpace(int length, char *string);
static UHF_return UHF_error_check(uint8_t *ans, uint8_t answer_length);

/**
 * @brief
 *      Generic function for write commands sent over i2c
 * @details
 *      This function will build a command dependant on command code and
 *      input parameters, send the command, and interpret the answer
 * @attention
 *      Only certain write command codes are valid. Be aware of input
 *      pointer type
 * @param code
 *          The write command code as it appears in the UHF
 *          Transceiver's manual
 *
 *          CODE    COMMAND DESCRIPTION
 *          0       Set the status control word
 *          1       Set the frequency
 *          6       Set PIPE mode timeout period
 *          7       Set beacon transmission period
 *          8       Set audio beacon transmission period
 *          9       Restore default values
 *          239     Enable/Disable Automatic AX.25 Decoding
 *          244     Enter low power mode
 *          245     Set destination call sign
 *          246     Set source call sign
 *          247     Set morse code call sign
 *          248     Set MIDI audio beacon message
 *          251     Set the beacon message content
 *          252     Set the device address
 *          253     FRAM memory write
 *          255     Put the transceiver into secure mode
 *
 * @param param
 *          Pointer to required input. Code dictates required pointer type:
 *          CODE    TYPE        PARAM DESCRIPTION
 *          0       uint8_t*    Array of 12 SCW values
 *          1       uint32_t*   Frequency in Hz
 *          6       uint16_t*   Time in seconds (1-255)
 *          7       uint16_t*   Time in seconds (1-65535)
 *          8       uint16_t*   Time in seconds (30-65535)
 *          9       uint8_t*    = 1 to confirm reset
 *          239     uint8_t*    State (0 or 1)
 *          244     uint8_t*    = 1 to confirm change
 *          245     uhf_configStruct*   Config structure
 *          246     uhf_configStruct*   ''
 *          247     uhf_configStruct*   ''
 *          248     uhf_configStruct*   ''
 *          251     uhf_configStruct*   ''
 *          252     uint8_t*    = 0x22 or 0x23
 *          253     uhf_framStruct*     FRAM structure
 *          255     uint8_t*    = 1 to confirm change
 *
 * @return
 *      UHF_return
 */

UHF_return UHF_genericWrite(uint8_t code, void *param) {
    char command_to_send[MAX_UHF_W_CMDLEN] = {0};
    uint8_t command_length = 0;
    uint8_t answer_length = 0;

    /* The following switch statement depends on the command code to:    *
     *    - Calculate necessary ASCII characters from input parameters *
     *    - Build the command to be sent                               */

    switch (code) {
    case UHF_SCW_CMD: { // Set the status control word
        uint8_t *array = (uint8_t *)param;
        uint8_t hex[4] = {0};

        if (*(array + UHF_SCW_PIPE_INDEX) == 1) {
            enter_pipe_mode = true;
        }

        // Grouping params into 4 bits (hex values)
        hex[0] = (*(array) << 2) | *(array + 1);
        hex[1] = (*(array + 2) << 3) | *(array + 3);
        hex[2] = (*(array + 4) << 3) | (*(array + 5) << 2) | (*(array + 6) << 1) | (*(array + 7));
        hex[3] = (*(array + 8) << 3) | (*(array + 9) << 2) | (*(array + 10) << 1) | (*(array + 11));

        convHexToASCII(4, hex);
        // Building the command
        char command_assembly[30] = {'E',         'S', '+',    'W',       '2',    i2c_address_small_digit_ascii,
                                        '0',         '0', hex[0], hex[1],    hex[2], hex[3],
                                        BLANK_SPACE, 'C', 'C',    'C',       'C',    'C',
                                        'C',         'C', 'C',    CARRIAGE_R, 0};
        strcpy(command_to_send, command_assembly);
        answer_length = UHF_WRITE_ANSLEN_SCW;
        break;
    }

    case UHF_FREQ_CMD: { // Set the frequency
        uint32_t *new_freq = (uint32_t *)param;
        if (*new_freq < MIN_U_FREQ || *new_freq > MAX_U_FREQ)
            return U_BAD_PARAM;

        float temp = (*new_freq) / 6500000.0f;
        uint8_t val1 = (uint8_t)temp - 1;                   // Integer term
        uint32_t val2 = (uint32_t)((temp - val1) * 524288); // Fractional term
        uint8_t hex[8] = {(val2 >> 4) & 15,  (val2)&15,         (val2 >> 12) & 15, (val2 >> 8) & 15,
                          (val2 >> 20) & 15, (val2 >> 16) & 15, (val1 >> 4) & 15,  (val1)&15};

        convHexToASCII(8, hex);

        // Building the command
        char command_assembly[30] = {
            'E',    'S',       '+',    'W',    '2',         i2c_address_small_digit_ascii,
            '0',    '1',       hex[0], hex[1], hex[2],      hex[3],
            hex[4], hex[5],    hex[6], hex[7], BLANK_SPACE, 'C',
            'C',    'C',       'C',    'C',    'C',         'C',
            'C',    CARRIAGE_R, 0};
        strcpy(command_to_send, command_assembly);
        answer_length = UHF_WRITE_ANSLEN_FREQ;
        break;
    }

    case UHF_PIPET_CMD:  // Set PIPE mode Timeout Period
    case UHF_BCNT_CMD:   // Set Beacon Transmission Period
    case UHF_AUDIOT_CMD: // Set Audio Beacon Transmission Period
    {
        uint32_t *time = (uint32_t *)param;

        if (code == UHF_PIPET_CMD) {
            if (*time < 1 || *time > 255)
                return U_BAD_PARAM;
        }

        if (code == UHF_BCNT_CMD || code == UHF_AUDIOT_CMD) {
            if (*time > 0xFFFF)
                return U_BAD_PARAM;
        }

        uint8_t hex[4] = {(*time >> 12) & 15, (*time >> 8) & 15, (*time >> 4) & 15, (*time) & 15};
        convHexToASCII(4, hex);

        char command_assembly[30] = {
            'E',    'S',       '+',    'W',    '2',         i2c_address_small_digit_ascii,
            '0',    code + 48, '0',    '0',    '0',         '0',
            hex[0], hex[1],    hex[2], hex[3], BLANK_SPACE, 'C',
            'C',    'C',       'C',    'C',    'C',         'C',
            'C',    CARRIAGE_R, 0};
        strcpy(command_to_send, command_assembly);
        if (code == 6) {
            answer_length = UHF_WRITE_ANSLEN_PIPET;
        } else if (code == 7) {
            answer_length = UHF_WRITE_ANSLEN_BCNT;
        } else if (code == 8) {
            answer_length = UHF_WRITE_ANSLEN_AUDIOT;
        }
        break;
    }

    case UHF_DFLT_CMD: { // Restore Default Values
        uint8_t *confirm = (uint8_t *)param;
        if (*confirm != 1)
            return U_BAD_PARAM;
        char command_assembly[20] = {'E', 'S', '+',         'W', '2', i2c_address_small_digit_ascii,
                                        '0', '9', BLANK_SPACE, 'C', 'C', 'C',
                                        'C', 'C', 'C',         'C', 'C', CARRIAGE_R, 0};
        strcpy(command_to_send, command_assembly);
        answer_length = UHF_WRITE_ANSLEN_DFLT;
        break;
    }

    case UHF_AX25_CMD: { // Enable/Disable AX.25 Automatic Decoding
        uint8_t *state = (uint8_t *)param;
        convHexToASCII(1, state);
        char command_assembly[21] = {'E', 'S',       '+', 'W',   '2',         i2c_address_small_digit_ascii,
	                             'E', 'F',       '0', *state, BLANK_SPACE, 'C',
				     'C', 'C',       'C', 'C',   'C',         'C',
				     'C', CARRIAGE_R, 0};
        strcpy(command_to_send, command_assembly);
        answer_length = UHF_WRITE_ANSLEN_AX25;
        break;
    }

    case UHF_LOWPWR_CMD: { // Enter low power mode
        uint8_t *confirm = (uint8_t *)param;
        if (*confirm != 1)
            return U_BAD_PARAM;
        char command_assembly[30] = {'E', 'S', '+',         'W', '2', i2c_address_small_digit_ascii,
                                        'F', '4', BLANK_SPACE, 'C', 'C', 'C',
                                        'C', 'C', 'C',         'C', 'C', CARRIAGE_R, 0};
        strcpy(command_to_send, command_assembly);
        answer_length = UHF_WRITE_ANSLEN_LOWPWR;
        break;
    }

    case 245: // Set Destination Call Sign
    case 246: // Set Source Call Sign
    {
        uhf_configStruct *sign = (uhf_configStruct *)param;
        char command_assembly[30] = {'E', 'S', '+', 'W', '2', i2c_address_small_digit_ascii, 'F',
	                             (uint8_t)code - 192,
				     sign->message[0], sign->message[1], sign->message[2],
				     sign->message[3], sign->message[4], sign->message[5],
				     BLANK_SPACE, 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
				     CARRIAGE_R, 0};
        strcpy(command_to_send, command_assembly);
        if (code == 245) {
            answer_length = UHF_WRITE_ANSLEN_DSTCAL;
        } else if (code == 426) {
            answer_length = UHF_WRITE_ANSLEN_SRCCAL;
        }
        break;
    }

    case UHF_MORSECAL_CMD: { // Set Morse Code Call Sign
        uhf_configStruct *callsign = (uhf_configStruct *)param;
        uint8_t len[2] = {(callsign->len - (callsign->len % 10)) / 10, callsign->len % 10};
        convHexToASCII(2, len);
        char command_assembly[60] = {'E', 'S', '+',    'W',   '2', i2c_address_small_digit_ascii,
	                             'F', '7', len[0], len[1]};
	int i = 0;
        for (; i < callsign->len; i++) {
            uint8_t sym = callsign->message[i];
            if (sym != 0x2D && sym != 0x2E && sym != BLANK_SPACE)
                return U_BAD_PARAM;
            command_assembly[10 + i] = sym;
        }
        command_assembly[10 + i] = BLANK_SPACE;
        command_assembly[11 + i] = 'C';
        command_assembly[12 + i] = 'C';
        command_assembly[13 + i] = 'C';
        command_assembly[14 + i] = 'C';
        command_assembly[15 + i] = 'C';
        command_assembly[16 + i] = 'C';
        command_assembly[17 + i] = 'C';
        command_assembly[18 + i] = 'C';
        command_assembly[19 + i] = CARRIAGE_R;
        command_assembly[20 + i] = 0;
        strcpy(command_to_send, command_assembly);
        answer_length = UHF_WRITE_ANSLEN_MORSECAL;
        break;
    }

    case UHF_MIDIBCN_CMD: { // Set the MIDI Audio Beacon
        uhf_configStruct *beacon = (uhf_configStruct *)param;
        uint8_t len[2] = {(beacon->len - (beacon->len % 10)) / 10, beacon->len % 10};
        convHexToASCII(2, len);
        char command_assembly[120] = {'E', 'S', '+',    'W',   '2', i2c_address_small_digit_ascii,
	                              'F', '8', len[0], len[1], 0};
        uint8_t j = 0;
        for (; j < (3 * beacon->len); j++) {
            command_assembly[10 + j] = beacon->message[j];
        }
        command_assembly[10 + j] = BLANK_SPACE;
        command_assembly[11 + j] = 'C';
        command_assembly[12 + j] = 'C';
        command_assembly[13 + j] = 'C';
        command_assembly[14 + j] = 'C';
        command_assembly[15 + j] = 'C';
        command_assembly[16 + j] = 'C';
        command_assembly[17 + j] = 'C';
        command_assembly[18 + j] = 'C';
        command_assembly[19 + j] = CARRIAGE_R;
        command_assembly[20 + j] = 0;
        strcpy(command_to_send, command_assembly);
        answer_length = UHF_WRITE_ANSLEN_MIDIBCN;
        break;
    }

    case UHF_BCNMSG_CMD: { // Set the Beacon Message contents
        uhf_configStruct *beacon = (uhf_configStruct *)param;
        uint8_t len[2] = {(beacon->len) >> 4, (beacon->len) & 15};
        convHexToASCII(2, len);

        uint8_t command_assembly[120] = {'E', 'S', '+',    'W',   '2', i2c_address_small_digit_ascii,
                                         'F', 'B', len[0], len[1]};
        int k = 0;
        for (; k < beacon->len; k++) {
            command_assembly[10 + k] = beacon->message[k];
        }
        command_assembly[10 + k] = BLANK_SPACE;
        command_assembly[11 + k] = 'C';
        command_assembly[12 + k] = 'C';
        command_assembly[13 + k] = 'C';
        command_assembly[14 + k] = 'C';
        command_assembly[15 + k] = 'C';
        command_assembly[16 + k] = 'C';
        command_assembly[17 + k] = 'C';
        command_assembly[18 + k] = 'C';
        command_assembly[19 + k] = CARRIAGE_R;

        command_length = beacon->len + 20;
        memcpy(command_to_send, command_assembly, command_length);
        answer_length = UHF_WRITE_ANSLEN_BCNMSG;
        break;
    }

    case UHF_I2CADR_CMD: { // Set the device address
        uint8_t *add = (uint8_t *)param;

        if (*add != 0x22 && *add != 0x23)
            return U_BAD_PARAM;
        uint8_t small = *add - 32;
        convHexToASCII(1, &small);
        char command_assembly[21] = {'E', 'S',       '+', 'W',   '2',         i2c_address_small_digit_ascii,
                                     'F', 'C',       '2', small, BLANK_SPACE, 'C',
				     'C', 'C',       'C', 'C',   'C',         'C',
				     'C', CARRIAGE_R, 0};
        strcpy(command_to_send, command_assembly);
        answer_length = UHF_WRITE_ANSLEN_I2CADR;
        break;
    }

    case UHF_FRAM_CMD: { // FRAM memory write
        uhf_framStruct *fram_w = (uhf_framStruct *)param;

        uint32_t add = fram_w->add;
        if (add >= 0x8000 && add <= 0x83A4)
            return U_BAD_PARAM;
        if (add >= 0x83FE && add <= 0x24000)
            return U_BAD_PARAM;

        uint8_t chadd[8] = {add >> 28,        (add >> 24) & 15, (add >> 20) & 15, (add >> 16) & 15,
                            (add >> 12) & 15, (add >> 8) & 15,  (add >> 4) & 15,  add & 15};
        convHexToASCII(8, chadd);

        char command_assembly[60] = {'E',
                                        'S',
                                        '+',
                                        'W',
                                        '2',
                                        i2c_address_small_digit_ascii,
                                        'F',
                                        'D',
                                        chadd[0],
                                        chadd[1],
                                        chadd[2],
                                        chadd[3],
                                        chadd[4],
                                        chadd[5],
                                        chadd[6],
                                        chadd[7],
                                        [48] = BLANK_SPACE,
                                        'C',
                                        'C',
                                        'C',
                                        'C',
                                        'C',
                                        'C',
                                        'C',
                                        'C',
                                        CARRIAGE_R,
					0};
        uint8_t hex[2] = {0};
        for (int i = 0; i < 16; i++) {
            hex[0] = fram_w->data[i] >> 4;
            hex[1] = fram_w->data[i] & 15;
            convHexToASCII(2, hex);
            command_assembly[16 + 2 * i] = hex[0];
            command_assembly[16 + 2 * i + 1] = hex[1];
        }
        strcpy(command_to_send, command_assembly);
        answer_length = UHF_WRITE_ANSLEN_FRAM;
        break;
    }

    case UHF_SECURE_CMD: { // Secure Mode write
        uint8_t *confirm = (uint8_t *)param;
        if (*confirm != 1)
            return U_BAD_PARAM;

        char command_assembly[20] = {'E', 'S', '+',         'W', '2', i2c_address_small_digit_ascii,
	                             'F', 'F', BLANK_SPACE, 'C', 'C', 'C',
				     'C', 'C', 'C',         'C', 'C', CARRIAGE_R, 0};
        strcpy(command_to_send, command_assembly);
        answer_length = UHF_WRITE_ANSLEN_SECURE;
        break;
    }

    default:
        return U_BAD_CONFIG;
    }

    // strlen calculates the length of all commands except the beacon command, which can have 0x00-valued bytes
    if (code != UHF_BCNMSG_CMD)
        command_length = strlen(command_to_send);

    /* The following is necessary for all write commands:
     *    - Calculate the crc32 of the command
     *    - Send the command and receive the answer
     *    - Handle errors
     */

    /* Calculate the crc32 of the command*/
    crc32_calc(find_blankSpace(command_length, command_to_send), command_to_send);
    uint8_t *ans = pvPortMalloc(answer_length * sizeof(uint8_t));
    UHF_return return_val;

/* Send the command and receive the answer */
#ifndef UHF_USE_I2C_CMDS
    return_val = uhf_uart_sendAndReceive((uint8_t *)command_to_send, command_length, ans, answer_length);
#else
    uint8_t i2c_address = i2c_address_small_digit_ascii;
    convHexFromASCII(1, &i2c_address);
    i2c_address += 0x20;
    if (code == UHF_I2CADR_CMD) {
        // i2c command to change the i2c address does not receive a response.
        return_val = i2c_sendCommand(i2c_address, command_to_send, command_length);
    } else if ((code == UHF_SCW_CMD) && (enter_pipe_mode == true)) {
        return_val = i2c_sendAndReceivePIPE(i2c_address, command_to_send, command_length, ans, answer_length);
    } else {
        return_val = i2c_sendAndReceive(i2c_address, command_to_send, command_length, ans, answer_length);
    }
#endif

    // Handle errors
    if((return_val == U_I2C_SUCCESS) || (return_val == U_UART_SUCCESS)){
        return_val = UHF_error_check(ans, answer_length);
    }

    vPortFree(ans);
    enter_pipe_mode = false;
    return return_val;
}

/**
 * @brief
 *      Generic function for read commands sent over i2c
 * @details
 *      This function will send a command dependant on command code,
 *      send the command, interpret the answer and save read data
 * @attention
 *      Only certain read command codes are valid. Be aware of input
 *      pointer type
 * @param code
 *      The write command code as it appears in the UHF
 *      Transceiver's manual:
 *
 *      CODE    COMMAND DESCRIPTION
 *      0       Get the status control word
 *      1       Get the frequency
 *      2       Get uptime
 *      3       Get # of transmitted packets
 *      4       Get # of received packets
 *      5       Get # of received packets w CRC16 error
 *      6       Get PIPE mode timeout period
 *      7       Get beacon transmission period
 *      8       Get audio beacon transmission period
 *      10      Get the internal temperature of the board
 *      239     Get the state of AX.25 decoding
 *      244     Get low power mode status
 *      245     Get destination call sign
 *      246     Get source call sign
 *      247     Get morse code call sign
 *      248     Get MIDI audio beacon
 *      249     Get software version build
 *      250     Get device payload size
 *      251     Get the beacon message content
 *      253     FRAM memory read
 *      255     Get the secure mode key
 *
 * @param param
 *      Pointer to required input. Code dictates required pointer type:
 *      CODE    TYPE        PARAM DESCRIPTION
 *      0       uint8_t*    Array of 12 status control word values
 *      1       uint32_t*   Frequency in Hz
 *      2       uint32_t*   Array of 2 values (1 time, 1 rssi)
 *      3       uint32_t*   Array of 2 Values (1 #, 1 rssi)
 *      4       uint32_t*   Array of 2 values (1 #, 1 rssi)
 *      5       uint32_t*   Array of 2 values (1 #, 1 rssi)
 *      6       uint32_t*   Array of 2 values (1 time [1-255], 1 rssi)
 *      7       uint32_t*   Array of 2 values (1 time [1-65535], 1 rssi)
 *      8       uint32_t*   Array of 2 values (1 time [30-65535], 1 rssi)
 *      10      float*      Value in degrees celsius
 *      239     uint8_t*    State (0 or 1)
 *      244     uint8_t*    = 1 for low power mode
 *      245     uhf_configStruct*   Config struct
 *      246     uhf_configStruct*   ''
 *      247     uhf_configStruct*   ''
 *      248     uhf_configStruct*   ''
 *      249     uint8_t*    Char array (form "X.xx")
 *      250     uint16_t*   Value in # of bytes
 *      251     uhf_configStruct*   Config struct
 *      253     uhf_framStruct*     FRAM structure
 *      255     uint32_t*   Value of the secure key
 *
 * @return
 *      UHF_return
 */

UHF_return UHF_genericRead(uint8_t code, void *param) {
    /* The following is necessary for all read commands:
     *    - Form the command
     *    - Send the command and receive the answer
     *    - Handle errors
     */

    /* Form the command */
    // Note: The FRAM read command requires a unique format
    uint8_t code_chars[2] = {(code >> 4) & 15, code & 15};
    convHexToASCII(2, code_chars);
    char command_to_send[MAX_UHF_R_CMDLEN] = {
        'E',           'S',           '+',         'R', '2', i2c_address_small_digit_ascii,
        code_chars[0], code_chars[1], BLANK_SPACE, 'C', 'C', 'C',
        'C',           'C',           'C',         'C', 'C', CARRIAGE_R, 0};

    if (code == UHF_FRAM_CMD) {
        uhf_framStruct *fram_struct = (uhf_framStruct *)param;
        uint32_t add = fram_struct->add;
        if (add >= 0x8000 && add <= 0x83A4)
            return U_BAD_PARAM;
        if (add >= 0x83FE && add <= 0x24000)
            return U_BAD_PARAM;

        uint8_t chadd[8] = {add >> 28,        (add >> 24) & 15, (add >> 20) & 15, (add >> 16) & 15,
                            (add >> 12) & 15, (add >> 8) & 15,  (add >> 4) & 15,  add & 15};
        convHexToASCII(8, chadd);

        char fram_command[MAX_UHF_R_CMDLEN] = {'E',         'S',
                                               '+',         'R',
					       '2',         i2c_address_small_digit_ascii,
					       'F',         'D',
					       chadd[0],    chadd[1],
					       chadd[2],    chadd[3],
					       chadd[4],    chadd[5],
					       chadd[6],    chadd[7],
					       BLANK_SPACE, 'C',
					       'C',         'C',
					       'C',         'C',
					       'C',         'C',
					       'C',         [25] = CARRIAGE_R, 0};
        strcpy(command_to_send, fram_command);
    }

    uint8_t answer_length = 0;
    switch (code) {
    case UHF_SCW_CMD:
        answer_length = UHF_READ_ANSLEN_SCW;
        break;
    case UHF_FREQ_CMD:
        answer_length = UHF_READ_ANSLEN_FREQ;
        break;
    case UHF_UPTIME_CMD:
        answer_length = UHF_READ_ANSLEN_UPTIME;
        break;
    case UHF_TPCKT_CMD:
        answer_length = UHF_READ_ANSLEN_TPCKT;
        break;
    case UHF_RPCKT_CMD:
        answer_length = UHF_READ_ANSLEN_RPCKT;
        break;
    case UHF_RPCKTER_CMD:
        answer_length = UHF_READ_ANSLEN_RPCKTER;
        break;
    case UHF_PIPET_CMD:
        answer_length = UHF_READ_ANSLEN_PIPET;
        break;
    case UHF_BCNT_CMD:
        answer_length = UHF_READ_ANSLEN_BCNT;
        break;
    case UHF_AUDIOT_CMD:
        answer_length = UHF_READ_ANSLEN_AUDIOT;
        break;
    case UHF_TEMP_CMD:
        answer_length = UHF_READ_ANSLEN_TEMP;
        break;
    case UHF_AX25_CMD:
        answer_length = UHF_READ_ANSLEN_AX25;
        break;
    case UHF_LOWPWR_CMD:
        answer_length = UHF_READ_ANSLEN_LOWPWR;
        break;
    case UHF_SRCCAL_CMD:
        answer_length = UHF_READ_ANSLEN_SRCCAL;
        break;
    case UHF_DSTCAL_CMD:
        answer_length = UHF_READ_ANSLEN_DSTCAL;
        break;
    case UHF_MORSECAL_CMD:
        answer_length = UHF_READ_ANSLEN_MORSECAL;
        break;
    case UHF_MIDIBCN_CMD:
        answer_length = UHF_READ_ANSLEN_MIDIBCN;
        break;
    case UHF_SWVER_CMD:
        answer_length = UHF_READ_ANSLEN_SWVER;
        break;
    case UHF_PLDSZ_CMD:
        answer_length = UHF_READ_ANSLEN_PLDSZ;
        break;
    case UHF_BCNMSG_CMD:
        answer_length = UHF_READ_ANSLEN_BCNMSG;
        break;
    case UHF_FRAM_CMD:
        answer_length = UHF_READ_ANSLEN_FRAM;
        break;
    case UHF_SECURE_CMD:
        answer_length = UHF_READ_ANSLEN_SECURE;
        break;
    default:
        return U_BAD_PARAM;
    }

    crc32_calc(find_blankSpace(strlen(command_to_send), command_to_send), command_to_send);

    /* Send the command and receive the answer */
    uint8_t *ans = pvPortMalloc(answer_length * sizeof(uint8_t));
    UHF_return return_val;

#ifndef UHF_USE_I2C_CMDS
    return_val = uhf_uart_sendAndReceive((uint8_t *)command_to_send, strlen(command_to_send), ans, answer_length);
#else
    uint8_t i2c_address = i2c_address_small_digit_ascii;
    convHexFromASCII(1, &i2c_address);
    i2c_address += 0x20; // Address is always 0x22 or 0x23
    return_val =
        i2c_sendAndReceive(i2c_address, (uint8_t *)command_to_send, strlen(command_to_send), ans, answer_length);
#endif

    /* Handle Errors */
    if((return_val == U_I2C_SUCCESS) || (return_val == U_UART_SUCCESS)){
        return_val = UHF_error_check(ans, answer_length);
    }

    if (return_val == U_ANS_SUCCESS) {
      int blankspace_index = find_blankSpace(strlen((char *)ans), (char *)ans);

        /* The following switch statement depends on the command code to:
         *    - Interpret the answer
         *    - Calculate relevant parameters
         *    - Save these in *param and subsequent pointers
         */

        switch (code) {
        case UHF_SCW_CMD: { // Get the status control word
            uint8_t *array = (uint8_t *)param;

            uint8_t hex[4] = {ans[blankspace_index - 4], ans[blankspace_index - 3], ans[blankspace_index - 2],
                              ans[blankspace_index - 1]};
            convHexFromASCII(4, hex);

            // Storing the original parameters in the array
            *array = hex[0] >> 2;
            *(array + 1) = hex[0] & 3;
            *(array + 2) = hex[1] >> 3;
            *(array + 3) = hex[1] & 7;
            *(array + 4) = hex[2] >> 3;
            *(array + 5) = (hex[2] >> 2) & 1;
            *(array + 6) = (hex[2] >> 1) & 1;
            *(array + 7) = hex[2] & 1;
            *(array + 8) = (hex[3] >> 3);
            *(array + 9) = (hex[3] >> 2) & 1;
            *(array + 10) = (hex[3] >> 1) & 1;
            *(array + 11) = hex[3] & 1;
            break;
        }

        case UHF_FREQ_CMD: { // Get the frequency
            uint32_t *freq = (uint32_t *)param;

            uint8_t hex[8] = {ans[blankspace_index - 8], ans[blankspace_index - 7], ans[blankspace_index - 6],
                              ans[blankspace_index - 5], ans[blankspace_index - 4], ans[blankspace_index - 3],
                              ans[blankspace_index - 2], ans[blankspace_index - 1]};
            convHexFromASCII(8, hex);

            uint8_t val1 = (hex[6] << 4) | hex[7];
            uint32_t val2 =
                (hex[4] << 20) | (hex[5] << 16) | (hex[2] << 12) | (hex[3] << 8) | (hex[0] << 4) | hex[1];

            *freq = (val1 + (val2 / 524288.0f)) * 6500000.0f;

            break;
        }

        case UHF_UPTIME_CMD:  // Get uptime
        case UHF_TPCKT_CMD:   // Get # of transmitted packets
        case UHF_RPCKT_CMD:   // Get # of received packets
        case UHF_RPCKTER_CMD: // Get # of received packets w CRC16 error
        case UHF_PIPET_CMD:   // Get the PIPE Mode timeout
        case UHF_BCNT_CMD:    // Get Beacon transmission period
        case UHF_AUDIOT_CMD:  // Get Audio Beacon period
        {
            uint32_t *value = (uint32_t *)param;

            uint8_t hex[8] = {ans[blankspace_index - 8], ans[blankspace_index - 7], ans[blankspace_index - 6],
                              ans[blankspace_index - 5], ans[blankspace_index - 4], ans[blankspace_index - 3],
                              ans[blankspace_index - 2], ans[blankspace_index - 1]};
            convHexFromASCII(8, hex);

            *value = (hex[0] << 28) | (hex[1] << 24) | (hex[2] << 20) | (hex[3] << 16) | (hex[4] << 12) |
                     (hex[5] << 8) | (hex[6] << 4) | hex[7];

            // Compute the RSSI
            uint8_t rssi_hex[2] = {ans[blankspace_index - 10], ans[blankspace_index - 9]};
            convHexFromASCII(2, rssi_hex);

//            *(value + 1) = (rssi_hex[0] << 4) | rssi_hex[1];
            break;
        }

        case UHF_TEMP_CMD: { // Get the internal temperature
            float *value = (float *)param;

            uint8_t dec[4] = {ans[3], ans[4], ans[5], ans[6]};
            convHexFromASCII(3, dec + 1);

            *value = (dec[1] * 10.0f) + (dec[2]) + (dec[3] / 10.0f);
            if (dec[0] == 0x2D)
                *value *= -1.0f;
            break;
        }
            //    case 11: {  // Get the i2c pull-up configuration
            //          uint8_t *value = (uint8_t *)param;
            //
            //          uint8_t hex[2] = {ans[3], ans[4]};
            //          convHexFromASCII(3, hex);
            //
            //          *value = hex[0] << 4 | hex[1];
            //          break;
            //        }

        case UHF_AX25_CMD: { // Get Low Power Mode Status
            uint8_t *status = (uint8_t *)param;
            *status = ans[4];
            convHexFromASCII(1, status);
            break;
        }

        case UHF_LOWPWR_CMD: { // Get Low Power Mode Status
            uint8_t *status = (uint8_t *)param;

            uint8_t hex[2] = {ans[blankspace_index - 2], ans[blankspace_index - 1]};
            convHexFromASCII(2, hex);
            *status = (hex[0] << 4) | hex[1];
            break;
        }

        case UHF_DSTCAL_CMD:   // Get Destination Call Sign
        case UHF_SRCCAL_CMD: { // Get Source Call Sign
            uhf_configStruct *callsign = (uhf_configStruct *)param;
            callsign->len = 6;

            for (int j = 0; j < callsign->len; j++) {
                callsign->message[j] = ans[blankspace_index + j - 6];
            }
            break;
        }

        case UHF_MORSECAL_CMD: { // Get Morse Code Call Sign
            uhf_configStruct *callsign = (uhf_configStruct *)param;
            uint8_t dec[2] = {ans[3], ans[4]};
            convHexFromASCII(2, dec);

            callsign->len = dec[0] * 10 + dec[1];

            for (int i = 0; i < callsign->len; i++) {
                uint8_t sym = ans[5 + i];
                callsign->message[i] = sym;
            }
            break;
        }

        case UHF_MIDIBCN_CMD: { // Get the MIDI Audio Beacon
            uhf_configStruct *beacon = (uhf_configStruct *)param;
            uint8_t dec[2] = {ans[3], ans[4]};
            convHexFromASCII(2, dec);

            beacon->len = dec[0] * 10 + dec[1];

            int j = 0;
            for (; j < beacon->len; j++) {
                beacon->message[3 * j] = ans[5 + 3 * j];
                beacon->message[3 * j + 1] = ans[6 + 3 * j];
                beacon->message[3 * j + 2] = ans[7 + 3 * j];
            }
            break;
        }

        case UHF_SWVER_CMD: { // Get Software Version build
            uint8_t *version = (uint8_t *)param;

            *version = ans[3];
            *(version + 1) = ans[4];
            *(version + 2) = ans[5];
            *(version + 3) = ans[6];
            break;
        }

        case UHF_PLDSZ_CMD: { // Get Device Payload Size
            uint16_t *p_size = (uint16_t *)param;

            uint8_t hex[4] = {ans[blankspace_index - 4], ans[blankspace_index - 3], ans[blankspace_index - 2],
                              ans[blankspace_index - 1]};
            convHexFromASCII(4, hex);

            *p_size = (hex[0] << 12) | (hex[1] << 8) | (hex[2] << 4) | hex[3];
            break;
        }

        case UHF_BCNMSG_CMD: { // Get the beacon message content
            uhf_configStruct *beacon = (uhf_configStruct *)param;
            uint8_t len[2] = {ans[3], ans[4]};
            convHexFromASCII(2, len);

            beacon->len = (len[0] << 4) | len[1];

            int i = 0;

            for (; i < beacon->len; i++) {
                uint8_t temp[2] = {ans[59 + 2 * i], ans[60 + 2 * i]};
                convHexFromASCII(2, temp);
                uint8_t val = (temp[0] << 4) | temp[1];
                beacon->message[i] = val;
                // TODO: Deal with beacon encoding (read value is different from write
                // value)
            }
            break;
        }

        case UHF_FRAM_CMD: { // FRAM memory read
            uhf_framStruct *fram_r = (uhf_framStruct *)param;

            int i = 0;
            for (; i < 16; i++) {
                uint8_t temp[2] = {ans[3 + 2 * i], ans[4 + 2 * i]};
                convHexFromASCII(2, temp);
                fram_r->data[i] = (temp[0] << 4) | temp[1];
            }
            break;
        }

        case UHF_SECURE_CMD: { // Secure Mode read
            uint32_t *key = (uint32_t *)param;

            uint8_t hex[8] = {ans[3], ans[4], ans[5], ans[6], ans[7], ans[8], ans[9], ans[10]};
            convHexFromASCII(8, hex);
            *key = (hex[0] << 28) | (hex[1] << 24) | (hex[2] << 20) | (hex[3] << 16) | (hex[4] << 12) |
                   (hex[5] << 8) | (hex[6] << 4) | hex[7];

            break;
        }

        default:
            return_val = U_BAD_PARAM;
        }
    }
    vPortFree(ans);
    return return_val;
}

/**
 * @brief
 *      Converts hex values to their ASCII characters
 * @param length
 *      Number of subsequent elements to convert
 * @param arr
 *      Pointer to start of char array
 */

void convHexToASCII(int length, uint8_t *arr) {
    int i = 0;
    for (; i < length; i++) {
        if (*(arr + i) < 10) {
            *(arr + i) += 48;
        } else {
            *(arr + i) += 55;
        }
    }
}

/**
 * @brief
 *      Converts ASCII characters to their hex values
 * @param length
 *      Number of subsequent elements to convert
 * @param arr
 *      Pointer to start of char array
 */

void convHexFromASCII(int length, uint8_t *arr) {
    for (int i = 0; i < length; i++) {
        if (*(arr + i) >= 65) {
            *(arr + i) -= 55;
        } else {
            *(arr + i) -= 48;
        }
    }
}

/**
 * @brief
 *      Calculates the CRC32 for a command and appends to
 *the end (as ASCII)
 * @details
 *      Taken from: https://github.com/Michaelangel007/crc32
 * @param length
 *      # of bytes in input
 * @param command_to_send
 *      Pointer to start of char array
 * @return uint32_t
 *      crc32 value (not used)
 */

static uint32_t crc32_calc(size_t length, char *command_to_send) {
    int count = length;
    const uint32_t POLY = 0xEDB88320;
    const unsigned char *buffer = (const unsigned char *) command_to_send;
    uint32_t crc = (uint32_t) -1;

    while (length--) {
        crc = crc ^ *buffer++;
        int i = 0;
        for (; i < 8; i++) {
            if (crc & 1) {
                crc = (crc >> 1) ^ POLY;
            } else {
                crc = (crc >> 1);
            }
        }
    }
    crc = ~crc;

    // Converting the CRC32 into hex then ascii
    uint8_t chex[8] = {0};
    int j = 7;
    for (; j >= 0; j--) {
        chex[j] = crc & 15;
        crc = crc >> 4;
        convHexToASCII(1, chex + j);
        *(command_to_send + count + j + 1) = chex[j];
    }

    return crc;
}

static UHF_return UHF_error_check(uint8_t *ans, uint8_t answer_length){

    UHF_return return_val = U_ANS_SUCCESS;
    char *ans_str = (char *)pvPortMalloc(sizeof(char)*(answer_length+1));
    memcpy(ans_str, ans, answer_length);
    *(ans_str + answer_length) = 0; // string terminator

        if (ans_str[0] != LETTER_O) {
            // Received error-type answer
            if (!strcmp(ans_str, "E_CRC_ERR 3D2B08DC\r")) {
                return_val = U_BAD_CMD_CRC;
            } else if (!strcmp(ans_str, "E_CRC_ERR_LEN 9B49857A\r")) {
                return_val = U_BAD_CMD_LEN;
            } else if (!strcmp(ans_str, "ERR 84F89937\r")) {
                return_val = U_ERR;
            } else if (!strcmp(ans_str, "ERR+REMOTE 6884D28\r")) {
                return_val = U_ERR_2;
            } else if (!strcmp(ans_str, "ERR+MIDI CA62190D\r")) {
                return_val = U_ERR_2;
            } else if (!strcmp(ans_str, "ERR+FB C76900C0\r")) {
                return_val = U_ERR_FB;
            } else if (!strcmp(ans_str, "ERR+CHKSUM 1105E41C\r")) {
                return_val = U_ERR_CHKSUM;
            } else if (!strcmp(ans_str, "ERR+FW AAC4E42B\r")) {
                return_val = U_ERR_FW;
            } else {
                return_val = U_UNKOWN;
            }
        } else {
            // Received "OK..."-type answer. Now check the CRC.
            char *crc_recalc = (char *)pvPortMalloc(sizeof(char) * (answer_length+1));
            memcpy(crc_recalc, ans_str, answer_length+1);
            crc32_calc(find_blankSpace(strlen(crc_recalc), crc_recalc), crc_recalc);

            if (strcmp(crc_recalc, ans_str)) {
                return_val = U_BAD_ANS_CRC;
            } else if (!strcmp(ans_str, "OK+F1F1 908A5EAB\r")) {
                return_val = U_FW_UPDATE_SUCCESS;
            }
            vPortFree(crc_recalc);
            vPortFree(ans_str);
        }
        return return_val;
}

/**
 * @brief
 *      For parsing: Returns the index of the last blank
 * space character
 * @param length
 *      Length of the string being checked
 * @param command_to_send
 *      Pointer to start of char array
 * @return int
 *      Index
 */

static int find_blankSpace(int length, char *command_to_send) {
    for (int k = length; k > 0; k--) {
        if (command_to_send[k] == BLANK_SPACE) {
            return k;
        }
    }
    return -2;
}

/**
 * @brief
 *      Allows access via UHF to i2c devices
 * @details
 *    Command must be sent over UART or Radio
 * @param format
 *      The way the data is sent ('S', 'C', or 'D')
 * @param s_address
 *      I2C slave device address
 * @param len
 *      Length of the data field
 * @param data
 *      Pointer to data to be sent over I2C bus
 * @return
 *      UHF_return
 */

UHF_return UHF_genericI2C(uint8_t format, uint8_t s_address, uint8_t len, uint8_t *data, uint8_t n_read_bytes) {
    uint8_t params[4] = {s_address >> 4, s_address & 15, len >> 4, len & 15};
    convHexToASCII(4, params);
    char command_to_send[MAX_UHF_W_CMDLEN] = {
        'E',    'S',       '+',       'W',       '2',      i2c_address_small_digit_ascii, 'F', '1',
        format, params[0], params[1], params[2], params[3], 0};

    int i = 0;
    for (; i < len; i++) {
        command_to_send[13 + 2 * i] = data[i] >> 4;
        command_to_send[13 + 2 * i + 1] = data[i] & 15;
        convHexToASCII(2, (uint8_t *) &command_to_send[13 + 2 * i]);
    }

    uint8_t hex_bytes[2] = {n_read_bytes >> 4, n_read_bytes & 15};
    convHexToASCII(2, hex_bytes);
    command_to_send[13 + 2 * i] = hex_bytes[0];
    command_to_send[13 + 2 * i + 1] = hex_bytes[1];
    command_to_send[13 + 2 * i + 2] = BLANK_SPACE;
    command_to_send[13 + 2 * i + 11] = CARRIAGE_R;

    crc32_calc(find_blankSpace(strlen(command_to_send), command_to_send), command_to_send);

    // TODO: Finish this function, which is missing the UART send command and
    // interpreting the response

    return U_GOOD_CONFIG;
}

/**
 * @brief
 *      Sends a firmware update command to the UHF
 * @details
 *      See "Firmware Update" section in User Manual
 * @param line
 *      Line of code from the .SCRM file as an ascii character array
 * @param line_length
 *      Number of characters in the line
 * @return
 *      UHF_return
 */
UHF_return UHF_firmwareUpdate(uint8_t *line, uint8_t line_length) {
    char firmware_command[MAX_UHF_W_CMDLEN] = {'E', 'S', '+', 'D', '2', i2c_address_small_digit_ascii};
    int i = 0;
    for (; i < line_length; i++) {
        firmware_command[6 + i] = *(line + i);
    }
    firmware_command[6 + i] = BLANK_SPACE;
    firmware_command[7 + i] = 'C';
    firmware_command[8 + i] = 'C';
    firmware_command[9 + i] = 'C';
    firmware_command[10 + i] = 'C';
    firmware_command[11 + i] = 'C';
    firmware_command[12 + i] = 'C';
    firmware_command[13 + i] = 'C';
    firmware_command[14 + i] = 'C';
    firmware_command[15 + i] = CARRIAGE_R;
    firmware_command[16 + i] = 0;
    
    crc32_calc(find_blankSpace(strlen((char *)firmware_command), firmware_command), firmware_command);

    uint8_t ans[UHF_WRITE_ANSLEN_FW] = {0};
    UHF_return return_val;

#ifndef UHF_USE_I2C_CMDS
        uhf_uart_sendAndReceive((uint8_t *)firmware_command, strlen(firmware_command), ans, UHF_WRITE_ANSLEN_FW);
#else
    uint8_t i2c_address = i2c_address_small_digit_ascii;
    convHexFromASCII(1, &i2c_address);
    i2c_address += 0x20; // Address is always 0x22 or 0x23
    return_val = i2c_sendAndReceive(i2c_address, firmware_command, strlen(firmware_command), ans,
                                    UHF_WRITE_ANSLEN_FW);
#endif

    // Handle errors
    if((return_val == U_I2C_SUCCESS) || (return_val == U_UART_SUCCESS)){
        return_val = UHF_error_check(ans, UHF_WRITE_ANSLEN_FW);
    }

    return return_val;
}
