#include "faps_parse.h"
#include "faps_process.h"
#include "pwm.h"
#include <avr/io.h>
#include "config.h"
#include "crc16.h"

/*
 * Decide what to do with a given command
 */
int process(msg_t *msg) 
{
	char buildtime[] =  __DATE__ " " __TIME__;

	switch (msg->devid) {
		case 0:
			switch (msg->msgid) {
				case 9:
					grs_send(package(sizeof(buildtime), 0x00, 0x09, buildtime),sizeof(buildtime));
					break;
			}


		case 100: 
			pwm_set_duty(DC1, msg->data[0]);
			break;
		case 101: 
			pwm_set_duty(DC2, msg->data[0]);
			break;
		case 102: 
			pwm_set_duty(DC3, msg->data[0]);
			break;
		case 103: 
			pwm_set_duty(RC1, msg->data[0]);
			break;
		case 104: 
			pwm_set_duty(RC2, msg->data[0]);
			break;
		case 105: 
			pwm_set_duty(RC3, msg->data[0]);
			break;
		case 106: 
			pwm_set_duty(RC4, msg->data[0]);
			break;
		case 107: 
			pwm_set_duty(RC5, msg->data[0]);
			break;
		case 108: 
			PORTL ^= (1<<LED4);
			break;
	}
}

/*
 * Prepare messages
 */
char *package(uint8_t len, uint8_t devid, uint8_t msgid, uint8_t data[]) {
	uint8_t i = 0;
	uint16_t crc = 0x0000;

	pack[0] = '$';
	pack[1] = len;
	pack[2] = devid;
	pack[3] = msgid;
	for (i = 0; i < len; i++) {
		pack[i+4] = data[i];
	}
	
	crc = crc16_ccitt_calc(pack+1,len+3);
	
	pack[i+4] = (crc >> 8) & 0x00FF;
	pack[i+5] = crc & 0x00FF;

	return pack;
}

/*
 * Send to HLI
 */
void hli_send(uint8_t ptr[], uint8_t len) {
	int i;

	for (i=0; i<len+6; i++) {
		uart_putc(*(ptr+i));
	}
}

/*
 * Send to GRS
 */
void grs_send(uint8_t ptr[], uint8_t len) {
	int i;

	for (i=0; i<len+6; i++) {
		uart2_putc(*(ptr+i));
	}
}

