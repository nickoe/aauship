/** 
 *  @defgroup lli LLI
 *  @code #include <config.h> @endcode
 * 
 *  @brief Main files that creates the Low Level Interface to FAPS for AAUSHIP
 *
 *  This program is ment to be some generic software that makes it an easy to use interface
 *  that handles all default behaviour for a vesel. 
 *
 *  @author Nick Østergaard nickoe@es.aau.dk
 */


#include <avr/io.h>
#include <util/delay.h>

#include <stdlib.h>
#include <string.h>

#include <avr/interrupt.h>
#include <avr/pgmspace.h>

#include "config.h"
#include "uart.h"
#include "faps_parse.h"

#include "pwm.h"
#include "spi.h"
#include "adis16405.h"


volatile int adis_ready_counter=0;
volatile int tx_counter = 0;
int awake_flag = 0;
uint8_t rmc_idx = 0;


ISR(PCINT2_vect) {
	adis_ready_counter++;
	tx_counter++;
}

int main (void)
{	
	/* variables for the UART0 (USB connection) */
	unsigned int c = 0, c2 = 0, c3 = 0; // Variable for reading UARTS
	char buffer[MAX_MSG_SIZE];
	char buffer2[MAX_MSG_SIZE];
	char buffer3[MAX_MSG_SIZE];
	int  idx = 0, idx2 = -1, idx3 = -1;
	int	 len2 = 0;
	int	 len3 = 0;
	char meas_buffer[TX_BUFF_SIZE];
	int txi = 0;
	int txtop=0;
	unsigned int i = 0;
	char *ptr;
	unsigned char hli_mutex = 0;
	unsigned int gps = 0;
	unsigned int imu = 0;
	signed int ratio = 0;
	uint16_t xacc = 0;
	uint8_t xacca[2];
	char s[64];
	char rmc[256];
awake_flag = 0;


  /* set outputs */
	PORTL = 0xff; // Turn off LEDS
  DDRL = (1<<LED1) | (1<<LED2) | (1<<LED3) | (1<<LED4); // Set pins for LED as output

	pwm_init();
	spiInit();

	/* initialize UARTS */
  uart_init( UART_BAUD_SELECT(UART_BAUD_RATE,F_CPU) ); // USB connection
  uart2_init( UART_BAUD_SELECT(UART2_BAUD_RATE,F_CPU) ); // APC220 radio
  uart3_init( UART_BAUD_SELECT(UART3_BAUD_RATE,F_CPU) ); // UP-501 GPS

	/* Interrupt stuff for ADIS */
	PCICR |= 1<<PCIE2; // Enable interrupt PORTK
	PCMSK2 |= (1<<PCINT23); // interrupt in PCINT23

  /* now enable interrupt, since UART library is interrupt controlled */
  sei();

	spiTransferWord(0xBE80); // ADSI software reset
	_delay_ms(500);
	/* Set GPS to a faster baud and update UART speed */
	//uart3_puts("$PMTK251,115200*1F");
	uart3_puts("$PMTK251,57600*2C\r\n");
	//uart3_puts("$PMTK251,38400*27");
	//uart3_puts("$PMTK251,0*28");
	_delay_ms(500);
	//	uart3_init( UART_BAUD_SELECT(115200,F_CPU) );
	uart3_init( UART_BAUD_SELECT(57600,F_CPU) );
	//uart3_init( UART_BAUD_SELECT(38400,F_CPU) );
	/* 115200 seems to be a little bit unstable, at least testing via radio*/

	adis_reset_factory();
	adis_set_sample_rate();

  while (1) {
		/* Read each UART serially and check each of them for data, if there is handle it */ 	
		c = uart_getc();
		c2 = uart2_getc();
		c3 = uart3_getc();

		// Stop motors when connection is lost
		if (awake_flag > AWAKE_THRESHOLD) {
			pwm_set_duty(RC1, 0 );
			pwm_set_duty(RC2, 0 );
		};

		if(tx_counter >= TX_READY) {
			//empty buffer
			for (txi = 0; txi < txtop; txi++) {
				uart2_putc(meas_buffer[txi]); // Sending buffered data to RF
			}
			txtop = 0;
			#ifdef AUTO_SHUTDOWN_ENABLE
			awake_flag++;
			#endif
			PORTL ^= (1<<LED2);
			tx_counter -= TX_READY;
		}


		if (adis_ready_counter >= ADIS_READY) {
			adis_decode_burst_read_pack(&adis_data_decoded);
			adis_reduce_decoded_burst(); // Reduce data ammount
			#ifdef LOG_ENABLE
			hli_send(package(sizeof(adis8_t), 0x14, 0x0D, &adis_data_decoded), sizeof(adis8_t)); // Log to SD card
			#endif

			memcpy(&meas_buffer[txtop],	(char *)package(sizeof(adis8_reduced_t), 0x14, 0x0E, &adis_data_decoded_reduced),sizeof(adis8_reduced_t)+6);
			txtop=txtop+sizeof(adis8_reduced_t)+6;

			adis_ready_counter -= ADIS_READY;

			PORTL ^= (1<<LED4);
		}


		/* Reading from radio */
		if ( c2 & UART_NO_DATA ) {} else // Data available
		{ //if data is $, set a flag, read next byte, set that value as the length, read while incrementing index until length reached, parse
//uart_putc(c2);
			if (idx2 == 0) { // We should buffer a packet
				len2 = c2+5; // Set length
			}

			if ( (idx2 < len2) && (idx2 >= 0)) { // We are buffering
				buffer2[idx2] = c2;
				idx2++;

				if (idx2 == len2) { // We now have a full packet

					if (parse(&rfmsg, buffer2)) {
						PORTL ^= (1<<LED1);
						process(&rfmsg);
					}

					idx2 = -1; // Set flag in new packet mode

					#ifdef DEBUG
					//puts_msg(&rfmsg);
					#endif
				}
			}

			if (c2 == '$') { // We have a possible message comming
//				PORTL ^= (1<<LED4);
				idx2 = 0; // Set "flag"
			}
		}

		/* Reading from GPS */
		if ( c3 & UART_NO_DATA ) {} else  // Data available
		{
			/* Transmitting NMEA GPS sentences to the HLI */
			if (c3 == '$') { // We have a possible message comming
				//PORTL ^= (1<<LED3);
				len3 = 0; // Set "flag"
			}

			if (len3 >= 0) { // We are buffering
				buffer3[len3] = c3;
				len3++;
				if (c3 == '\n') { // We now have a full packet
					if(buffer3[4] != 'S') { // Disable GSV and GSA messages
						#ifdef LOG_ENABLE
						hli_send(package(len3, 0x1E, 0x06, buffer3), len3); // Log to SD card
						#endif
						if (rmc_cut(buffer3,rmc)) {
							// Invalid RMC data
						} else {
							memcpy(&meas_buffer[txtop],	(char *)package(rmc_idx, 30, 6, rmc),rmc_idx+6);
							txtop=txtop+rmc_idx+6;

							PORTL ^= (1<<LED3);
						}

						len3 = -1; // Set flag in new packet mode
					}
				}
			}
		}
  }

  return 1;
}
