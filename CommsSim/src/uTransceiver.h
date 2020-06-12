// uTransceiver.h
// Author: Thomas Ganley
// May 28, 2020

#ifndef UTRANSCEIVER_H
#define UTRANSCEIVER_H

#include "mock_i2c.h"
#include <stdint.h>
#include <string.h>

#define MAX_M_LEN 120

typedef enum{
	U_GOOD_CONFIG =  0,
	U_BAD_CONFIG  = -1,
	U_BAD_PARAM   = -2,
	U_BAD_ANS_CRC = -3,

	U_BAD_CMD_CRC = -4,
	U_BAD_CMD_LEN = -5,
	U_CMD_SPEC_2  =  2,
	U_CMD_SPEC_3  =  3,

	U_UNK_ERR     = -10,
}U_ret;

struct U_config {
	uint8_t len;
	uint8_t message[MAX_M_LEN];
};

struct U_fram {
	uint32_t add;
	uint8_t data[16];
};

// Converts hex values to their ASCII characters
void convHexToASCII(int length, uint8_t * arr);
void convHexFromASCII(int length, uint8_t * arr);
uint32_t crc32_calc(size_t length, char * cmd);
int find_blankSpace(char * string, int len);

int generic_U_write(uint8_t code, void * param);
int generic_U_read(uint8_t code, void * param);
#endif // UTRANSCEIVER_H
