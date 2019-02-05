/*
 * aes_interface.h
 *
 * Created: 05/02/2019 14:22:31
 *  Author: Erik
 */ 

#ifndef AES_INTERFACE_H_
#define AES_INTERFACE_H_

#include "mbedtls/aes.h"

void generate_aes_key(unsigned char *);

void phex(unsigned char *, unsigned char);

#endif /* AES_INTERFACE_H_ */