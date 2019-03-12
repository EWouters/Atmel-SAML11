#include <atmel_start.h>
#include <stdlib.h>

#include "trustzone_veneer.h"

#define MIN_NUM_BYTES 1
#define MAX_NUM_BYTES 8000

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	delay_ms(10);
	
	for (size_t num_bytes = MIN_NUM_BYTES; num_bytes <= MAX_NUM_BYTES; num_bytes++) {
		//size_t num_bytes = MAX_NUM_BYTES;
		uint8_t *input = malloc(sizeof(uint8_t) * num_bytes);
		// Fill with sequential data.
		for (size_t byte = 0; byte < num_bytes; byte++) {
			input[byte] = byte; // Will wrap at 0xff.
		}

		delay_ms(10);
		
		// Set GPIO pin high.
		gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
		// Store data in secure Flash
		nsc_store_data(input, num_bytes);
		// Set GPIO pin low.
		gpio_set_pin_level(DGI_GPIO2, GPIO_LOW);
		
		delay_ms(10);
		
		// Sleep here
		
		// Overwrite the memory
		for (size_t byte = 0; byte < num_bytes; byte++) {
			input[byte] = 0xfe;
		}
		// Free the memory
		free(input);
		// And reallocate
		uint8_t *output = malloc(sizeof(unsigned char) * num_bytes);
		
		delay_ms(10);
		
		// Set GPIO pin high.
		gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);
		// Read from secure Flash
		nsc_load_data(output, num_bytes);
		// Set GPIO pin low.
		gpio_set_pin_level(DGI_GPIO3, GPIO_LOW);
		
		delay_ms(10);
		
		//// Check if memory has correct data
		//for (size_t byte = 0; byte < num_bytes; byte++) {
		//	if (output[byte] !=  byte % 0xff) {
		//		gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
		//	}
		//}
		
		// Free the memory
		free(output);
	}

	delay_ms(200);
	// Signal end of test
	gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
	gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);

	/* Replace with your application code */
	//while (1) {
	//}
}
