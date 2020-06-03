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

// Converts ASCII characters to their hex values
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
int find_blankSpace(char * string, int len)
{
	for(int k = len; k>0; k--){
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
	
	crc32_calc(find_blankSpace(answer, strlen(answer)), expected);

	if(strcmp(expected, answer)) return 1;
}

int generic_U_write(uint8_t code, void * param)
{
	uint8_t cmd[30] = {0};

	switch(code){

		case 0: {// Set the status control word
			uint8_t * array = (uint8_t *)param;
			uint8_t hex[8] = {0};
	
		        // Grouping params into 4 bits (hex values)
		        hex[0] = (*(array) << 2) | *(array+1);
	        	hex[1] = (*(array+2) << 3) | *(array+3);
		        hex[2] = (*(array+4) << 3) | (*(array+5) << 2) | (*(array+6) << 1) | (*(array+7));
		        hex[3] = (*(array+8) << 3) | (*(array+9) << 2) | (*(array+10) << 1) | (*(array+11));
		
		        convHexToASCII(4, hex);
			
		        // Building the command
		        uint8_t command[30] = {'E','S','+','W','2','2','0','0',hex[0],hex[1],hex[2],hex[3],' ','C','C','C','C','C','C','C','C','\r'};
			strcpy(cmd, command);
			break;
			}	


		case 1: {// Set the frequency (Unsure if correct-> index 5 of hex?)
			uint32_t * new_freq = (uint32_t *)param;
			if(*new_freq < 435000000 || *new_freq > 438000000) return 1;
			
			float temp = (*new_freq)/6500000.0f;
			uint8_t val1 = (uint8_t)temp - 1; //Integer term
			uint32_t val2 = (uint32_t)((temp - val1)*524288); // Fractional term
			uint8_t hex[8] = {(val2>>16)&15, (val2>>12)&15, (val2>>8)&15, (val2>>4)&15, (val2)&15, 15, (val1>>4)&15, (val1)&15};
			convHexToASCII(8, hex);
			
			// Building the command
			uint8_t command[30] = {'E','S','+','W','2','2','0','1',hex[0],hex[1],hex[2],hex[3],hex[4],hex[5],hex[6],hex[7],' ','C','C','C','C','C','C','C','C','\r'};
			strcpy(cmd, command);
			break;
			}


		case 6: {// Set PIPE mode Timeout Period
			uint8_t * time = (uint8_t *)param;

			uint8_t hex[2] = {(*time) >> 4, (*time) & 15};
			convHexToASCII(2, hex);

			uint8_t command[30] = {'E','S','+','W','2','2','0','6','0','0','0','0','0','0',hex[0],hex[1],' ','C','C','C','C','C','C','C','C','\r'};
			strcpy(cmd, command);
			break;
			}


		case 9: {// Restore Default Values
			uint8_t * confirm = (uint8_t *)param;
			if(*confirm != 1) return 1;
			uint8_t command[20] = {'E','S','+','W','2','2','0','9',' ','C','C','C','C','C','C','C','C','\r'};
			strcpy(cmd, command);
			break;
			}
		

		case 241:{// Generic write and/or read from an i2c device
			uint8_t command[30];
			strcpy(cmd, command);
			}


		default: return 1;
	}
	
	// Calculate crc32 & send command
	crc32_calc(find_blankSpace(cmd, strlen(cmd)), cmd);
        uint8_t ans[30] = {0};
        i2c_sendCommand(strlen(cmd), cmd, ans);
	printf("write %d cmd: %s\n", code, cmd);
	printf("write %d ans: %s\n", code, ans);
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

int generic_U_read(uint8_t code, void * param)
{
	uint8_t c1 = (code >> 4) & 15;
	uint8_t c2 = code & 15;
	convHexToASCII(1, &c1);
	convHexToASCII(1, &c2);

	uint8_t command[20] = {'E','S','+','R','2','2',c1,c2,' ','C','C','C','C','C','C','C','C','\r'};
	crc32_calc(find_blankSpace(command, strlen(command)), command);
		
        uint8_t ans[30] = {0};
        i2c_sendCommand(strlen(command), command, ans);
	int b = find_blankSpace(ans,strlen(ans));

	printf("read  %d cmd: %s\n", code, command);
	printf("read  %d ans: %s\n", code, ans);
        if(check_crc32(strlen(ans), ans)) return 2;

	switch(code){
		case 0:{// Get the status control word
			uint8_t * array = (uint8_t *)param;

			uint8_t hex[4] = {ans[b-4], ans[b-3], ans[b-2], ans[b-1]};
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


		case 1: {// Get the frequency (Unsure if this is correct-> index 5 of hex is unused
			uint32_t * freq = (uint32_t *)param;

			uint8_t hex[8] = {ans[b-8], ans[b-7], ans[b-6], ans[b-5], ans[b-4], ans[b-3], ans[b-2], ans[b-1]};
			convHexFromASCII(8,hex);
			
			uint8_t val1 = (hex[6] << 4) | hex[7];
			uint32_t val2 = (hex[0] << 16) | (hex[1] << 12) | (hex[2] << 8) | (hex[3] << 4) | hex[4];

			*freq = (val1 + (val2/524288.0f))*6500000.0f;

			// Compute the RSSI
			uint8_t rssi_hex[2] = {ans[b-10], ans[b-9]};
			convHexFromASCII(2, rssi_hex);

			*(freq + 1) = (rssi_hex[0] << 4) | rssi_hex[1];
			break;
			}


		case 2: // Get uptime
		case 3: // Get # of transmitted packets
		case 4: // Get # of received packets
		case 5: // Get # of received packets w CRC16 error
		case 6: // Get the PIPE Mode timeout
		case 7: // Get Beacon transmission period
		case 8: // Get Audio Beacon period
		       	{
			uint32_t * value = (uint32_t *)param;

			uint8_t hex[8] = {ans[b-8],ans[b-7],ans[b-6],ans[b-5],ans[b-4],ans[b-3],ans[b-2],ans[b-1]};
			convHexFromASCII(8,hex);
			
			*value = (hex[0]<<28) | (hex[1]<<24) | (hex[2]<<20) | (hex[3]<<16) | (hex[4]<<12) | (hex[5]<<8) | (hex[6]<<4) | hex[7];
			
			// Compute the RSSI
                        uint8_t rssi_hex[2] = {ans[b-10], ans[b-9]};
                        convHexFromASCII(2, rssi_hex);

                        *(value + 1) = (rssi_hex[0] << 4) | rssi_hex[1];
			break;
			}
			
		case 10:{
			float * value = (float*)param;

			uint8_t dec[4] = {ans[3],ans[4],ans[5],ans[6]};
			convHexFromASCII(3, dec+1);
			
			*value = (dec[1]*10.0f) + (dec[2]) + (dec[3]/10.0f);
			if(dec[0] == 0x2D) *value *= -1.0f;
			}
		default:
			return 1;
	}
}
