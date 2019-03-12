#include <atmel_start.h>
#include <stdlib.h>
#include <string.h>

#include "mbedtls/aes.h"
#include "mbedtls/cmac.h"

#define MIN_AES_BLOCKS 1
#define MAX_AES_BLOCKS 100

#define DELAY delay_ms(10);
#define SLEEP

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	DELAY
	
	mbedtls_aes_context aes;
	mbedtls_aes_context aes2;
	
	uint8_t key[32] = {
		0x60, 0x3d, 0xeb, 0x10, 0x15, 0xca, 0x71, 0xbe, 0x2b, 0x73, 0xae, 0xf0, 0x85, 0x7d, 0x77, 0x81,
		0x1f, 0x35, 0x2c, 0x07, 0x3b, 0x61, 0x08, 0xd7, 0x2d, 0x98, 0x10, 0xa3, 0x09, 0x14, 0xdf, 0xf4 };
	uint8_t iv[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };
	uint8_t iv2[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };
	
	mbedtls_aes_setkey_enc( &aes, key, 256 );
	mbedtls_aes_setkey_dec( &aes2, key, 256 );
	
	for (size_t num_bytes = MIN_AES_BLOCKS * MBEDTLS_AES_BLOCK_SIZE; num_bytes <= MAX_AES_BLOCKS * MBEDTLS_AES_BLOCK_SIZE; num_bytes += MBEDTLS_AES_BLOCK_SIZE) {
	//size_t num_bytes = MAX_AES_BLOCKS * MBEDTLS_AES_BLOCK_SIZE;
		// Allocate num_bytes bytes.
		uint8_t *input = malloc(sizeof(uint8_t) * num_bytes);
		// Fill with sequential data.
		for (size_t byte = 0; byte < num_bytes; byte++) {
			input[byte] = byte; // Will wrap at 0xff.
		}

		DELAY
		
		// Set GPIO pin high.
		gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
		// Encrypt in place.
		mbedtls_aes_crypt_cbc( &aes, MBEDTLS_AES_ENCRYPT, num_bytes, iv, input, input);
		// Set GPIO pin low.
		gpio_set_pin_level(DGI_GPIO2, GPIO_LOW);
	
		DELAY
		
		SLEEP
		
		DELAY
	
		// Set GPIO pin high.
		gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);
		// Decrypt in place.
		mbedtls_aes_crypt_cbc( &aes2, MBEDTLS_AES_DECRYPT, num_bytes, iv2, input, input);
		// Set GPIO pin low.
		gpio_set_pin_level(DGI_GPIO3, GPIO_LOW);
		
		DELAY
	
		//// Check if memory has correct data
		//for (int byte = 0; byte < num_bytes; byte++) {
			//if (input[byte] != 0xff) { // byte % 0xff
				//gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
			//}
		//}
	
		// Free the memory/
		free(input);
	}

	DELAY
	
	// Signal end of test
	gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
	gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);

	/* Replace with your application code */
	//while (1) {
	//}
}