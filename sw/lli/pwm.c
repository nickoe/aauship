/**
 * @file
 * @author Nick Østergaard
 *
 * @section DESCRIPTION
 * This file handles the raw motor and servo control for the
 * outputs.
 *
 */

#include <avr/io.h>
#include "config.h"

/*


f_OCnA = fclk_IO/(2*N*(1+OCRnA)
*/
// Initialiser PWM, specifikt for vores bil
void pwm_init(void) {
	// Enable all PWM pins as outputs
	DDRE = (1<<DCPWM1) | (1<<DCPWM2) | (1<<DCPWM3);
	DDRB = (1<<RCPWM1) | (1<<RCPWM2) | (1<<RCPWM3);
	DDRH = (1<<RCPWM4) | (1<<RCPWM5);


// DCPWM1
  OCR3B = 1000; //set 1ms pulse  1000=1ms  2000=2ms
  TCCR3A |= (1<<COM3B1);//COM1A1 Clear OCnA when match counting up,Set on 

// DCPWM2
  OCR3C = 1000; //set 1ms pulse  1000=1ms  2000=2ms
  TCCR3A |= (1<<COM3C1);//COM1A1 Clear OCnA when match counting up,Set on 

// DCPWM3
  OCR3A=1000; //set 1ms pulse  1000=1ms  2000=2ms
  TCCR3A |= (1<<COM3A1);//COM1A1 Clear OCnA when match counting up,Set on 

  TCCR3B |= (1<<WGM33) | (1<<CS31);// Phase and Freq correct ICR1=Top   //Mode 8: Phase and Freq. Correct PWM top=ICR1
  ICR3=20000; // Period time



// RCPWM1
  OCR1A=5000; //set 1ms pulse  1000=1ms  2000=2ms
  TCCR1A |= (1<<COM1A1);//COM1A1 Clear OCnA when match counting up,Set on 

// RCPWM2
  OCR1B=5000; //set 1ms pulse  1000=1ms  2000=2ms
  TCCR1A |= (1<<COM1B1);//COM1A1 Clear OCnA when match counting up,Set on 

// RCPWM3
  OCR1C=5000; //set 1ms pulse  1000=1ms  2000=2ms
  TCCR1A |= (1<<COM1C1);//COM1A1 Clear OCnA when match counting up,Set on 

  TCCR1B |= (1<<WGM13) | (1<<CS11);// Phase and Freq correct ICR1=Top
  ICR1=20000; // Period time



// RCPWM4
  OCR4B=10000; //set 1ms pulse  1000=1ms  2000=2ms
  TCCR4A |= (1<<COM4B1);//COM1A1 Clear OCnA when match counting up,Set on 

// RCPWM5
  OCR4C=10000; //set 1ms pulse  1000=1ms  2000=2ms
  TCCR4A |= (1<<COM4C1);//COM1A1 Clear OCnA when match counting up,Set on 

  TCCR4B |= (1<<WGM43) | (1<<CS41);// Phase and Freq correct ICR1=Top
  ICR4=20000; // Period time
}

void pwm_set(int channel, int value) {
// @TODO implement this as a switch case

// @TODO make a nice illustration that illustrates sub-d connector connections and board to board connector
}
