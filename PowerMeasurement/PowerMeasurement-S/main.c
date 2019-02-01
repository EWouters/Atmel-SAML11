#include <atmel_start.h>

#include "serial_interface.h"

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();

	/* Replace with your application code */
	char * command[CMD_MAX_LEN + 1];
	while (1) {
		//delay_ms(1000);
		*command = serial_command();
	}
}
