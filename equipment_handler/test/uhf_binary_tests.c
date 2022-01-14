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

UHF_return uhf_binary_test(){
    //Read from the UHF
//    uint8_t UHF_return;
//    uint8_t scw[12] = {0};
//    uint32_t pipe_timeout = 0;
//    uint32_t freq = 437875000;
//
//    UHF_genericWrite(1, &freq);
//
//    UHF_return = UHF_genericRead(0, scw);
//    UHF_return = UHF_genericRead(6, &pipe_timeout);
//    scw[UHF_SCW_UARTBAUD_INDEX] = UHF_UARTBAUD_19200;
//    scw[UHF_SCW_RFMODE_INDEX] = UHF_RFMODE7;
//    scw[UHF_SCW_BCN_INDEX] = UHF_BCN_OFF;
//    scw[UHF_SCW_PIPE_INDEX] = UHF_PIPE_ON;
//    pipe_timeout = 40;
//
//    UHF_return = UHF_genericWrite(6, &pipe_timeout);
//    UHF_return = UHF_genericWrite(0, scw);

   //    uint8_t data[18] = {1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9};
   //    for (uint8_t i = 0; i < 0x1000; i++);
   //    sciSend(UHF_SCI, 18, data);
   //    for (uint8_t i = 0; i < 0x100000; i++);
   //    sciSend(UHF_SCI, 18, data);
   //    for (uint8_t i = 0; i < 0x100000; i++);
   //    sciSend(UHF_SCI, 18, data);
   //    for (uint8_t i = 0; i < 0x100000; i++);

   //    int res = csp_ping(EPS_APP_ID, 10000, 100, CSP_O_NONE);
   //    uint32 returned = sciReceiveByte(UHF_SCI);
   //
   //    int counter = 0;
   //    for(counter; counter < 0x800000; counter++);

   // Change to pipe mode
   // scw[UHF_SCW_PIPE_INDEX] = UHF_PIPE_ON;

   // Send the new configuration (write to pipe mode)
   //    UHF_return = UHF_genericWrite(0, scw);
}
