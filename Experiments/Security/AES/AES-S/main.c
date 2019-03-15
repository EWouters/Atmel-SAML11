#include <atmel_start.h>
#include <stdlib.h>
#include <string.h>

#include "mbedtls/aes.h"
#include "mbedtls/cmac.h"

#define MIN_AES_BLOCKS 1
#define MAX_AES_BLOCKS 880

#define AES_KEY_SIZE 256

#define PULSE_GPIO
#define DELAY delay_ms(1);
#define SLEEP


static mbedtls_aes_context aes;
static mbedtls_aes_context aes2;

#if(AES_KEY_SIZE == 128)
static const uint8_t key[16] = {
	0x60, 0x3d, 0xeb, 0x10, 0x15, 0xca, 0x71, 0xbe, 0x2b, 0x73, 0xae, 0xf0, 0x85, 0x7d, 0x77, 0x81 };
#elif(AES_KEY_SIZE == 256)
static const uint8_t key[32] = {
	0x60, 0x3d, 0xeb, 0x10, 0x15, 0xca, 0x71, 0xbe, 0x2b, 0x73, 0xae, 0xf0, 0x85, 0x7d, 0x77, 0x81,
	0x1f, 0x35, 0x2c, 0x07, 0x3b, 0x61, 0x08, 0xd7, 0x2d, 0x98, 0x10, 0xa3, 0x09, 0x14, 0xdf, 0xf4 };
#else
#error Only 128 and 256 are supported for AES_KEY_SIZE
#endif

static uint8_t iv[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };
static uint8_t iv2[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	#ifdef PULSE_GPIO
		DELAY
	#endif
	
	mbedtls_aes_setkey_enc( &aes, key, AES_KEY_SIZE );
	mbedtls_aes_setkey_dec( &aes2, key, AES_KEY_SIZE );
	
	// Allocate MAX_AES_BLOCKS * MBEDTLS_AES_BLOCK_SIZEbytes.
	uint8_t *input = malloc(sizeof(uint8_t) * MAX_AES_BLOCKS * MBEDTLS_AES_BLOCK_SIZE);
	
	for (size_t num_bytes = MIN_AES_BLOCKS * MBEDTLS_AES_BLOCK_SIZE; num_bytes <= MAX_AES_BLOCKS * MBEDTLS_AES_BLOCK_SIZE; num_bytes += MBEDTLS_AES_BLOCK_SIZE) {
		//num_bytes = MAX_AES_BLOCKS * MBEDTLS_AES_BLOCK_SIZE;
		// Fill with sequential data.
		for (size_t byte = 0; byte < num_bytes; byte++) {
			input[byte] = byte; // Will wrap at 0xff.
		}

		#ifdef PULSE_GPIO
			DELAY
			// Set GPIO pin high.
			gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
		#endif
		
		// Encrypt in place.
		mbedtls_aes_crypt_cbc( &aes, MBEDTLS_AES_ENCRYPT, num_bytes, iv, input, input);
		
		#ifdef PULSE_GPIO
			// Set GPIO pin low.
			gpio_set_pin_level(DGI_GPIO2, GPIO_LOW);
			DELAY
		#endif
		
		SLEEP
		

		#ifdef PULSE_GPIO
			DELAY
			// Set GPIO pin high.
			gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);
		#endif
		
		// Decrypt in place.
		mbedtls_aes_crypt_cbc( &aes2, MBEDTLS_AES_DECRYPT, num_bytes, iv2, input, input);
		
		
		#ifdef PULSE_GPIO
			// Set GPIO pin low.
			gpio_set_pin_level(DGI_GPIO3, GPIO_LOW);
			DELAY
		#endif
	
		//// Check if memory has correct data
		//for (int byte = 0; byte < num_bytes; byte++) {
			//if (input[byte] != 0xff) { // byte % 0xff
				//gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
			//}
		//}

	}

	// Free the memory
	free(input);

	#ifdef PULSE_GPIO
		DELAY
		// Signal end of test
		gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
		gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);
	#endif
}
