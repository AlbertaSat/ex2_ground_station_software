#include <stdio.h>
#include <stdlib.h>

#include "uTransceiver.h"
#include "uhf.h"

nt main(int argc, char *argv[]) {
    // Test from Josh
    uint8_t code = 0;
    UHF_return ret_val = 0;
    // uint8_t scw[12] = {0, 0b11, 0, 0b101, 0, 0, 1, 0, 0, 0, 1, 1};
    //
    // ret_val = UHF_genericWrite(code, scw);

    //Test 7a: read SCW
    uint8_t scw_ret[12] = {0};
    ret_val = HAL_UHF_getSCW(scw_ret);//Return value doesn't matter. See gnuradio terminal output

    //Test 7b: change address to 0x23
    ret_val = HAL_UHF_setI2C(0x23);
    ret_val = HAL_UHF_setI2C(0x22);//change back to 0x22

    //Test 7c: write then read U_FRAM
    UHF_framStruct fram_test;
    fram_test.addr = 0x00;
    fram_test.data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
    HAL_UHF_setFRAM(fram_test);
    UHF_framStruct fram_rx_test;
    fram_test.addr = 0x00;
    fram_test.data = {0};
    HAL_UHF_getFRAM(&fram_rx_test);//Return value doesn't matter. See gnuradio terminal output

    //Test 7d: reset device
    scw[2] = {1};//I think this is the return flag
    ret_val = HAL_UHF_setSCW(scw_ret);

    return 0;
}
