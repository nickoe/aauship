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
	unsigned int c;
	char buffer[1024];
	int  num=134;
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
  while (1)
    {

      OCR1A = 1000; //leave servo at min rotation
      _delay_ms(1000);
      OCR1A = 2000; //leave serve at max rotation
    _delay_ms(1000);




        c = uart3_getc();
        if ( c & UART_NO_DATA )
        {
          /* 
           * no data available from UART 
           */
        }
        else
        {
          /* 
           * send received character back
           */	
					if (c == '$') { // Hvorfor skal det være single quote?
			 			PORTL ^= (1<<LED3);


					} 
          uart2_putc( (unsigned char)c );

        }
    }
 
  return 1;
}
