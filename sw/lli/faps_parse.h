#ifndef	_FAPS_PARSE_H
#define	_FAPS_PARSE_H

#include	<stdint.h>

typedef struct  {
	uint8_t len;			// Data length
	uint8_t	devid;		// Device ID
	uint8_t	msgid;		// Message ID
	char	data[255];	// Data portion
	uint8_t ckh; 			// High byte checksum
	uint8_t ckl; 			// Low byte checksum
} msg_t;

msg_t sdmsg;
msg_t rfmsg;
msg_t hlimsg;

int parse(msg_t *msg, char s[]);
#endif	/* _FAPS_PARSE_H */
