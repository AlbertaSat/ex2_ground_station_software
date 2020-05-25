#include "build/temp/_test_sTransmitter.c"
#include "build/test/mocks/mock_spi.h"
#include "build/test/mocks/mock_i2c.h"
#include "src/sTransmitter.h"
#include "/var/lib/gems/2.7.0/gems/ceedling-0.30.0/vendor/unity/src/unity.h"














void setUp(void)

{

}



void tearDown(void)

{

}



void test_setControl130_getControl130(void)

{

 uint8_t new_control = 130;

 set_S_control(new_control);



 uint8_t control = 0;

 get_S_control(&control);



 UnityAssertEqualNumber((UNITY_INT)(UNITY_UINT8 )((new_control)), (UNITY_INT)(UNITY_UINT8 )((control)), (

((void *)0)

), (UNITY_UINT)(28), UNITY_DISPLAY_STYLE_UINT8);

 resetTest();

}



void test_setEncoder4_getEncoder4(void)

{

 uint8_t new_encoder = 4;

 set_S_control(0);

 set_S_encoder(new_encoder);



 uint8_t encoder = 0;

        get_S_encoder(&encoder);



 UnityAssertEqualNumber((UNITY_INT)(UNITY_UINT8 )((new_encoder)), (UNITY_INT)(UNITY_UINT8 )((encoder)), (

((void *)0)

), (UNITY_UINT)(41), UNITY_DISPLAY_STYLE_UINT8);

}



void test_setPAPower26_getPAPower26(void)

{

 uint8_t new_paPower = 26;

 set_S_paPower(new_paPower);



 uint8_t power = 0;

 get_S_paPower(&power);



 UnityAssertEqualNumber((UNITY_INT)(UNITY_UINT8 )((new_paPower)), (UNITY_INT)(UNITY_UINT8 )((power)), (

((void *)0)

), (UNITY_UINT)(52), UNITY_DISPLAY_STYLE_UINT8);

}



void test_setFrequency_getFrequency(void)

{

 float new_frequency = 2225.5f;

 set_S_frequency(new_frequency);



 float frequency = 0;

 get_S_frequency(&frequency);



 UnityAssertFloatsWithin((UNITY_FLOAT)((0.1)), (UNITY_FLOAT)((new_frequency)), (UNITY_FLOAT)((frequency)), (

((void *)0)

), (UNITY_UINT)(63));

}



void test_PAtemp(void)

{

 float exp_temp = -50;

 float temperature = 0;

 get_S_paTemp(&temperature);

 UnityAssertFloatsWithin((UNITY_FLOAT)((0.1)), (UNITY_FLOAT)((exp_temp)), (UNITY_FLOAT)((temperature)), (

((void *)0)

), (UNITY_UINT)(71));

}

void test_putAmountBytesInBuffer(void)

{

 int amount = 10000;

 add_vBuffer(amount);

 uint16_t count = 0;

 get_S_bufferCount(&count);

 UnityAssertEqualNumber((UNITY_INT)(UNITY_UINT16)((amount)), (UNITY_INT)(UNITY_UINT16)((count)), (

((void *)0)

), (UNITY_UINT)(79), UNITY_DISPLAY_STYLE_UINT16);

}

void test_sendAmountBytesInBuffer(void)

{

 int amount = 10000;

 set_S_control(130);

 transmit_vBuffer(amount);

 uint16_t count = 0;

 get_S_bufferCount(&count);

 UnityAssertEqualNumber((UNITY_INT)(UNITY_UINT16)((0)), (UNITY_INT)(UNITY_UINT16)((count)), (

((void *)0)

), (UNITY_UINT)(88), UNITY_DISPLAY_STYLE_UINT16);

}



void test_bufferOverrun(void)

{

 empty_vBuffer();

 int amount = 20481;

 add_vBuffer(amount);

 uint16_t overrun = 0;

 get_S_bufferOverrun(&overrun);



 UnityAssertEqualNumber((UNITY_INT)(UNITY_UINT16)((1)), (UNITY_INT)(UNITY_UINT16)((overrun)), (

((void *)0)

), (UNITY_UINT)(99), UNITY_DISPLAY_STYLE_UINT16);

}

void test_bufferUnderrun()

{

 empty_vBuffer();

 int amount = 1;

 transmit_vBuffer(amount);

 uint16_t underrun = 0;

 get_S_bufferUnderrun(&underrun);



 UnityAssertEqualNumber((UNITY_INT)(UNITY_UINT16)((1)), (UNITY_INT)(UNITY_UINT16)((underrun)), (

((void *)0)

), (UNITY_UINT)(109), UNITY_DISPLAY_STYLE_UINT16);

}
