#ifndef CONFIG_H
#define CONFIG_H
/**
 * @file
 * @author Nick Østergaard
 *
 * @section DESCRIPTION
 * This is the configuration file for the LLI interface for AAUSHIP1
 */

#define DEBUG 

/**
 * Serial rates
 */
// USB connection
#define UART_BAUD_RATE   115200
// APC220 radio
#define UART2_BAUD_RATE   38400
// UP-501 GPS
#define UART3_BAUD_RATE    9600


/**
 * Blinkenlights
 */
#define LED1 PL0
#define LED2 PL1
#define LED3 PL2
#define LED4 PL3


/**
 * PWM outputs
 */ 
// OC3 timer
#define DCPWM1 PE4 // OC3B
#define DCPWM2 PE5 // OC3C
#define DCPWM3 PE3 // OC3A
// OC1 timer
#define RCPWM1 PB5 // OC1A
#define RCPWM2 PB6 // OC1B
#define RCPWM3 PB7 // OC1C
// OC4 timer
#define RCPWM4 PH4 // OC4B
#define RCPWM5 PH5 // OC4C

/**
 * Message related stuff
 */
#define MAX_MSG_SIZE 10

#endif // CONFIG_H 
