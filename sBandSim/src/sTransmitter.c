// sTransmitter.c
// Author: Thomas Ganley
// May 13, 2020

#include "sTransmitter.h"
#include "mock_i2c.h" //*
#include "mock_spi.h" //*
#include <stdint.h>
#include <unistd.h> //*
	
//* Simulated registers so that we can "store" values
static uint8_t reg0 = 0, reg1 = 0, reg3 = 0, reg4 = 0, reg5 = 0;
static uint8_t reg17 = 0, reg18 = 0, reg19 = 1, reg20 = 0;
static uint8_t reg21 = 0, reg22 = 0, reg23 = 0, reg24 = 0;
static uint8_t reg25 = 0, reg26 = 0, reg27 = 0, reg28 = 0;
static uint8_t reg29 = 0, reg30 = 0, reg31 = 0, reg32 = 0;
static uint8_t reg33 = 0, reg34 = 0, reg35 = 0, reg36 = 0;
static uint8_t reg37 = 0, reg38 = 0, reg39 = 0, reg40 = 0, reg41 = 0;

//* Simulated buffer function for adding 
int add_vBuffer(int n_bytes)// Replace with spi_writeData eventually
{
	spi_writeData_Expect();
	spi_writeData();

	for(int j = 0; j < n_bytes; j++){ 
		
		// Time Delay
		sleep(S_DATA_TIME);

		// Overrun?
		if(reg25 == 0 && reg24 == 80){
			if(reg23 == 255){
				reg22++;
				reg23 = 0;
			}else{
				reg23++;
			}
			reg19 = 0;
			continue;
		}

		
		if(reg25 == 255){
			reg24++;
			reg25 = 0;
		}else{
			reg25++;
			uint16_t b_count = 0;
			get_S_bufferCount(&b_count);			
			if(b_count > 2560){
				reg19 = 0;
			}
		}
	}
	return 0;
}

int transmit_vBuffer(int n_bytes) // No such function will actually need to be called
{	
	for(int k = 0; k < n_bytes; k++){
		
		// Time Delay
		sleep(S_DATA_TIME);
		// Underrun?
		if(reg25 == 0 && reg24 == 0){
			if(reg21 == 255){
				reg20++;
				reg21 = 0;
			}else{
				reg21++;
			}
			reg19 = 1;
			continue;
		}
		
		if(reg25 == 0){
			reg25 = 255;
			reg24--;	
		}else{
			reg25--;
			
			uint16_t b_count = 0;
			get_S_bufferCount(&b_count);
			if(b_count <= 2560){
				reg19 = 1;
			}
		}
	}
	return 0;
}
void empty_vBuffer(void)
{
	reg25 = 0;
	reg24 = 0;
}

//* Function to read a register, called in other functions (replace with i2c_readRegister eventually)
int read_reg(uint8_t address, uint8_t * ptr)
{
	uint8_t exp = 0x0; //*
	switch (address){
        case 0: exp = reg0; break;//*
        case 1: exp = reg1; break;//*
        case 3: exp = reg3; break;//*
        case 4: exp = reg4; break;//*
        case 5: exp = reg5; break;//*
        case 17: exp = reg17; break;//*
        case 18: exp = reg18; break;//*
        case 19: exp = reg19; break;//*
        case 20: exp = reg20; break;//*
        case 21: exp = reg21; break;//*
        case 22: exp = reg22; break;//*
        case 23: exp = reg23; break;//*
        case 24: exp = reg24; break;//*
        case 25: exp = reg25; break;//*
        case 26: exp = reg26; break;//*
        case 27: exp = reg27; break;//*
        case 28: exp = reg28; break;//*
        case 29: exp = reg29; break;//*
        case 30: exp = reg30; break;//*
        case 31: exp = reg31; break;//*
        case 32: exp = reg32; break;//*
        case 33: exp = reg33; break;//*
        case 34: exp = reg34; break;//*
        case 35: exp = reg35; break;//*
        case 36: exp = reg36; break;//*
        case 37: exp = reg37; break;//*
        case 38: exp = reg38; break;//*
        case 39: exp = reg39; break;//*
        case 40: exp = reg40; break;//*
        case 41: exp = reg41; break;//*
	default: return 1;//*
	}

	i2c_readRegister_ExpectAndReturn(address, exp);//*
	*ptr = i2c_readRegister(address);
	resetTest(); //*
	return 0;
}
// Function to write to a register, called in other functions
int write_reg(uint8_t address, uint8_t val)
{
	i2c_writeRegister_Expect(address, val); //*
	i2c_writeRegister(address, val);

	switch (address){
	case 0: reg0 = val; break;//*
	case 1: reg1 = val; break;//*
	case 3: reg3 = val; break;//*
	case 4: reg4 = val; break;//*
	case 5: reg5 = val; break;//*
	case 17: reg17 = val; break;//*
	case 18: reg18 = val; break;//*
	case 19: reg19 = val; break;//*
	case 20: reg20 = val; break;//*
	case 21: reg21 = val; break;//*
	case 22: reg22 = val; break;//*
	case 23: reg23 = val; break;//*
	case 24: reg24 = val; break;//*
	case 25: reg25 = val; break;//*
	case 26: reg26 = val; break;//*
	case 27: reg27 = val; break;//*
	case 28: reg28 = val; break;//*
	case 29: reg29 = val; break;//*
	case 30: reg30 = val; break;//*
	case 31: reg31 = val; break;//*
	case 32: reg32 = val; break;//*
	case 33: reg33 = val; break;//*
	case 34: reg34 = val; break;//*
	case 35: reg35 = val; break;//*
	case 36: reg36 = val; break;//*
	case 37: reg37 = val; break;//*
	case 38: reg38 = val; break;//*
	case 39: reg39 = val; break;//*
	case 40: reg40 = val; break;//*
	case 41: reg41 = val; break;//*
	default: return 1; //*
	}
	return 0;
}
// Function to combine readings from two registers 
uint16_t append_bytes(uint8_t b1, uint8_t b2)
{
	uint16_t b = (b1 << 8) | b2;
	return b;
}

// Calculates the board temperature (called in get_topTemp & get_bottomTemp)
float b_Temp(uint8_t b1, uint8_t b2)
{
	float temperature = 0;
	uint16_t b = (b1 << 4) | (b2 >> 4);
	if (b1 & 128){
		temperature = -0.0625f*(float)((~b & 4095) + 1);
	}else{
		temperature = 0.0625f*(float)(b);
	}
	return temperature;
}


// REGISTER 0x00:
// Get the value of the control register
int get_S_control(uint8_t * ctrl)
{
	uint8_t rawValue = 0;
	if(read_reg(0x0, &rawValue)){
		return 1;	
	}else{
		*ctrl = rawValue;
		return 0;
	}
}

// Set a new control on the transmitter
int set_S_control(uint8_t new_control)
{
	if(write_reg(0x0, new_control)){
		return 1;
	}else{
		return 0;
	}
}


// REGISTER 0x01:
// Get the value of the encoder register
int get_S_encoder(uint8_t * enc)
{
	uint8_t rawValue = 0;
       	if(read_reg(0x01, &rawValue)){
		return 1;
	}else{
		*enc = rawValue;
		return 0;
	}

}

// Set a new encoder value
int set_S_encoder(uint8_t new_encoder)
{
	uint8_t control = 0;
	if(!get_S_control(&control)){
		if(control == 0){
			write_reg(0x01, new_encoder);
			return 0;
		}else{
			return 1;
		}
	
	}else{
		return 1;
	}
}

// REGISTER 0x03:
// Get the Power Amplifier power
int get_S_paPower(uint8_t * power)
{
	uint8_t rawValue = 0;
       	
	if(read_reg(0x03, &rawValue)){
		return 1;
	}else{
		switch (rawValue){
		case 0: *power = 24; break;
		case 1: *power = 26; break;
		case 2: *power = 28; break;
		case 3: *power = 30; break;
		default: return 1;
		}
		return 0;
	}
}
// Set the Power Amplifier power
int set_S_paPower(uint8_t new_paPower)
{
	uint8_t rawValue = 0;

	switch (new_paPower){
	case 24: rawValue = 0; break;
	case 26: rawValue = 1; break;
	case 28: rawValue = 2; break;
	case 30: rawValue = 3; break;
	default: return 1;
	}

	if(write_reg(0x03, rawValue)){
		return 1;
	}else{
		return 0;
	}
}


// Register 0x04:
// Get the frequency
int get_S_frequency(float * freq)
{
	uint8_t offset = 0;
	if(read_reg(0x04, &offset)){
		return 1;
	}else{
		*freq = (float)offset/2 + 2200.0f;
		return 0;
	}
}

// Set a new frequency
int set_S_frequency(float new_frequency)
{
	if(new_frequency >= 2200.0f && new_frequency <= 2300.0f){
		uint8_t offset = (uint8_t)((new_frequency - 2200.0f)*2);
		if(write_reg(0x04, offset)){
			return 1;
		}else{
			return 0; // Successful Write
		}
	}else{
		return 1;
	}
}

// REGISTER 0x05:
// Reset the FPGA logic
int softResetFPGA(void)
{
	if(write_reg(0x05, 0x0)){
		return 1;
	}else{
		return 0;
	}
}

// REGISTER 0x11:
// Get the firmware version
int get_S_firmwareVersion(float * version)
{
	uint8_t rawValue = 0;
	if(read_reg(0x11, &rawValue)){
		return 1;
	}else{
		float major = (float)(rawValue >> 4);
        	float minor = (float)(rawValue & 15);
		minor /= 100.0f;
		*version = (major+minor);
		return 0;
	}
}

// REGISTER 0x12:
// Get the status of the lock and the PA
int get_S_status(uint8_t * stat)
{
	uint8_t rawValue = 0;
	if(read_reg(0x12, &rawValue)){
		return 1;
	}else{
		*stat = rawValue;
		return 0;
	}
}

// REGISTER 0x13:
// Check if Transmit Ready
int get_S_TR(int * transmit)
{
	uint8_t rawValue = 0;
       	if(read_reg(0x13, &rawValue)){
		return 1;
	}else{
		*transmit = rawValue;
		return 0;
	}
}

// REGISTERS 0x14 & 0x15:
// Get the buffer underrun
int get_S_bufferUnderrun(uint16_t * underrun)
{
	uint8_t rawValue1 = 0;
	uint8_t rawValue2 = 0;
	if(read_reg(0x14, &rawValue1) || read_reg(0x15, &rawValue2)){
		return 1;
	}else{
		*underrun = append_bytes(rawValue1, rawValue2);
		return 0;
	}
}

// REGISTERS 0x16 & 0x17:
// Get the buffer overrun
int get_S_bufferOverrun(uint16_t * overrun)
{
        uint8_t rawValue1 = 0;
        uint8_t rawValue2 = 0;
        if(read_reg(0x16, &rawValue1) || read_reg(0x17, &rawValue2)){
                return 1;
        }else{
                *overrun = append_bytes(rawValue1, rawValue2);
                return 0;
        }
}


// REGISTERS 0x18 & 0x19:
// Get the buffer count
int get_S_bufferCount(uint16_t * count)
{
        uint8_t rawValue1 = 0;
        uint8_t rawValue2 = 0;
        if(read_reg(0x18, &rawValue1) || read_reg(0x19, &rawValue2)){
                return 1;
        }else{
                *count = append_bytes(rawValue1, rawValue2);
                return 0;
        }
}


// REGISTERS 0x1A & 0x1B:
// Get RF Power
int get_S_RFpwr(float * pwr)
{
        uint8_t rawValue1 = 0;
        uint8_t rawValue2 = 0;
        if(read_reg(0x14, &rawValue1) || read_reg(0x15, &rawValue2)){
                return 1;
        }else{
                uint16_t value = append_bytes(rawValue1, rawValue2);
                *pwr =  ((float)value*(7.0f/6144.0f));
		return 0;
	}
}

// REGISTERS 0x1C & 0x1D:
// Get PA temperature
int get_S_paTemp(float * temp)
{
	uint8_t rawValue1 = 0;
	uint8_t rawValue2 = 0;
	if(read_reg(0x1C, &rawValue1) || read_reg(0x1D, &rawValue2)){
		return 1;
	}else{
		uint16_t value = append_bytes(rawValue1, rawValue2);
		*temp = (((float)value*3.0f/4096.0f)-0.5f)*100.0f;
		return 0;
	}
}

// REGISTERS 0x1E & 0x1F:
// Get temperature of the top of the board
int get_S_topTemp(float * temp)
{
        uint8_t rawValue1 = 0;
        uint8_t rawValue2 = 0;
        if(read_reg(0x1E, &rawValue1) || read_reg(0x1F, &rawValue2)){
                return 1;
        }else{
                *temp = b_Temp(rawValue1, rawValue2);
                return 0;
        }
}

// REGISTERS 0x20 & 0x21:
// Get temperature of the bottom of the board
int get_S_bottomTemp(float * temp)
{
        uint8_t rawValue1 = 0;
        uint8_t rawValue2 = 0;
        if(read_reg(0x20, &rawValue1) || read_reg(0x21, &rawValue2)){
                return 1;
        }else{
                *temp = b_Temp(rawValue1, rawValue2);
                return 0;
        }
}
	
// REGISTERS 0x22 & 0x23:
// Get battery bus current reading
int get_S_batCurrent(float * cur)
{
	uint8_t rawValue1 = 0;
	uint8_t rawValue2 = 0;
	if(read_reg(0x22, &rawValue1) || read_reg(0x23, &rawValue2)){
		return 1;
	}else{
		uint16_t value = append_bytes(rawValue1, rawValue2);
		int16_t temp = (int16_t)value;
		*cur = (float)temp*0.00004f;
		return 0;
	}
}

// REGISTERS 0x24 & 0x25:
// Get battery bus voltage reading
int get_S_batVoltage(float * volt)
{
	uint8_t rawValue1 = 0;
	uint8_t rawValue2 = 0;
	
	if(read_reg(0x24, &rawValue1) || read_reg(0x25, &rawValue2)){
		return 1;
	}else{
		uint16_t value = append_bytes(rawValue1, rawValue2);
		value &= 8191;
		*volt = (float)value*0.004f;
		return 0;
	}
}

// REGISTERS 0x26 & 0x27:
// Get the Power Amplifier Current
int get_S_paCurrent(float * cur)
{
        uint8_t rawValue1 = 0;
        uint8_t rawValue2 = 0;
        if(read_reg(0x26, &rawValue1) || read_reg(0x27, &rawValue2)){
                return 1;
        }else{
                uint16_t value = append_bytes(rawValue1, rawValue2);
                int16_t temp = (int16_t)value;
                *cur = (float)temp*0.00004f;
                return 0;
        }
}


// REGISTERS 0x28 & 0x29:
// Get the Power Amplifier Voltage
int get_S_paVoltage(float * volt)
{
        uint8_t rawValue1 = 0;
        uint8_t rawValue2 = 0;

        if(read_reg(0x28, &rawValue1) || read_reg(0x29, &rawValue2)){
                return 1;
        }else{
                uint16_t value = append_bytes(rawValue1, rawValue2);
                value &= 8191;
                *volt = (float)value*0.004f;
                return 0;
        }
}
