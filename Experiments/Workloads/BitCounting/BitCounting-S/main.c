#include <atmel_start.h>
#include <stdlib.h>

//#define GET_MAX_STACK_POINTER
#ifdef GET_MAX_STACK_POINTER
static int max_sp = 0;
#endif

#define NUM_UINTS 2048
/*
Verify in python using:

bitcount = "".join([bin(n) for n in range(NUM_UINTS)]).count('1')

*/

#define PULSE_GPIO
#define DELAY delay_ms(1);
#define SLEEP

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	delay_ms(10);

	// Allocate input.
	unsigned int *input = malloc(sizeof(unsigned int) * NUM_UINTS);
	
	
	// Fill with sequential data.
	for (size_t n = 0; n < NUM_UINTS; n++) {
		input[n] = n;
	}
	
	static int result = 0;
	
#ifdef PULSE_GPIO
	DELAY
	// Set GPIO pin high.
	gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
#endif
	
	// Add up bit count.
	for (size_t n = 0; n < NUM_UINTS; n++) {
		result += __builtin_popcount(input[n]);
	}
	
#ifdef PULSE_GPIO
	// Set GPIO pin low.
	gpio_set_pin_level(DGI_GPIO2, GPIO_LOW);
	DELAY
#endif
	
	// Free the memory
	free(input);

#ifdef PULSE_GPIO
	DELAY
	// Signal end of test
	gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
	gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);
#endif
}
