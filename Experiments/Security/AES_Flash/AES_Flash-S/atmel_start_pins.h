/*
 * Code generated from Atmel Start.
 *
 * This file will be overwritten when reconfiguring your Atmel Start project.
 * Please copy examples or other code you want to keep to a separate file
 * to avoid losing it when reconfiguring.
 */
#ifndef ATMEL_START_PINS_H_INCLUDED
#define ATMEL_START_PINS_H_INCLUDED

#include <hal_gpio.h>

// SAML11 has 9 pin functions

#define GPIO_PIN_FUNCTION_A 0
#define GPIO_PIN_FUNCTION_B 1
#define GPIO_PIN_FUNCTION_C 2
#define GPIO_PIN_FUNCTION_D 3
#define GPIO_PIN_FUNCTION_E 4
#define GPIO_PIN_FUNCTION_F 5
#define GPIO_PIN_FUNCTION_G 6
#define GPIO_PIN_FUNCTION_H 7
#define GPIO_PIN_FUNCTION_I 8

#define GPIO_HIGH true
#define GPIO_LOW false

#define DGI_GPIO0 GPIO(GPIO_PORTA, 10)
#define DGI_GPIO1 GPIO(GPIO_PORTA, 11)
#define DGI_GPIO2 GPIO(GPIO_PORTA, 23)
#define DGI_GPIO3 GPIO(GPIO_PORTA, 27)

#endif // ATMEL_START_PINS_H_INCLUDED
