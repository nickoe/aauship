#ifndef	_ADIS16405_H
#define	_ADIS16405_H

/**
 * @file
 * @defgroup adis ADIS16405
 * @code #include <adis16405.h> @endcode
 * @author Nick Østergaard nickoe@es.aau.dk
 * @author Simon Als Nielsen
 *
 * @brief This file provides functions to grab data from the IMU.
 *
 */

/**@{*/

/* Measurement functions */
#define FLASH_CNT  0x00 /* Flash memory write count */
#define SUPPLY_OUT 0x02 /* Power supply measurement */
#define XGYRO_OUT 0x04 /* X-axis gyroscope output */
#define YGYRO_OUT 0x06 /* Y-axis gyroscope output */
#define ZGYRO_OUT 0x08 /* Z-axis gyroscope output */
#define XACCL_OUT 0x0A /* X-axis accelerometer output */
#define YACCL_OUT 0x0C /* Y-axis accelerometer output */
#define ZACCL_OUT 0x0E /* Z-axis accelerometer output */
#define XMAGN_OUT 0x10 /* X-axis magnetometer measurement */
#define YMAGN_OUT 0x12 /* Y-axis magnetometer measurement */
#define ZMAGN_OUT 0x14 /* Z-axis magnetometer measurement */
#define TEMP_OUT  0x16 /* Temperature output */
#define AUX_ADC   0x18 /* Auxiliary ADC measurement */

/* Calibration parameters */
#define XGYRO_OFF 0x1A /* X-axis gyroscope bias offset factor */
#define YGYRO_OFF 0x1C /* Y-axis gyroscope bias offset factor */
#define ZGYRO_OFF 0x1E /* Z-axis gyroscope bias offset factor */
#define XACCL_OFF 0x20 /* X-axis acceleration bias offset factor */
#define YACCL_OFF 0x22 /* Y-axis acceleration bias offset factor */
#define ZACCL_OFF 0x24 /* Z-axis acceleration bias offset factor */
#define XMAGN_HIF 0x26 /* X-axis magnetometer, hard-iron factor */
#define YMAGN_HIF 0x28 /* Y-axis magnetometer, hard-iron factor */
#define ZMAGN_HIF 0x2A /* Z-axis magnetometer, hard-iron factor */
#define XMAGN_SIF 0x2C /* X-axis magnetometer, soft-iron factor */
#define YMAGN_SIF 0x2E /* Y-axis magnetometer, soft-iron factor */
#define ZMAGN_SIF 0x30 /* Z-axis magnetometer, soft-iron factor */

#define GPIO_CTRL 0x32 /* Auxiliary digital input/output control */
#define MSC_CTRL  0x34 /* Miscellaneous control */
#define SMPL_PRD  0x36 /* Internal sample period (rate) control */
#define SENS_AVG  0x38 /* Dynamic range and digital filter control */
#define SLP_CNT   0x3A /* Sleep mode control */
#define DIAG_STAT 0x3C /* System status */

/* Alarm functions */
#define GLOB_CMD  0x3E /* System command */
#define ALM_MAG1  0x40 /* Alarm 1 amplitude threshold */
#define ALM_MAG2  0x42 /* Alarm 2 amplitude threshold */
#define ALM_SMPL1 0x44 /* Alarm 1 sample size */
#define ALM_SMPL2 0x46 /* Alarm 2 sample size */
#define ALM_CTRL  0x48 /* Alarm control */
#define AUX_DAC   0x4A /* Auxiliary DAC data */

#define PRODUCT_ID 0x56 /* Product identifier */

/* Stuff for output handeling, this is deprecated */
#define ADIS_STOP   0
#define ADIS_SILENT 1
#define ADIS_CSV    2
#define ADIS_BIN    3

/* Function prototypes */
void adis_self_test( void );
void adis_burst_read(void * pvParameters);
void adis_get_temp( void );
void adis_reset_factory( void );
void adis_recalibrate_gyros( void );
void adis_output( unsigned char );
float data_read(int data_type);

/**@}*/

#endif	/* _ADIS16405_H */
