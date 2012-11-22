/** 
 *  @defgroup lli LLI
 *  @code #include <config.h> @endcode
 * 
 *  @brief Main files that creates the Low Level Interface to FAPS for AAUSHIP
 *
 *  This program is ment to be some generic software that makes it an easy to use interface
 *  that handles all default behaviour for a vesel. 
 *
 *  @author Nick Østergaard nickoe@es.aau.dk
 */


#include <avr/io.h>
#include <util/delay.h>

#include <stdlib.h>
#include <string.h>

#include <avr/interrupt.h>
#include <avr/pgmspace.h>

#include "config.h"
#include "uart.h"
#include "faps_parse.h"
#include "pwm.h"
#include "spi.h"
#include "adis16405.h"


int main (void)
{	
	/* variables for the UART0 (USB connection) */
	unsigned int c, c2, c3; // Variable for reading UARTS
	char buffer[MAX_MSG_SIZE];
	char buffer2[MAX_MSG_SIZE];
	char buffer3[MAX_MSG_SIZE];
	int  idx = 0, idx2 = -1, idx3 = 0;
	int	 len2 = 0;
	unsigned int i = 0;
	char s[64];
	char *ptr;

  /* set outputs */
	PORTL = 0xff; // Turn off LEDS
  DDRL = (1<<LED3) | (1<<LED4); // Set pins for LED as output

	pwm_init();
	spiInit();

	/* initialize UARTS */
  uart_init( UART_BAUD_SELECT(UART_BAUD_RATE,F_CPU) ); // USB connection
  uart2_init( UART_BAUD_SELECT(UART2_BAUD_RATE,F_CPU) ); // APC220 radio
  uart3_init( UART_BAUD_SELECT(UART3_BAUD_RATE,F_CPU) ); // UP-501 GPS

  /* now enable interrupt, since UART library is interrupt controlled */
  sei();


	_delay_ms(500);
	/* Set GPS to a faster baud and update UART speed */
	//uart3_puts("$PMTK251,115200*1F");
	uart3_puts("$PMTK251,57600*2C\r\n");
	//uart3_puts("$PMTK251,38400*27");
	//uart3_puts("$PMTK251,0*28");
	_delay_ms(500);
	//	uart3_init( UART_BAUD_SELECT(115200,F_CPU) );
	uart3_init( UART_BAUD_SELECT(57600,F_CPU) );
	//uart3_init( UART_BAUD_SELECT(38400,F_CPU) );
	/* 115200 seems to be a little bit unstable, at least testing via radio*/


	char date[11] = __DATE__;
	char time[8] = __TIME__;
	char buildtime[] =  __DATE__ " " __TIME__;
	buildtime[sizeof(buildtime)-1] = 0;
	memcpy(buildtime,date,sizeof(date));
	memcpy(&buildtime[sizeof(date)+1],time,sizeof(time));
	buildtime[sizeof(buildtime)] = ' ';
	uart2_putc('\n');
	uart2_puts(buildtime);


/*
	uart2_puts(date);
	uart2_putc(' ');
	uart2_puts(time);
	uart2_putc('\n');
	uart2_putc('\r');
*/





	adis_reset_factory();
	

	uint8_t str[4];

	str[0] = 0xDE;
	str[1] = 0xAD;
	str[2] = 0xBE;
	str[3] = 0xEF;
	
	ptr = (char *)package(4, 0x02, 0x03, str);
/*	for (i=0; i<2+6; i++) {
		uart2_putc(*(ptr+i));
	}*/
	//grs_send(package(4, 0x02, 0x03, str),4);


  while (1) {
		/* Read each UART serially and check each of them for data, if there is handle it */ 
/*
		c = uart_getc();
		c2 = uart2_getc();
		c3 = uart3_getc();
*/


	/*	spiTransferWord(0x3E00);
		for (i = 0;i<12;i++) { spiTransferWord(0x0000);}
*/

/*
		spiTransferWord(0x5600);
		if (spiTransferWord(0x0000) == 0x4015) {
			while(1) {
				uart2_puts("!!");
			}
		}
*/

/*
		uart2_puts(itoa(adis_get_xacc(),s,10));
		uart2_putc('\r');
		uart2_putc('\n');
*/

		_delay_ms(100);

		/* Reading from radio */
		if ( c2 & UART_NO_DATA ) {} else // Data available
		{ //if data is $, set a flag, read next byte, set that value as the length, read while incrementing index until length reached, parse

			if (idx2 == 0) { // We should buffer a packet
				len2 = c2+5; // Set length
			}

			if ( (idx2 < len2) && (idx2 >= 0)) { // We are buffering
				buffer2[idx2] = c2;
				idx2++;
				if (idx2 == len2) { // We now have a full packet

					parse(&rfmsg, buffer2);
					process(&rfmsg);
					idx2 = -1; // Set flag in new packet mode

					#ifdef DEBUG
					//puts_msg(&rfmsg);
					#endif
				}
			}

			if (c2 == '$') { // We have a possible message comming
				PORTL ^= (1<<LED4);
				idx2 = 0; // Set "flag"
			}


		}

		/* Reading from GPS */
		if ( c3 & UART_NO_DATA ) {} else  // Data available
		{
				//uart2_putc(c3);
			if (c3 == '$') { // We have a possible message comming

				PORTL ^= (1<<LED3);

		
			} 
			//uart2_puts(buffer);
			//uart2_putc('\n');
			//uart2_putc( (unsigned char)c );
		}
  }
 
  return 1;
}
