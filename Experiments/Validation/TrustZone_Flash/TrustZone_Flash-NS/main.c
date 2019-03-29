#include <atmel_start.h>
#include <stdlib.h>

#include "trustzone_veneer.h"

#define MIN_NUM_BYTES 1
#define MAX_NUM_BYTES 6496

#define MALICIOUS_FLASH_WRITE
#define MALICIOUS_FLASH_READ

#ifndef FLASH_PAGE_SIZE
#define FLASH_PAGE_SIZE 64
#endif

#ifndef NVMCTRL_FLASH_SIZE
#define NVMCTRL_FLASH_SIZE 65536
#endif

#ifndef NVMCTRL_ROW_PAGES
#define NVMCTRL_ROW_PAGES 4
#endif

#ifndef NVMCTRL_ROW_SIZE
#define NVMCTRL_ROW_SIZE (NVMCTRL_PAGE_SIZE * NVMCTRL_ROW_PAGES)
#endif

#define SLEEP

int main(void)
{
	/* Initializes MCU, drivers and middleware */

	atmel_start_init();
	
	DELAY;
	
	uint8_t *input = malloc(sizeof(uint8_t) * MAX_NUM_BYTES);
	
	for (size_t num_bytes = MIN_NUM_BYTES; num_bytes <= MAX_NUM_BYTES; num_bytes++) {
		//size_t num_bytes = MAX_NUM_BYTES;
		// Fill with sequential data.
		for (size_t byte = 0; byte < num_bytes; byte++) {
			input[byte] = byte; // Will wrap at 0xff.
		}

		//START_MEASURE(DGI_GPIO2);
		//// Store data in secure Flash
		//nsc_store_data(input, num_bytes);
		//STOP_MEASURE(DGI_GPIO2);
		
#ifdef MALICIOUS_FLASH_WRITE
		// Malicious write to flash (Should fail!)
		uint32_t target_addr = FLASH_ADDR + FLASH_SIZE - num_bytes;
		target_addr -= target_addr % NVMCTRL_ROW_SIZE;
	
		for (uint32_t page_index = 0; page_index * FLASH_PAGE_SIZE < num_bytes; page_index += 1) {
			if (page_index % NVMCTRL_ROW_PAGES == 0) {
				/* Erase row in flash */
				FLASH_0_erase_row(target_addr + page_index * FLASH_PAGE_SIZE);
			}
			FLASH_0_write_page(target_addr + page_index * FLASH_PAGE_SIZE, &input[page_index * FLASH_PAGE_SIZE], FLASH_PAGE_SIZE);
			// TODO: decrease FLASH_PAGE_SIZE to correct number on last write if not multiple of FLASH_PAGE_SIZE.
		}
#endif
		
		SLEEP
		
		// Overwrite the memory
		for (size_t byte = 0; byte < num_bytes; byte++) {
			input[byte] = 0xfe;
		}
		
#ifdef MALICIOUS_FLASH_READ
		// Malicious read from flash (Should fail!)
#ifdef MALICIOUS_FLASH_WRITE
		target_addr = FLASH_ADDR + FLASH_SIZE - num_bytes;
#else
		uint32_t target_addr = FLASH_ADDR + FLASH_SIZE - num_bytes;
#endif
		target_addr -= target_addr % NVMCTRL_ROW_SIZE;
		FLASH_0_read(target_addr, input, num_bytes);
#endif
		
		START_MEASURE(DGI_GPIO3);
		// Read from secure Flash
		nsc_load_data(input, num_bytes);
		STOP_MEASURE(DGI_GPIO3);
		
		//// Check if memory has correct data
		//for (size_t byte = 0; byte < num_bytes; byte++) {
		//	if (input[byte] !=  byte % 0xff) {
		//		gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
		//	}
		//}
		
	}

	// Free the memory
	free(input);

	END_MEASUREMENT;
}
