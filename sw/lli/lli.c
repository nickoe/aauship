#include <avr/io.h>
#include <util/delay.h>

#include <stdlib.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>

#include "uart.h"

#define LED1 PL0
#define LED2 PL1
#define LED3 PL2
#define LED4 PL3

//#define UART_BAUD_RATE      9600
#define UART_BAUD_RATE      38400
#define UART2_BAUD_RATE      38400
#define UART3_BAUD_RATE      9600

int main (void)
{
	/* variables for the UART0 (USB connection) */
	unsigned int c;
	char buffer[7];
	int  num=134;
	unsigned int i = 0;

  /* set outputs */
  DDRB = (1<<PB5) | (1<<PB7);
	PORTL = 0xff; // Turn off LEDS
  DDRL = (1<<LED3) | (1<<LED4); // Set pins for LED as output


	/* initialize UARTS */
  uart_init( UART_BAUD_SELECT(UART_BAUD_RATE,F_CPU) ); 
  uart2_init( UART_BAUD_SELECT(UART2_BAUD_RATE,F_CPU) ); // APC220 radio
  uart3_init( UART_BAUD_SELECT(UART3_BAUD_RATE,F_CPU) ); // UP-501 GPS
  /*
   * now enable interrupt, since UART library is interrupt controlled
   */
  sei();
     uart_puts("String stored in SRAM\n");
     uart2_puts("Printing via radio\n");
     uart3_puts("Printing to GPS\n");
  while (1)
    {
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
						if (c |= '\n') {
							i = i +1;
						}
					} 

            /*
             * new data available from UART
             * check for Frame or Overrun error
             */
            if ( c & UART_FRAME_ERROR )
            {
                /* Framing Error detected, i.e no stop bit detected */
                uart2_puts_P("UART Frame Error: ");
            }
            if ( c & UART_OVERRUN_ERROR )
            {
                /* 
                 * Overrun, a character already present in the UART UDR register was 
                 * not read by the interrupt handler before the next character arrived,
                 * one or more received characters have been dropped
                 */
                uart2_puts_P("UART Overrun Error: ");
            }
            if ( c & UART_BUFFER_OVERFLOW )
            {
                /* 
                 * We are not reading the receive buffer fast enough,
                 * one or more received character have been dropped 
                 */
                uart2_puts_P("Buffer overflow error: ");
            }

          uart2_putc( (unsigned char)c );

          //uart2_putc( (unsigned char)c );

        }
    }
 
  return 1;
}
