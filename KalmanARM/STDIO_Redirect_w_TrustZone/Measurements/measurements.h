/*
 * measurements.h
 *
 * Created: 2019-02-25 12:45:01
 *  Author: Dragos
 */ 


#ifndef MEASUREMENTS_H_
#define MEASUREMENTS_H_

#include "../globals.h"

void DONT_MEASURE() {
	gpio_set_pin_level(DGI_GPIO3, true);
	
	//gpio_set_pin_level(LED0, false);
	delay_ms(DELAY_DURATION);
}

void MEASURE() {
	//gpio_set_pin_level(LED0, true);
	delay_ms(DELAY_DURATION);
	
	gpio_set_pin_level(DGI_GPIO3, false);	
}

#endif /* MEASUREMENTS_H_ */