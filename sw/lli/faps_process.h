#ifndef	_FAPS_PROCESS_H
#define	_FAPS_PROCESS_H

#include	"faps_parse.h"

uint8_t pack[256];

char *package(uint8_t devid, uint8_t msgid, uint8_t data[250]);
#endif	/* _FAPS_PROCESS_H */
