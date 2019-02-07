/*
 * checkpointing.c
 *
 * Created: 2019-02-06 16:14:03
 *  Author: erikw_000
 */ 

#include "checkpointing.h"
#include <atmel_start.h>
#include "aes_interface.h"

#ifndef NVMCTRL_ROW_SIZE
#define NVMCTRL_ROW_SIZE (NVMCTRL_PAGE_SIZE * NVMCTRL_ROW_PAGES)
#endif

#define FLASH_OFFSET 0x2000
//static uint8_t flash_src_data[FLASH_PAGE_SIZE];
//static uint8_t flash_chk_data[FLASH_PAGE_SIZE];

int mem2flash(const uint8_t *buffer, const uint16_t length)
{
	int32_t rc = ERR_NONE;

#ifdef CHECK_LENGTH_IS_PAGE_SIZE
	if (length % NVMCTRL_ROW_SIZE != 0) {
		return ERR_WRONG_LENGTH;
	}
#endif  /* CHECK_LENGTH_IS_PAGE_SIZE */
	
	/* Target address.
	 * Make sure the address is reasonable to your application.
	 * It might a address in NVM memory of FLASH, DATAFLASH, AUX FLASH.
	 */
	//uint32_t target_addr = FLASH_ADDR + FLASH_SIZE - NVMCTRL_ROW_SIZE;
	
	uint16_t written = 0;
	
	while (written <= length)
	{
		if (written % NVMCTRL_ROW_SIZE == 0) {
			/* Erase row in flash */
			rc = FLASH_0_erase_row(FLASH_ADDR + FLASH_OFFSET + written);
			if (rc != ERR_NONE) {
				return rc;
			}
		}

		/* Write data to flash */
		rc = FLASH_0_write_page(FLASH_ADDR + FLASH_OFFSET + written, buffer + written, FLASH_PAGE_SIZE);
		if (rc != ERR_NONE) {
			return rc;
		}
		written += FLASH_PAGE_SIZE;
	}
	
	/* Erase row in flash */
	//rc = FLASH_0_erase_row(FLASH_ADDR);
	//if (rc != ERR_NONE) {
		//return rc;
	//}
	
	/* Write data to flash */
	//rc = FLASH_0_write_page(FLASH_ADDR + FLASH_OFFSET, buffer, FLASH_PAGE_SIZE);
	
	return rc;
}

int flash2mem(uint8_t *buffer, uint32_t length)
{
	int32_t rc = ERR_NONE;
	
#ifdef CHECK_LENGTH_IS_PAGE_SIZE
	if (length % NVMCTRL_ROW_SIZE != 0) {
		return ERR_WRONG_LENGTH;
	}
#endif  /* CHECK_LENGTH_IS_PAGE_SIZE */
	
	//uint32_t read = 0;
	//
	//while (read <= length)
	//{
		///* Read data from flash */
		//rc = FLASH_0_read(FLASH_ADDR + FLASH_OFFSET, buffer + read, FLASH_PAGE_SIZE);
		//if (rc != ERR_NONE) {
			//return rc;
		//}
		//read += FLASH_PAGE_SIZE;
	//}
	
	rc = FLASH_0_read(FLASH_ADDR + FLASH_OFFSET, buffer, length);
	
	/* Check data */
	//for (i = 0; i < FLASH_PAGE_SIZE; i++) {
		//if (flash_src_data[i] != flash_chk_data[i]) {
			//while (1)
			//; /* Error happen */
		//}
	//}
	
	return rc;
}

int test_write_flash(int num_bytes)
{
	int32_t rc = ERR_NONE;
	
	uint32_t i;
	
	printf("Performing flash read write test with %d bytes\n", num_bytes);
	
	uint32_t length = num_bytes * sizeof(uint8_t);
	
	uint8_t flash_src_data[length];
	
	printf("Is %d bytes\n", sizeof(flash_src_data));
	
	for (i = 0; i < length; i++) {
		flash_src_data[i] = i;
	}
	
	printf("flash_src_data:\t");
	phex(flash_src_data, length);

	rc = mem2flash(flash_src_data, length);
	if (rc != ERR_NONE) {
		printf("FAILURE! mem2flash returned %ld\n", rc);
		return rc;
	}
	
	printf("zeroing out flash_src_data in main memory\n");
	for (i = 0; i < length; i++) {
		flash_src_data[i] = 0;
	}
	printf("flash_src_data:\t");
	phex(flash_src_data, length);

	rc = flash2mem(flash_src_data, length);
	if (rc != ERR_NONE) {
		printf("FAILURE! flash2mem returned %ld\n", rc);
		return rc;
	}
	
	printf("flash_src_data:\t");
	phex(flash_src_data, length);
	
	return rc;
}