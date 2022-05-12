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
  * @file gnuradio_interface.c
  * @author Josh Lazaruk
  * @date 2022-03-16
  */

//#include "i2c_dummy.h"
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

uint16_t crc16(uint8_t* pData, int length)
{
    uint8_t i;
    uint16_t wCrc = 0xffff;
    while (length--) {
        wCrc ^= *(unsigned char *)pData++ << 8;
        for (i=0; i < 8; i++)
            wCrc = wCrc & 0x8000 ? (wCrc << 1) ^ 0x1021 : wCrc << 1;
    }
    return wCrc & 0xffff;
}

bool i2c_package_for_radio(char *command, uint8_t command_len) {
    uint8_t crc_command[128] = {0};
    crc_command[0] = command_len;
    for( int i = 0; i < command_len; i++) {
        crc_command[1+i] = command[i];
    }

    uint16_t crc_res = crc16(crc_command, command_len+1);

    uint8_t radio_command[148] = {0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA,
                                  0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA}; // Gives 16 preamble bytes
    // radio_command[0] = 0xAA;
    // radio_command[1] = 0xAA;
    // radio_command[2] = 0xAA;
    // radio_command[3] = 0xAA;
    // radio_command[4] = 0xAA;
    radio_command[16] = 0x7E;
    radio_command[17] = command_len;
    for( int i = 0; i < command_len; i++) {
        radio_command[18+i] = command[i];
    }

    radio_command[18+command_len] = ((uint16_t)crc_res >> 8) & 0xFF;
    radio_command[18+command_len+1] = ((uint16_t)crc_res >> 0) & 0xFF;

    FILE *fptr = fopen("output.bin","w");

    int radio_len = 16+2+command_len+2;
    fwrite(radio_command, sizeof(uint8_t), radio_len, fptr);
    uint8_t val = 0xAA;
    for(int i = 0; i < 10; i++){
        fwrite(&val, sizeof(uint8_t), 1, fptr);
    }
    
    // for( int i = 0; i < radio_len; i++){

    //   printf("%c", radio_command[i]);
    // }
    fclose(fptr);

    //printf("sending command to gnuradio from C\n");
    int status = system("cat output.bin | nc -w 1 127.0.0.1 1234");

    return true;
}
