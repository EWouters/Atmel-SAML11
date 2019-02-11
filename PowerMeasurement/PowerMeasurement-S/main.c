#include <atmel_start.h>
#include <hal_gpio.h>

#include "serial_interface.h"

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	gpio_set_pin_level(DGI_GPIO0,
	                // <y> Initial level
	                // <id> pad_initial_level
	                // <false"> Low
	                // <true"> High
	                false);
	
	gpio_set_pin_level(DGI_GPIO1,
	                // <y> Initial level
	                // <id> pad_initial_level
	                // <false"> Low
	                // <true"> High
	                true);
	
	gpio_set_pin_level(DGI_GPIO2,
	                // <y> Initial level
	                // <id> pad_initial_level
	                // <false"> Low
	                // <true"> High
	                false);
	
	gpio_set_pin_level(DGI_GPIO3,
	                // <y> Initial level
	                // <id> pad_initial_level
	                // <false"> Low
	                // <true"> High
	                true);

	// Set pin direction to output
	gpio_set_pin_direction(DGI_GPIO0, GPIO_DIRECTION_OUT);
	gpio_set_pin_direction(DGI_GPIO1, GPIO_DIRECTION_OUT);
	gpio_set_pin_direction(DGI_GPIO2, GPIO_DIRECTION_OUT);
	gpio_set_pin_direction(DGI_GPIO3, GPIO_DIRECTION_OUT);

	gpio_set_pin_function(DGI_GPIO0, GPIO_PIN_FUNCTION_OFF);
	gpio_set_pin_function(DGI_GPIO1, GPIO_PIN_FUNCTION_OFF);
	gpio_set_pin_function(DGI_GPIO2, GPIO_PIN_FUNCTION_OFF);
	gpio_set_pin_function(DGI_GPIO3, GPIO_PIN_FUNCTION_OFF);
	
	/* Replace with your application code */
	//char command[CMD_MAX_LEN + 1];
	while (1) {
		delay_ms(100);
		//serial_command(command);
		gpio_toggle_pin_level(DGI_GPIO0);
		gpio_toggle_pin_level(DGI_GPIO1);
		gpio_toggle_pin_level(DGI_GPIO2);
		gpio_toggle_pin_level(DGI_GPIO3);
	}
}
