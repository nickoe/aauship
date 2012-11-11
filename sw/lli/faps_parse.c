#include	"faps_parse.h"

/*
 * Parse packets, i.e. recieve it and put it in a struct that is accesible
 */


/*
 * Parse packet stings and put it in structure
 */
int parse(msg_t *msg, char s[])
{
	int i;
	msg->len = s[0];
	msg->devid = s[1];
	msg->msgid = s[2];
	for (i = 0; i < msg->len; i++) {
		msg->data[i] = s[3+i];
		msg->ckh = s[msg->len+3];
		msg->ckl = s[msg->len+4];
	}

	return 0;
}
