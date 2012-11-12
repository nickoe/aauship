#define ADIS_STOP   0
#define ADIS_SILENT 1
#define ADIS_CSV    2
#define ADIS_BIN    3

void adis_self_test( void );
void adis_burst_read(void * pvParameters);
void adis_get_temp( void );
void adis_reset_factory( void );
void adis_recalibrate_gyros( void );
void adis_output( unsigned char );
float data_read(int data_type);
