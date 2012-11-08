#include <avr/io.h>
#include <util/delay.h>

#include <stdlib.h>

#include <avr/interrupt.h>
#include <avr/pgmspace.h>

#include "config.h"
#include "uart.h"
#include "faps_parse.h"


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


  /* set outputs */
	PORTL = 0xff; // Turn off LEDS
  DDRL = (1<<LED3) | (1<<LED4); // Set pins for LED as output




	/* initialize UARTS */
  uart_init( UART_BAUD_SELECT(UART_BAUD_RATE,F_CPU) ); // USB connection
  uart2_init( UART_BAUD_SELECT(UART2_BAUD_RATE,F_CPU) ); // APC220 radio
  uart3_init( UART_BAUD_SELECT(UART3_BAUD_RATE,F_CPU) ); // UP-501 GPS
  /*
   * now enable interrupt, since UART library is interrupt controlled
   */
  sei();

	uart_puts("String stored in SRAM\n");
	uart2_puts(__DATE__);
	uart2_putc(' ');
	uart2_puts(__TIME__);
	uart2_putc('\n');
	uart2_putc('\r');
	uart3_puts("Printing to GPS\n");
	pwm_init();

  while (1) {
		/* Read each UART serially and check each of them for data, if there is handle it */ 
		c = uart_getc();
		c2 = uart2_getc();
		c3 = uart3_getc();

		/* Reading from radio */
		if ( c2 & UART_NO_DATA ) {} else // Data available
		{ //if data is $, set a flag, read next byte, set that value as the length, read while incrementing index until length reached, parse

			if (idx2 == 0) { // We should buffer a packet
				len2 = c2; // Set length
			}

			if ( (idx2 < len2) && (idx2 >= 0)) { // We are buffering
				buffer2[idx2] = c2;
				idx2++;
				if (idx2 == len2) { // We now have a full packet
					parse(buffer2);
					idx2 = -1; // Set flag in new packet mode
				
					#ifdef DEBUG
					uart2_putc(msg.len);
					uart2_putc(msg.devid);
					uart2_putc(msg.msgid);
					uart2_puts(msg.data);
					uart2_putc(msg.ckh);
					uart2_putc(msg.ckl);
					uart2_putc('\n');
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

			if (c3 == '$') { // We have a possible message comming

				PORTL ^= (1<<LED3);
					//uart2_putc('k');
		
			} 
			//uart2_puts(buffer);
			//uart2_putc('\n');
			//uart2_putc( (unsigned char)c );
		}
  }
 
  return 1;
}
