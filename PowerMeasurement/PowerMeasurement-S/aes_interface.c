/*
 * aes_interface.c
 *
 * Created: 05/02/2019 14:22:11
 *  Author: Erik
 */ 

#include <atmel_start.h>
//#include "driver_init.h"
//#include "stdio_start.h"

#include "mbedtls/entropy.h"
#include "mbedtls/ctr_drbg.h"
#include <string.h>

#include "aes_interface.h"

void generate_aes_key(unsigned char * key1) 
{
	mbedtls_ctr_drbg_context ctr_drbg;
	mbedtls_entropy_context entropy;
	unsigned char key[32];

	char *pers = "power measurement Ui1hu6oOCY";
	//char *pers = "aes generate key";
	int ret;
	
	mbedtls_entropy_init( &entropy );

	mbedtls_ctr_drbg_init( &ctr_drbg );

	if( ( ret = mbedtls_ctr_drbg_seed( &ctr_drbg, mbedtls_entropy_func, &entropy,
	(unsigned char *) pers, strlen( pers ) ) ) != 0 )
	{
		printf( " failed\n ! mbedtls_ctr_drbg_init returned -0x%04x\n", -ret );
		//goto exit;
		return;
	}

	if( ( ret = mbedtls_ctr_drbg_random( &ctr_drbg, key, 32 ) ) != 0 )
	{
		printf( " failed\n ! mbedtls_ctr_drbg_random returned -0x%04x\n", -ret );
		//goto exit;
		return;
	}

}

// prints string as hex
void phex(unsigned char * str, unsigned char len)
{
    for (unsigned char i = 0; i < len; ++i)
        printf("%.2x", str[i]);
    printf("\n");
}