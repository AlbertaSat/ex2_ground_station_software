// uTransceiver.c
// Author: Thomas Ganley
// May 28, 2020

#include "uTransceiver.h"

static uint8_t sm_add = '2'; // Stores the second digit of the address

U_ret generic_U_write(uint8_t code, void * param)
{
	uint8_t cmd[120] = {0};

	/* The following switch statement depends on the command code to:    *
	 * 	- Calculate necessary ASCII characters from input parameters *
	 * 	- Build the command to be sent                               */

	switch(code){

		case 0: {// Set the status control word
			uint8_t * array = (uint8_t *)param;
			uint8_t hex[4] = {0};
	
		        // Grouping params into 4 bits (hex values)
		        hex[0] = (*(array) << 2) | *(array+1);
	        	hex[1] = (*(array+2) << 3) | *(array+3);
		        hex[2] = (*(array+4) << 3) | (*(array+5) << 2) | (*(array+6) << 1) | (*(array+7));
		        hex[3] = (*(array+8) << 3) | (*(array+9) << 2) | (*(array+10) << 1) | (*(array+11));
			
			convHexToASCII(4, hex);
		        // Building the command
		        uint8_t command[30] = {'E','S','+','W','2',sm_add,'0','0',hex[0],hex[1],hex[2],hex[3],' ','C','C','C','C','C','C','C','C','\r'};
			strcpy(cmd, command);
			break;
			}	


		case 1: {// Set the frequency (Unsure if correct-> index 5 of hex?)
			uint32_t * new_freq = (uint32_t *)param;
			if(*new_freq < 435000000 || *new_freq > 438000000) return U_BAD_PARAM;
			
			float temp = (*new_freq)/6500000.0f;
			uint8_t val1 = (uint8_t)temp - 1; //Integer term
			uint32_t val2 = (uint32_t)((temp - val1)*524288); // Fractional term
			uint8_t hex[8] = {(val2>>16)&15, (val2>>12)&15, (val2>>8)&15, (val2>>4)&15, (val2)&15, 15, (val1>>4)&15, (val1)&15};
			convHexToASCII(8, hex);
			
			// Building the command
			uint8_t command[30] = {'E','S','+','W','2',sm_add,'0','1',hex[0],hex[1],hex[2],hex[3],hex[4],hex[5],hex[6],hex[7],' ','C','C','C','C','C','C','C','C','\r'};
			strcpy(cmd, command);
			break;
			}


		case 6: // Set PIPE mode Timeout Period
		case 7: // Set Beacon Transmission Period
		case 8:	// Set Audio Beacon Transmission Period
			{
			uint16_t * time = (uint16_t *)param;

			uint8_t hex[4]= {(*time >> 12)&15, (*time >> 8)&15, (*time >> 4)&15, (*time) & 15};
			convHexToASCII(4, hex);

			uint8_t command[30] = {'E','S','+','W','2',sm_add,'0','6','0','0','0','0',hex[0],hex[1],hex[2],hex[3],' ','C','C','C','C','C','C','C','C','\r'};
			strcpy(cmd, command);
			break;
			}


		case 9: {// Restore Default Values
			uint8_t * confirm = (uint8_t *)param;
			if(*confirm != 1) return U_BAD_PARAM;
			uint8_t command[20] = {'E','S','+','W','2',sm_add,'0','9',' ','C','C','C','C','C','C','C','C','\r'};
			strcpy(cmd, command);
			break;
			}
		

		case 244:{// Enter low power mode
			uint8_t * confirm = (uint8_t *)param;
			if(*confirm != 1) return U_BAD_PARAM;
			uint8_t command[30] = {'E','S','+','W','2',sm_add,'F','4',' ','C','C','C','C','C','C','C','C','\r'};
			strcpy(cmd, command);
			break;
			}


		case 245: // Set Destination Call Sign
		case 246: // Set Source Call Sign
			{
			struct U_config * sign = (struct U_config *)param;
			uint8_t command[30] = {'E','S','+','W','2',sm_add,'F',(uint8_t)code-192,sign->message[0],sign->message[1],sign->message[2],sign->message[3],sign->message[4],sign->message[5],' ','C','C','C','C','C','C','C','C','\r'};
			strcpy(cmd, command);
			break;
			} 
		

		case 247:{ // Set Morse Code Call Sign
			struct U_config * callsign = (struct U_config *)param;
			uint8_t len[2] = {(callsign->len - (callsign->len % 10))/10, callsign->len % 10};
			convHexToASCII(2, len);
			uint8_t command[60] = {'E','S','+','W','2',sm_add,'F','7',len[0],len[1]};
			int i = 0;
			for(i; i < callsign->len; i++){
				uint8_t sym = callsign->message[i];
				if(sym != 0x2D && sym != 0x2E && sym != 0x20) return U_BAD_PARAM;
				command[10+i] = sym;
			}
			command[10+i] = 0x20;
			command[19+i] = 0x0D;
			strcpy(cmd, command);
			break;
			}


		case 248:{ // Set the MIDI Audio Beacon
			struct U_config * beacon = (struct U_config *)param;
			uint8_t len[2] = {(beacon->len - (beacon->len % 10))/10, beacon->len % 10};
			convHexToASCII(2, len);
			uint8_t command[120] = {'E','S','+','W','2',sm_add,'F','8',len[0],len[1]};
			uint8_t j = 0;
			uint8_t count = 0;
			for(j; j < beacon->len; j++){
				uint8_t midi = beacon->message[2*j];
				uint8_t sym = beacon->message[2*j+1];
				
				if(midi < 12 || midi > 99) return U_BAD_PARAM;
				uint8_t len_chars[2] = {(midi - (midi % 10))/10, midi % 10};
				convHexToASCII(2, len_chars);
				command[10+3*j] = len_chars[0];
				command[11+3*j] = len_chars[1];
				command[12+3*j] = sym;
			}
			command[10+j+count] = 0x20;
			command[19+j+count] = 0x0D;
			strcpy(cmd, command);
			break;
			}


		case 251:{ // Set the Beacon Message contents
			struct U_config * beacon = (struct U_config *)param;
			uint8_t len[2] = {(beacon->len - (beacon->len % 10))/10, beacon->len % 10};
			convHexToASCII(2, len);

			uint8_t command[120] = {'E','S','+','W','2',sm_add,'F','B',len[0],len[1]};
			int k = 0;

			for(k; k < beacon->len; k++){
				command[10+k] = beacon->message[k];
			}
			command[10+k] = 0x20;
			command[19+k] = 0x0D;
			strcpy(cmd, command);
			break;			
			}
			 

		case 252:{ // Set the device address
			uint8_t * add = (uint8_t *)param;

			if(*add != 0x22 && *add != 0x23) return U_BAD_PARAM;
			uint8_t small = *add - 32;
			convHexToASCII(1, &small);
			uint8_t command[20] = {'E','S','+','W','2',sm_add,'F','C','2',small,' ','C','C','C','C','C','C','C','C','\r'};
			strcpy(cmd, command);
			break;
			}


		case 253:{ // FRAM memory write
			struct U_fram * fram_w = (struct U_fram *)param;

			uint32_t add = fram_w->add;
			if(add >= 0x8000 && add <= 0x83A4) return U_BAD_PARAM;
			if(add >= 0x83FE && add <= 0x24000) return U_BAD_PARAM;
			
			uint8_t chadd[8] = {add >> 28, (add >> 24) & 15, (add >> 20) & 15, (add >> 16) & 15, (add >> 12) & 15, (add >> 8) & 15, (add >> 4) & 15, add & 15};
			convHexToASCII(8, chadd);

			uint8_t command[60] = {'E','S','+','W','2',sm_add,'F','D',chadd[0],chadd[1],chadd[2],chadd[3],chadd[4],chadd[5],chadd[6],chadd[7], [48] = ' ', [57] = 0x0D};
			uint8_t hex[2] = {0};
			for(int i = 0; i < 16; i++){
				hex[0] = fram_w->data[i] >> 4;
				hex[1] = fram_w->data[i] & 15;
				convHexToASCII(2, hex);
				
				command[16 + 2*i] = hex[0];
				command[16 + 2*i + 1] = hex[1];
			}
			
			strcpy(cmd, command);
			break;
			}


		case 255:{ // Secure Mode write
			uint8_t * confirm = (uint8_t *)param;
			if(*confirm != 1) return U_BAD_PARAM;

			uint8_t command[20] = {'E','S','+','W','2',sm_add,'F','F',' ','C','C','C','C','C','C','C','C', 0x0D};
			strcpy(cmd, command);
			break;
			}


		default: return U_BAD_CONFIG;
	}


	/* The following is necessary for all write commands: *
	 * 	- Calculate the crc32                         *
	 * 	- Send the command and receive the answer     * 
	 * 	- Checking the crc32 of the answer            * 
	 * 	- Checking for an answer indicating an error  */

	crc32_calc(find_blankSpace(cmd, strlen(cmd)), cmd);
        uint8_t ans[30] = {0};
        i2c_sendCommand(strlen(cmd), cmd, ans);

	if(ans[0] == 'E'){
		
		// Error answers intrinsic to all commands (unsure about exact format of these)
		if(!strcmp(ans, "E_CRC_ERR\r")) return U_BAD_CMD_CRC;
	        if(!strcmp(ans, "E_CRC_ERR_LEN\r")) return U_BAD_CMD_LEN;

		switch(code){
			case 1: 
			case 6:
			case 7:
			case 8:
			case 244:
			case 247:
			case 251:
			case 253:
			case 254:
			case 255:
				return U_CMD_SPEC_2;
				break;
			case 248:
				if(ans[4] == 'M') return U_CMD_SPEC_2;
				return U_CMD_SPEC_3;

			default: return U_UNK_ERR;
		}
	}

	uint8_t expected[120] = {0};
        strcpy(expected, ans);
        crc32_calc(find_blankSpace(expected, strlen(expected)), expected);
	
	printf("write %d cmd: %s\n", code, cmd);
	printf("write %d ans: %s\n", code, ans);

        if(ans[0] == 0x4F){
		if(code == 252) sm_add = ans[4];
                if(!strcmp(expected, ans)){
                        return U_GOOD_CONFIG;
                }else{
                        return U_BAD_ANS_CRC;
                }
        }else{
                return U_BAD_CONFIG;
	}
}



U_ret generic_U_read(uint8_t code, void * param)
{                                                                 
	/* The following is necessary for all read commands:                 *   
	 * 	- Determining ASCII characters representing the command code *
	 * 	- Calculating the crc32                                      *
	 * 	- Sending the command and receiving the answer               *  
	 * 	- Checking the crc32 of the answer                           * 
	 * 	- Checking for an answer indicating an error                 */
	
	uint8_t code_chars[2] = {(code >> 4) & 15, code & 15};
	convHexToASCII(2, code_chars);

	uint8_t command[30] = {'E','S','+','R','2',sm_add,code_chars[0],code_chars[1],' ','C','C','C','C','C','C','C','C','\r'};
	
	if(code == 253){
		struct U_fram * fram_struct = (struct U_fram *)param;

                uint32_t add = fram_struct->add;
                if(add >= 0x8000 && add <= 0x83A4) return U_BAD_PARAM;
                if(add >= 0x83FE && add <= 0x24000) return U_BAD_PARAM;

                uint8_t chadd[8] = {add >> 28, (add >> 24) & 15, (add >> 20) & 15, (add >> 16) & 15, (add >> 12) & 15, (add >> 8) & 15, (add >> 4) & 15, add & 15};
                convHexToASCII(8, chadd);

		uint8_t fram_command[30] = {'E','S','+','R','2',sm_add,chadd[0],chadd[1],chadd[2],chadd[3],chadd[4],chadd[5],chadd[6],chadd[7],' ',[25]=0x0D};
		strcpy(command, fram_command);
	}

	crc32_calc(find_blankSpace(command, strlen(command)), command);
		
        uint8_t ans[150] = {0};
        i2c_sendCommand(strlen(command), command, ans);

	if(ans[0] == 'E'){

                // Error answers intrinsic to all commands (unsure about exact format of these)
                if(!strcmp(ans, "E_CRC_ERR\r")) return U_BAD_CMD_CRC;
                if(!strcmp(ans, "E_CRC_ERR_LEN\r")) return U_BAD_CMD_LEN;

                if(code == 251 || code == 253 || code == 254) return U_CMD_SPEC_2;
                return U_UNK_ERR;
        }
        
	int b = find_blankSpace(ans,strlen(ans));

	printf("read  %d cmd: %s\n", code, command); //*
	printf("read  %d ans: %s\n", code, ans); //*
        
	uint8_t expected[150] = {0};
        strcpy(expected, ans);
        crc32_calc(find_blankSpace(expected, strlen(expected)), expected);

        if(ans[0] == 0x4F){
                if(strcmp(expected, ans)){            
			printf("Bad crc: %s\n",expected);
                        return U_BAD_ANS_CRC;
                }
        }


	/* This switch statement depends on the command code to: *
	 * 	- Interpret the answer                           *
	 * 	- Calculate relevant parameters                  *
	 * 	- Save these in *param and subsequent pointers   */

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
			

		case 10:{ // Get the internal temperature
			float * value = (float*)param;

			uint8_t dec[4] = {ans[3],ans[4],ans[5],ans[6]};
			convHexFromASCII(3, dec+1);
			
			*value = (dec[1]*10.0f) + (dec[2]) + (dec[3]/10.0f);
			if(dec[0] == 0x2D) *value *= -1.0f;
			break;
			}


		case 244:{ // Get Low Power Mode Status
			uint8_t * status = (uint8_t *)param;

			uint8_t hex[2] = {ans[b-2], ans[b-1]};
			convHexFromASCII(2, hex);
			*status = (hex[0] << 4) | hex[1];
			break;
			}


		case 245: // Get Destination Call Sign
		case 246:{// Get Source Call Sign
			struct U_config * callsign = (struct U_config *)param;	
			for(int j = 0 ; j<6;j++){
				callsign->message[j] = ans[b + j -6];
			}
			break;
			}


		case 247:{// Get Morse Code Call Sign
			struct U_config * callsign = (struct U_config *)param;
			uint8_t dec[2] = {ans[3],ans[4]};
			convHexFromASCII(2, dec);

			callsign->len = dec[0] * 10 + dec[1];

			for(int i = 0; i < callsign->len; i++){
				uint8_t sym = ans[5+i];			
				callsign->message[i] = sym;
			}
			break;
			}


		case 248:{ // Get the MIDI Audio Beacon
			struct U_config * beacon = (struct U_config *)param;
			uint8_t dec[2] = {ans[3],ans[4]};
			convHexFromASCII(2, dec);
			
			beacon->len = dec[0] * 10 + dec[1];
			
			for(int j = 0; j < beacon->len; j++){
				uint8_t chars[2] = {ans[5+3*j], ans[6+3*j]};
				convHexFromASCII(2, chars);

				uint8_t sym = ans[7+3*j];
				
				beacon->message[2*j] = chars[0] * 10 + chars[1];
				beacon->message[2*j+1] = sym;
			}
			break;
			}


		case 249:{ // Get Software Version build
			uint8_t * version = (uint8_t *)param;

			*version = ans[3];
			*(version + 1) = ans[4];
			*(version + 2) = ans[5];
			*(version + 3) = ans[6];
			break;
			}

			 
		case 250:{ // Get Device Payload Size
			uint16_t * p_size = (uint16_t *)param;
			
			uint8_t hex[4] = {ans[b-4], ans[b-3], ans[b-2], ans[b-1]};
			convHexFromASCII(4, hex);

			*p_size = (hex[0] << 12) | (hex[1] << 8) | (hex[2] << 4) | hex[3];
			break;
			}


		case 251:{ // Get the beacon message content
			struct U_config * beacon = (struct U_config *)param;
			uint8_t len[2] = {ans[3], ans[4]};
			convHexFromASCII(2, len);
			
			beacon->len = (len[0] << 4) | len[1];
			
			for(int i = 0; i < beacon->len; i++){
				uint8_t temp[2] = {ans[59 + 2*i], ans[60 + 2*i]};
				convHexFromASCII(2, temp);
				uint8_t val = (temp[0] << 4) | temp[1];
				beacon->message[i] = val;
			}
			break;
			}


		case 253:{ // FRAM memory read
			struct U_fram * fram_r = (struct U_fram *)param;
			uint8_t hex[32] = {0};
			
			for(int i = 0; i < 16; i++){
				uint8_t temp[2] = {ans[3+2*i], ans[4+2*i]};
				convHexFromASCII(2, temp);
				fram_r->data[i] = (temp[0] << 4) | temp[1];
			}
			break;
			}


		case 255:{ // Secure Mode read
			uint32_t * key = (uint32_t *)param;
	       		
			uint8_t hex[8] = {ans[3],ans[4],ans[5],ans[6],ans[7],ans[8],ans[9], ans[10]};
			convHexFromASCII(8, hex);
			*key = (hex[0]<<28) | (hex[1]<<24) | (hex[2]<<20) | (hex[3]<<16) | (hex[4]<<12) | (hex[5]<<8) | (hex[6]<<4) | hex[7];
		
			break;		
			}


		default:
			return U_BAD_CONFIG;
	}
	return U_GOOD_CONFIG;
}

// Converts hex values to their ASCII characters
void convHexToASCII(int length, uint8_t * arr)
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
void convHexFromASCII(int length, uint8_t * arr)
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
uint32_t crc32_calc(size_t length, char * cmd)
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

        return crc;
}

// Returns the index of the last blank space character
int find_blankSpace(char * string, int len)
{
        for(int k = len; k>0; k--){
                if(string[k] == 0x20){
                        return k;
                }
        }
}

