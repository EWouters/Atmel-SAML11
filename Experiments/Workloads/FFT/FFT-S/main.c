#include <atmel_start.h>
#include "kissfft/kiss_fft.h"

//#define GET_MAX_STACK_POINTER
#ifdef GET_MAX_STACK_POINTER
static int max_sp = 0;
#endif

#define NFFT 128

#define SLEEP

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	START_MEASURE(DGI_GPIO2);
	size_t buflen = sizeof(kiss_fft_cpx)*NFFT;

	kiss_fft_cpx  * in = (kiss_fft_cpx*)malloc(buflen);
	kiss_fft_cpx  * out= (kiss_fft_cpx*)malloc(buflen);
	kiss_fft_cfg  cfg = kiss_fft_alloc(NFFT,0,NULL,NULL);
	STOP_MEASURE(DGI_GPIO2);
	
	int k;

	for (k=0;k<NFFT;++k) {
		in[k].r = (k % 65536) - 32768;
		in[k].i = (k % 65536) - 32768;
	}

	START_MEASURE(DGI_GPIO3);
	kiss_fft(cfg,in,out);
	STOP_MEASURE(DGI_GPIO3);

#ifdef GET_MAX_STACK_POINTER
	register int sp asm ("sp");
	max_sp = (sp > max_sp)? sp : max_sp;
#endif

	START_MEASURE(DGI_GPIO2);
	kiss_fft_free(cfg);
	
	kiss_fft_cfg  icfg = kiss_fft_alloc(NFFT,1,NULL,NULL);
	STOP_MEASURE(DGI_GPIO2);
	
	START_MEASURE(DGI_GPIO3);
	kiss_fft(icfg,out,in);
	STOP_MEASURE(DGI_GPIO3);

	START_MEASURE(DGI_GPIO2);	    
	kiss_fft_free(in);
	kiss_fft_free(out);
	kiss_fft_free(icfg);
	STOP_MEASURE(DGI_GPIO2);

	END_MEASUREMENT;
}
