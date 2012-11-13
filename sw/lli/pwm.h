#ifndef PWM_H
#define PWM_H

/**
 * PWM outputs
 */ 
// OC3 timer
#define DC1 1 // OC3B
#define DC2 2 // OC3C
#define DC3 3 // OC3A
// OC1 timer
#define RC1 4 // OC1A
#define RC2 5 // OC1B
#define RC3 6 // OC1C
// OC4 timer
#define RC4 7 // OC4B
#define RC5 8 // OC4C

void pwm_init(void);
void pwm_set(int channel, int duty);

#endif // PWM_H 
