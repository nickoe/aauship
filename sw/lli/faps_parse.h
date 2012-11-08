#ifndef	_FAPS_PARSE_H
#define	_FAPS_PARSE_H

#include	<stdint.h>

struct {
	uint8_t	devid;		// Device ID
	uint8_t	msgid;	// Message ID
	char	data[255]; // Data portion
	uint8_t ckh; // High byte checksum
	uint8_t ckl; // Low byte checksum
} msg;

#endif	/* _FAPS_PARSE_H */
