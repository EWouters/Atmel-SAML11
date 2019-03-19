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

#define SLEEP

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();

	// Allocate input.
	unsigned int *input = malloc(sizeof(unsigned int) * NUM_UINTS);
	
	// Fill with sequential data.
	for (size_t n = 0; n < NUM_UINTS; n++) {
		input[n] = n;
	}
	
	static int result = 0;
	
	START_MEASURE(DGI_GPIO2);
	// Add up bit count.
	for (size_t n = 0; n < NUM_UINTS; n++) {
		result += __builtin_popcount(input[n]);
	}
	STOP_MEASURE(DGI_GPIO2);
	
	// Free the memory
	free(input);

	END_MEASUREMENT;
}
