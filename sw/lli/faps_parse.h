#ifndef	_FAPS_PARSE_H
#define	_FAPS_PARSE_H
/** 
 *  @defgroup protocol FAPS
 *  @code #include <faps_parse.h> @endcode
 * 
 *  @brief Parse packets, i.e. recieve it and put it in a struct that is accesible
 *
 *  @author Nick Østergaard nickoe@es.aau.dk
 */

/**@{*/

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


/**
	@brief   Put buffered message into message structure
	@param   pointer of message structure, string array of buffer
	@return  none
*/
void parse(msg_t *msg, char s[]);


/**
	@brief   Send full message packet (used for binary debugging of packets)
	@param   pointer of message structure
	@return  none
*/
void puts_msg(msg_t *msg);

/**@}*/

#endif	/* _FAPS_PARSE_H */
