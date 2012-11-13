#include "faps_parse.h"
#include "faps_process.h"
#include "pwm.h"

/*
 * Decide what to do with a given command
 */
int process(msg_t *msg) 
{
	switch (msg->devid) {
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
	}
}
