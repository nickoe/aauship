#include	"faps_parse.h"

/*
 * Parse packets, i.e. recieve it and put it in a struct that is accesible
 */

int parse(char s[])
{
	int i = 0;
	msg.len = s[0];
	msg.devid = s[1];
	msg.msgid = s[2];
	for (i; i < msg.len; i++) {
		msg.data[i] = s[3+i];
	msg.ckh = s[msg.len+3];
	msg.ckl = s[msg.len+4];
	}
}
