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

int set_U_control(uint8_t * array)
{
        uint8_t hex[4] = {0};

        // Grouping params into 4 bits (hex values)
        hex[0] = (array[0] << 2) | (array[1]);
        hex[1] = (array[2] << 3) | (array[3]);
        hex[2] = (array[4] << 3) | (array[5] << 2) | (array[6] << 1) | (array[7]);
        hex[3] = (array[8] << 3) | (array[9] << 2) | (array[10] << 1) | (array[11]);

        convHexToASCII(4, hex);

        uint8_t command[22] = {'E','S','+','W','2','2','0','0', hex[0], hex[1], hex[2], hex[3], ' ', 'C','C','C','C','C','C','C','C','\r'};
        printf("%s", command);
}


