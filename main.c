#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

#include "uTransceiver.h"
#include "uhf.h"
#include "i2c_dummy.h"


//IMPORTANT "data" must be <=128 bytes
void generic_data_for_radio(char *data, uint8_t data_len) {
    uint8_t crc_command[129] = {0};
    crc_command[0] = data_len;
    for( int i = 0; i < data_len; i++) {
        crc_command[1+i] = data[i];
    }

    uint16_t crc_res = crc16(crc_command, data_len+1);

    uint8_t radio_command[149] = {0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA,
                                  0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA}; // Gives 16 preamble bytes
    // radio_command[0] = 0xAA;
    // radio_command[1] = 0xAA;
    // radio_command[2] = 0xAA;
    // radio_command[3] = 0xAA;
    // radio_command[4] = 0xAA;
    radio_command[16] = 0x7E;
    radio_command[17] = data_len;
    for( int i = 0; i < data_len; i++) {
        radio_command[18+i] = data[i];
    }

    radio_command[18+data_len] = ((uint16_t)crc_res >> 8) & 0xFF;
    radio_command[18+data_len+1] = ((uint16_t)crc_res >> 0) & 0xFF;

    FILE *fptr = fopen("data_output.bin","w");

    int radio_len = 16+2+data_len+2;
        fwrite(radio_command, sizeof(uint8_t), radio_len, fptr);
    // for( int i = 0; i < radio_len; i++){
    //
    //   printf("%c", radio_command[i]);
    // }
    fclose(fptr);

    int status = system("cat data_output.bin | nc -w 1 127.0.0.1 1234");

}

void radioTests7(void){
  // // Test from Josh
  // uint8_t code = 0;
  // UHF_return ret_val = 0;
  // // uint8_t scw[12] = {0, 0b11, 0, 0b101, 0, 0, 1, 0, 0, 0, 1, 1};
  // //
  // // ret_val = UHF_genericWrite(code, scw);
  //
  // //Test 7a: read SCW
  // uint8_t scw_ret[12] = {0};
  // ret_val = HAL_UHF_getSCW(scw_ret);//Return value doesn't matter. See gnuradio terminal output
  //
  // //Test 7b: change address to 0x23
  // ret_val = HAL_UHF_setI2C(0x23);
  // ret_val = HAL_UHF_setI2C(0x22);//change back to 0x22
  //
  // //Test 7c: write then read U_FRAM
  // UHF_framStruct fram_test;
  // fram_test.addr = 0x00;
  // fram_test.data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
  // HAL_UHF_setFRAM(fram_test);
  // UHF_framStruct fram_rx_test;
  // fram_test.addr = 0x00;
  // fram_test.data = {0};
  // HAL_UHF_getFRAM(&fram_rx_test);//Return value doesn't matter. See gnuradio terminal output
  //
  // //Test 7d: reset device
  // scw[2] = 1;//I think this is the return flag
  // ret_val = HAL_UHF_setSCW(scw_ret);
}

void radioTests12l(){
  system("cat pipe_command_mode5.bin | nc -w 1 127.0.0.1 1234");
  unsigned int total_time_us = 60*1000*1000;
  unsigned int delay_time_us = 20000;
  unsigned int repititions = total_time_us/delay_time_us;
  uint8_t data_len = 128;
  srand(time(NULL));
  // char originaldata[data_len] = {0};
  // for(int i = 0; i < data_len; i++){
  //   originaldata[i] = (char)(60+i);
  // }
  char data[128] = {0};

  printf("Generated output data:\n");
  //Circshifting ascii sequence
  for(int i = 0; i < repititions; i++){
    for(int j = 0; j < data_len; j++){

      data[j] = (char)rand();
      if(repititions < 2){
        printf("%c", data[j]);
      }

    }
    generic_data_for_radio(data, data_len);
    usleep(delay_time_us);
  }

  // //Circshifting ascii sequence
  // for(int i = 0; i < repititions; i++){
  //   int shift_num = repititions % data_len;
  //   for(int j = 0; j < data_len; j++){
  //     if(j < ()){
  //       data[j] = ;
  //     } else {
  //       data[j] = ;
  //     }
  //     printf("&c", data[j]);
  //   }
  //   generic_data_for_radio(data, data_len)
  //   usleep(delay_time_us);
  // }
}

int main(int argc, char *argv[]) {
  radioTests12l();
  return 0;
}
