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

// Convests ASCII characters to their hex values
int convHexFromASCII(int length, uint8_t * arr)
{
	for(int i = 0; i < length; i++){
		if(*(arr + i) >= 65){
			*(arr + i) -= 55;
		}else{
			*(arr + i) -= 48;
		}
	}
}

// Calculates the CRC32 for a command (may not need eventually)
int crc32_calc(size_t length, char * cmd)
{	
	int count = length;
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
	crc = ~crc;

	// Converting the CRC32 into hex then ascii
        uint8_t chex[8] = {0};
        for(int j = 7; j >= 0; j--){
                chex[j] = crc & 15;
                crc = crc >> 4;
                convHexToASCII(1, chex + j);
                *(cmd + count + j + 1) = chex[j];
        }

}

// Returns the index of the first blank space character
int find_blankSpace(char * string)
{
	for(int k = 0; k<50; k++){
		if(string[k] == 0x20){
			return k;
		}
	}
}

// Recalculate the crc32 of the answer
int check_crc32(int len, char * ans)
{
	uint8_t answer[30] = {0};
	for(int i = 0; i < len; i++){
		answer[i] = *(ans+i);
	}

	uint8_t expected[30] = {0};
	strcpy(expected, answer);
	
	crc32_calc(find_blankSpace(answer), expected);

	if(!strcmp(expected, answer)){
		return 0;
	}else{
		return 1;
	}
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

	// Building the command
        uint8_t command[23] = {'E','S','+','W','2','2','0','0', hex[0], hex[1], hex[2], hex[3],' ','C','C','C','C','C','C','C','C','\r','\0'};
        crc32_calc(find_blankSpace(command), command);
	uint8_t ans[20] = {0};
	i2c_sendCommand(strlen(command), command, ans);

	// Checking the answer
	if(ans[0] == 0x4F){
		if(!check_crc32(strlen(ans), ans)){
			return 0;
		}else{
			return 2;
		}
	}else{
		return 1;
	}

}


int get_U_control(uint8_t * array)
{
	uint8_t command[19] = {'E','S','+','R','2','2','0','0',' ','C','C','C','C','C','C','C','C','\r','\0'};
	crc32_calc(find_blankSpace(command), command);

	uint8_t ans[30] = {0};
	i2c_sendCommand(strlen(command), command, ans);

	if(!check_crc32(strlen(ans), ans)){

	}else{
		return 2;
	}

	int b_index = find_blankSpace(ans);
	uint8_t hex[4] = {ans[b_index - 4], ans[b_index - 3], ans[b_index - 2], ans[b_index - 1]};
	convHexFromASCII(4, hex);
	
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

	return 0;
}
