#include <atmel_start.h>

//#include "serial_interface.h"
#include "aes_interface.h"

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	/* Replace with your application code */
	test_aes();
	
	//char command[CMD_MAX_LEN + 1];
	//while (1) {
		//delay_ms(1000);
		//printf("looping");
		////serial_command(command);
	//}
}

//int main(void)
//{
	///* Initializes MCU, drivers and middleware */
	//atmel_start_init();
	//
	//mbedtls_aes_context aes;
	//mbedtls_aes_context aes2;
//
	//unsigned char key[16] = "itzkbgulrcsjmnv";
	//key[15] = 'x';
//
	//unsigned char iv[16] = {0xb2, 0x4b, 0xf2, 0xf7, 0x7a, 0xc5, 0xec, 0x0c, 0x5e, 0x1f, 0x4d, 0xc1, 0xae, 0x46, 0x5e, 0x75};
//
	//const unsigned char *input = (const unsigned char*) "Some string to b";
	//unsigned char output[128] = {0};
	//unsigned char output2[128] = {0};
//
	//mbedtls_aes_setkey_enc( &aes, key, 16*8 );
	//mbedtls_aes_crypt_cbc( &aes, MBEDTLS_AES_ENCRYPT, strlen((const char*)input), iv, input, output );
//
	//mbedtls_aes_setkey_dec( &aes2, key, 16*8 );
	//mbedtls_aes_crypt_cbc( &aes2, MBEDTLS_AES_DECRYPT, strlen((const char*)output), iv, output, output2 );
	//
	//
	//printf("output:\t");
	//phex(output, 128);
	//printf("output:\t");
	//phex(output2, 128);
//}
