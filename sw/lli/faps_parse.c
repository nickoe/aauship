#include	"faps_parse.h"


void parse(msg_t *msg, char s[])
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
}

void puts_msg(msg_t *msg)
{
	uart2_putc(rfmsg.len);
	uart2_putc(rfmsg.devid);
	uart2_putc(rfmsg.msgid);
	uart2_puts(rfmsg.data);
	uart2_putc(rfmsg.ckh);
	uart2_putc(rfmsg.ckl);
}


