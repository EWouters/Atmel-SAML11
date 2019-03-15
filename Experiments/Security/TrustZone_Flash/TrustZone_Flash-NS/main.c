#include <atmel_start.h>
#include <stdlib.h>

#include "trustzone_veneer.h"

#define MIN_NUM_BYTES 1
#define MAX_NUM_BYTES 6496

#define DELAY delay_ms(1);
#define SLEEP

int main(void)
{
	/* Initializes MCU, drivers and middleware */

	atmel_start_init();
	
	DELAY
	
	uint8_t *input = malloc(sizeof(uint8_t) * MAX_NUM_BYTES);
	
	for (size_t num_bytes = MIN_NUM_BYTES; num_bytes <= MAX_NUM_BYTES; num_bytes++) {
		//size_t num_bytes = MAX_NUM_BYTES;
		// Fill with sequential data.
		for (size_t byte = 0; byte < num_bytes; byte++) {
			input[byte] = byte; // Will wrap at 0xff.
		}

		DELAY
		
		// Set GPIO pin high.
		gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
		// Store data in secure Flash
		nsc_store_data(input, num_bytes);
		// Set GPIO pin low.
		gpio_set_pin_level(DGI_GPIO2, GPIO_LOW);
		
		DELAY
		
		SLEEP
		
		// Overwrite the memory
		for (size_t byte = 0; byte < num_bytes; byte++) {
			input[byte] = 0xfe;
		}
			
		DELAY
		
		// Set GPIO pin high.
		gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);
		// Read from secure Flash
		nsc_load_data(input, num_bytes);
		// Set GPIO pin low.
		gpio_set_pin_level(DGI_GPIO3, GPIO_LOW);
		
		DELAY
		
		//// Check if memory has correct data
		//for (size_t byte = 0; byte < num_bytes; byte++) {
		//	if (input[byte] !=  byte % 0xff) {
		//		gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
		//	}
		//}
		
	}

	// Free the memory
	free(input);

	DELAY
	
	// Signal end of test
	gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
	gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);
}
