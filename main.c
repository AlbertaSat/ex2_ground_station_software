#include <stdio.h>
#include <stdlib.h>

#include "uTransceiver.h"

// int main(int argc, char *argv[]) {
//     // For example, sending command 1 with frequency parameter.
//     uint8_t code = 1;
//     uint32_t freq = 437875000;

//     UHF_return ret_val = UHF_genericWrite(code, &freq);
//     return 0;
// }

int main(int argc, char *argv[]) {
    // Test from Josh
    uint8_t code = 0;
    uint8_t scw[12] = {0, 0b11, 0, 0b101, 0, 0, 1, 0, 0, 0, 1, 1};

    UHF_return ret_val = UHF_genericWrite(code, scw);
    return 0;
}