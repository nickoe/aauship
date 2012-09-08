#include <avr/io.h>
#include <util/delay.h>
 
 
int main (void)
{
  /* set PORTB for output*/
  DDRB = 0xFF;
  DDRD = 0xFF;

	PORTB = 0x00;
	PORTD = 0xff;
 
  while (1)
    {
      /* set PORTB.2 high */
      PORTB ^= 0xFF;
      PORTD ^= 0xFF;
	  	_delay_ms(100);

    }
 
  return 1;
}
