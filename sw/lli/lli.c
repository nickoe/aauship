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

int main (void)
{
	/* variables for the UART0 (USB connection) */
	unsigned int c;
	char buffer[7];
	int  num=134;

  /* set outputs */
  DDRB = (1<<PB5);
  DDRB = (1<<PB7);
  DDRL = (1<<LED3);

	/* initialize UARTS */
  uart_init( UART_BAUD_SELECT(UART_BAUD_RATE,F_CPU) ); 
  uart2_init( UART_BAUD_SELECT(UART_BAUD_RATE,F_CPU) ); // APC220 radio
  /*
   * now enable interrupt, since UART library is interrupt controlled
   */
  sei();
     uart_puts("String stored in SRAM\n");
     uart2_puts("Printing via radio\n");
  while (1)
    {
      /* flip PORTB.2 */
      PORTB ^= (1<<PB5);
      PORTB ^= (1<<PB7);
 			PORTL ^= (1<<LED3);
	  	_delay_ms(100);
    }
 
  return 1;
}
