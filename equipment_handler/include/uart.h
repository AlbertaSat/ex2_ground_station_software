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
 * @file uart.h
 * @author Thomas Ganley
 * @date 2021-08-23
 */

#ifndef EX2_HAL_EX2_UHF_SOFTWARE_EQUIPMENT_HANDLER_INCLUDE_UART_H_
#define EX2_HAL_EX2_UHF_SOFTWARE_EQUIPMENT_HANDLER_INCLUDE_UART_H_

void uart_send(uint32_t length, uint8_t * data);

void uart_sendAndReceive(uint32_t command_length, uint8_t * command, uint32_t answer_length, uint8_t * ans);


#endif /* EX2_HAL_EX2_UHF_SOFTWARE_EQUIPMENT_HANDLER_INCLUDE_UART_H_ */
