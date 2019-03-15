#include <atmel_start.h>
#include "kissfft/kiss_fft.h"

//#define GET_MAX_STACK_POINTER
#ifdef GET_MAX_STACK_POINTER
static int max_sp = 0;
#endif

#define NFFT 128

#define PULSE_GPIO
#define DELAY delay_ms(1);
#define SLEEP

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	DELAY
	DELAY
	DELAY
	
#ifdef PULSE_GPIO
	DELAY
	// Set GPIO pin high.
	gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
#endif
	
	size_t buflen = sizeof(kiss_fft_cpx)*NFFT;

	kiss_fft_cpx  * in = (kiss_fft_cpx*)malloc(buflen);
	kiss_fft_cpx  * out= (kiss_fft_cpx*)malloc(buflen);
	kiss_fft_cfg  cfg = kiss_fft_alloc(NFFT,0,NULL,NULL);
		
#ifdef PULSE_GPIO
	// Set GPIO pin low.
	gpio_set_pin_level(DGI_GPIO2, GPIO_LOW);
	DELAY
#endif
	
	int k;

	for (k=0;k<NFFT;++k) {
		in[k].r = (k % 65536) - 32768;
		in[k].i = (k % 65536) - 32768;
	}

#ifdef PULSE_GPIO
	DELAY
	// Set GPIO pin high.
	gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);
#endif

	kiss_fft(cfg,in,out);

#ifdef GET_MAX_STACK_POINTER
	register int sp asm ("sp");
	max_sp = (sp > max_sp)? sp : max_sp;
#endif

#ifdef PULSE_GPIO
	// Set GPIO pin low.
	gpio_set_pin_level(DGI_GPIO3, GPIO_LOW);
	DELAY
#endif

#ifdef PULSE_GPIO
	DELAY
	// Set GPIO pin high.
	gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
#endif
	
	kiss_fft_free(cfg);
	
	kiss_fft_cfg  icfg = kiss_fft_alloc(NFFT,1,NULL,NULL);

#ifdef PULSE_GPIO
	// Set GPIO pin low.
	gpio_set_pin_level(DGI_GPIO2, GPIO_LOW);
	DELAY
#endif
	
#ifdef PULSE_GPIO
	DELAY
	// Set GPIO pin high.
	gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);
#endif
	
	kiss_fft(icfg,out,in);

#ifdef PULSE_GPIO
	// Set GPIO pin low.
	gpio_set_pin_level(DGI_GPIO3, GPIO_LOW);
	DELAY
#endif

#ifdef PULSE_GPIO
	DELAY
	// Set GPIO pin high.
	gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
#endif
	    
	kiss_fft_free(in);
	kiss_fft_free(out);
	kiss_fft_free(icfg);
	
#ifdef PULSE_GPIO
	// Set GPIO pin low.
	gpio_set_pin_level(DGI_GPIO2, GPIO_LOW);
	DELAY
#endif

	
#ifdef PULSE_GPIO
	DELAY
	// Signal end of test
	gpio_set_pin_level(DGI_GPIO2, GPIO_HIGH);
	gpio_set_pin_level(DGI_GPIO3, GPIO_HIGH);
#endif
}
