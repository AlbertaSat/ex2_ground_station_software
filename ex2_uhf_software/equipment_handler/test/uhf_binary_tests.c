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
 * @file sband_binary_tests.c
 * @author Thomas Ganley
 * @date 2022-01-04
 */

#include "uTransceiver.h"

UHF_return uhf_binary_test() {

     uint8_t UHF_return;
     uint8_t scw[12] = {0};
     uint32_t pipe_timeout = 0;
     uint32_t freq = 437875000;

     UHF_genericWrite(UHF_FREQ_CMD, &freq);

     UHF_return = UHF_genericRead(UHF_SCW_CMD, scw);
     UHF_return = UHF_genericRead(UHF_PIPET_CMD, &pipe_timeout);
     scw[UHF_SCW_UARTBAUD_INDEX] = UHF_UARTBAUD_19200;
     scw[UHF_SCW_RFMODE_INDEX] = UHF_RFMODE7;
     scw[UHF_SCW_BCN_INDEX] = UHF_BCN_OFF;
     scw[UHF_SCW_PIPE_INDEX] = UHF_PIPE_ON;
     pipe_timeout = 40;
     UHF_return = UHF_genericWrite(UHF_PIPET_CMD, &pipe_timeout);
     UHF_return = UHF_genericWrite(UHF_SCW_CMD, scw);

     uint8_t data[18] = {1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9};
     for (uint8_t i = 0; i < 0x1000; i++);
     sciSend(UHF_SCI, 18, data);
     for (uint8_t i = 0; i < 0x100000; i++);
     sciSend(UHF_SCI, 18, data);
     for (uint8_t i = 0; i < 0x100000; i++);
     sciSend(UHF_SCI, 18, data);
     for (uint8_t i = 0; i < 0x100000; i++);

    return U_UART_SUCCESS;
}
