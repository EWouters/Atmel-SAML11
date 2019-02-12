#include <atmel_start.h>
#include <hal_gpio.h>

#include "serial_interface.h"

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	/* Replace with your application code */
	//char command[CMD_MAX_LEN + 1];
	while (1) {
		delay_ms(100);
		//serial_command(command);
		gpio_toggle_pin_level(DGI_GPIO0);
		delay_ms(10);
		gpio_toggle_pin_level(DGI_GPIO1);
		delay_ms(10);
		gpio_toggle_pin_level(DGI_GPIO2);
		delay_ms(10);
		gpio_toggle_pin_level(DGI_GPIO3);
		gpio_toggle_pin_level(LED0);
	}
}
