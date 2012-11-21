/* Systems header files */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Other header files */
#include "spi.h"
#include "adis16405.h"


#define ADIS_CS 0x00 // This is just a dummy value so far


/**
 * This is a function that checks of the IMU works.
 */
void adis_self_test( void ) {
	// @TODO
}

/**
 * This decodes the 14 bit raw data from the ADIS16405 sesor
 */

int32_t adis_decode_14bit_raw(int16_t sensor, int32_t scale){
	int32_t out;

	// Makes sure that we only copy the 14-bit data we are interrested in and that
	// the new variables is 32-bit
	out = (int32_t) (0x00003fff & sensor);

	// Handle negative values
	if(out>=0x2000)
		out = 0xffffc000 | out; 

	out = out * scale;

	return out;
}

/**
 * This decodes the 12 bit raw data from the ADIS16405 sesor
 */
int32_t adis_decode_12bit_raw(uint16_t sensor, uint32_t scale){
	//uint32_t sensor = 0;
	//sensor = (uint32_t)((SENSOR_OUT[0] << 8) | SENSOR_OUT[1]) &0xfff;
	if(sensor>=0x800) 
		sensor = 0xfffff000 | sensor;
	sensor = sensor * scale;
	return sensor;
}


/*
 * This function prints the temperature to stdout.
 * The scale factor is 0.14 degrees celcius per LSB, while 0x0000 = 25
 * degrees celcius.
 * 
 * WARNING: This does not work yet
 */
float adis_get_temp( void ) {
	unsigned char tmp[2]; // Temporary variable
	uint16_t temp = 255;
	float temperature = 0;
	unsigned char c[64];


	spiTransferWord(0x1600);
	temp = spiTransferWord(0x0000);
	temperature =	(adis_decode_12bit_raw(temp,140)+25000);

	return temperature;
}

int32_t adis_get_xacc( void ) {
	unsigned char tmp[2]; // Temporary variable
	uint16_t temp = 255;
	float temperature = 0;
	unsigned char c[64];


	spiTransferWord(0x0A00);
	temp = spiTransferWord(0x0000);
	temperature =	adis_decode_14bit_raw(temp,3330);

	return temperature;
}


/**
 * Restoring sensors to factory calibration
 */
void adis_reset_factory( void ) {
	spiTransferWord(0xBE02);
}

/**
 * Testing for device number, base 10 value is the model number
 */
uint8_t is_adis16405( void ) {
	spiTransferWord(0x5600);
	if (spiTransferWord(0x0000) == 0x4015) {
		return 1; // The devide is a ADIS16405
	} else {
		return 0; // Device not connected or is not a ADIS16405
	}
}
