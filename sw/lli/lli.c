#include <avr/io.h>
#include <util/delay.h>

#include <stdlib.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>

#include "uart.h"
#include "config.h"

int main (void)
{
	/* variables for the UART0 (USB connection) */
	unsigned int c, c2, c3; // Variable for reading UARTS
	char buffer[MAX_MSG_SIZE];
	char buffer2[MAX_MSG_SIZE];
	char buffer3[MAX_MSG_SIZE];
	int  idx=0;
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
     uart2_puts("Printing via radio\n");
     uart3_puts("Printing to GPS\n");
	pwm_init();

  while (1) {
		/* Read each UART serially and check each of them for data, if there is handle it */ 
		c = uart_getc();
		c2 = uart2_getc();
		c3 = uart3_getc();

		if ( (c2 & UART_NO_DATA) ) {} else // Data available
		{
			/* 
			 * send received character back
			 */	
			uart2_putc(c2);
//			uart2_putc((char) (c2 & 0x00ff));// echo
			if (c2 == '6') { // We have a possible message comming
				PORTL ^= (1<<LED4);
				uart2_putc('r');
			}
		}


		if ( 1 != (c3 & UART_NO_DATA) ) // Data available
		{

			if (c3 == ',') { // We have a possible message commingq	

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
