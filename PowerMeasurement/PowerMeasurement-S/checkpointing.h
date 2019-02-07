/*
 * checkpointing.h
 *
 * Created: 2019-02-06 16:14:17
 *  Author: erikw_000
 */ 


#ifndef CHECKPOINTING_H_
#define CHECKPOINTING_H_

#include "driver_init.h"
//#include "utils.h"

// https://stackoverflow.com/questions/29441005/aes-ctr-encryption-and-decryption

//#define CHECK_LENGTH_IS_PAGE_SIZE
#define AES_BLOCK_SIZE 256

struct ctr_state
{
	unsigned char ivec[AES_BLOCK_SIZE];
	unsigned int num;
	unsigned char ecount[AES_BLOCK_SIZE];
};

int mem2flash(const uint8_t *buffer, const uint16_t length);
int flash2mem(uint8_t *buffer, uint32_t length);
int test_write_flash(int num_bytes);

//int checkpointing( int mode,
				//size_t length,
				//unsigned char iv[16],
				//const unsigned char *input);
//
//int checkpoint()
 //aes
//
//restore()


#endif /* CHECKPOINTING_H_ */