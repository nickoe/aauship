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
#define LOG_ENABLE
//#define AUTO_SHUTDOWN_ENABLE

extern int awake_flag;
extern uint8_t rmc_idx;

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
#define MAX_MSG_SIZE 1024  // This should probably be 255 + len + devid + msgid + checksum
#define TX_BUFF_SIZE 350
//#define ADIS_READY 164 // 10 Hz
#define ADIS_READY 82 // 20Hz
//#define ADIS_READY 42 // 40Hz
#define TX_READY 546 // 3Hz
#define AWAKE_THRESHOLD 3

#endif // CONFIG_H 
