// uTransceiver.c
// Author: Thomas Ganley
// May 28, 2020

#include "uTransceiver.h"

// Converts hex values to their ASCII characters
int convHexToASCII(int length, uint8_t * arr)
{
        for(int i = 0; i < length; i++){
                if(*(arr + i) < 10){
                        *(arr + i) += 48;
                }else{
                        *(arr + i) += 55;
                }
        }
}

// Calculates the CRC32 for a command (may not need eventually)
uint32_t crc32_calc(size_t length, const void * cmd)
{
	const uint32_t POLY = 0xEDB88320;
	const unsigned char *buffer = (const unsigned char *)cmd;
	uint32_t crc = -1;

	while(length--){
		crc = crc ^ *buffer++;
		for(int i = 0; i < 8; i++){
			if(crc & 1){ crc = (crc >> 1) ^ POLY;}
			else{ crc = (crc >> 1);}
		}
	}
	return ~crc;
}


int set_U_control(uint8_t * array)
{
        uint8_t hex[8] = {0};

        // Grouping params into 4 bits (hex values)
        hex[0] = (array[0] << 2) | (array[1]);
        hex[1] = (array[2] << 3) | (array[3]);
        hex[2] = (array[4] << 3) | (array[5] << 2) | (array[6] << 1) | (array[7]);
        hex[3] = (array[8] << 3) | (array[9] << 2) | (array[10] << 1) | (array[11]);

        convHexToASCII(4, hex);

        uint8_t command[22] = {'E','S','+','W','2','2','0','0', hex[0], hex[1], hex[2], hex[3], ' ', 'C','C','C','C','C','C','C','C','\r'};
        uint32_t crc = crc32_calc(13, command);
	
	// Converting the CRC32 into hex then ascii
	uint8_t chex[8] = {0};
	chex[0] = (crc >> 28) & 15;
	chex[1] = (crc >> 24) & 15;
	chex[2] = (crc >> 20) & 15;
	chex[3] = (crc >> 16) & 15;
	chex[4] = (crc >> 12) & 15;
	chex[5] = (crc >> 8) & 15;
	chex[6] = (crc >> 4) & 15;
	chex[7] = crc & 15;
	
	convHexToASCII(8,chex);
	printf("%s\n",chex);
	
	command[13] = chex[0];
	command[14] = chex[1];
	command[15] = chex[2];
	command[16] = chex[3];
	command[17] = chex[4];
	command[18] = chex[5];
	command[19] = chex[6];
	command[20] = chex[7];

	printf("%s\n", command);
	
	uint8_t ans[20] = {0};
	i2c_sendCommand(22, command, ans);
	printf("%s\n", ans);
}

int get_U_control(uint8_t * array)
{
	uint8_t command[18] = {'E','S','+','R','2','2','0','0',' ','C','C','C','C','C','C','C','C','\r'};
}
