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

int test_aes_write_flash(int num_bytes)
{
	int32_t rc = ERR_NONE;
	
	mbedtls_aes_context aes;
	
	unsigned char key[32] = {
		0x60, 0x3d, 0xeb, 0x10, 0x15, 0xca, 0x71, 0xbe, 0x2b, 0x73, 0xae, 0xf0, 0x85, 0x7d, 0x77, 0x81,
	0x1f, 0x35, 0x2c, 0x07, 0x3b, 0x61, 0x08, 0xd7, 0x2d, 0x98, 0x10, 0xa3, 0x09, 0x14, 0xdf, 0xf4 };
	//unsigned char key[32];
	//generate_aes_key(key);
	
	unsigned char iv[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };
	unsigned char iv2[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };
	
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
	
	rc = mbedtls_aes_setkey_enc( &aes, key, 256 );
	if (rc != ERR_NONE) {
		printf("FAILURE! mbedtls_aes_setkey_enc returned %ld\n", rc);
		return rc;
	}
	rc = mbedtls_aes_crypt_cbc( &aes, MBEDTLS_AES_ENCRYPT, length, iv, flash_src_data, flash_src_data);
	if (rc != ERR_NONE) {
		printf("FAILURE! mbedtls_aes_crypt_cbc returned %ld\n", rc);
		return rc;
	}
	printf("encrypted in place:\t");
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
	
	rc = mbedtls_aes_setkey_dec( &aes, key, 256 );
	if (rc != ERR_NONE) {
		printf("FAILURE! mbedtls_aes_setkey_dec returned %ld\n", rc);
		return rc;
	}
	rc = mbedtls_aes_crypt_cbc( &aes, MBEDTLS_AES_DECRYPT, length, iv2, flash_src_data, flash_src_data);
	if (rc != ERR_NONE) {
		printf("FAILURE! mbedtls_aes_crypt_cbc returned %ld\n", rc);
		return rc;
	}
	printf("decrypted in place:\t");
	phex(flash_src_data, length);
	
	return rc;
}