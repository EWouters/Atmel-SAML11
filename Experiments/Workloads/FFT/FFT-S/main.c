#include <atmel_start.h>
#include "kissfft/kiss_fft.h"

#define NFFT 128

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	size_t buflen = sizeof(kiss_fft_cpx)*NFFT;

	kiss_fft_cpx  * in = (kiss_fft_cpx*)malloc(buflen);
	kiss_fft_cpx  * out= (kiss_fft_cpx*)malloc(buflen);
	kiss_fft_cfg  cfg = kiss_fft_alloc(NFFT,0,NULL,NULL);
	int k;

	for (k=0;k<NFFT;++k) {
		in[k].r = (k % 65536) - 32768;
		in[k].i = (k % 65536) - 32768;
	}

	kiss_fft(cfg,in,out);

	
	kiss_fft_free(cfg);
	
	kiss_fft_cfg  icfg = kiss_fft_alloc(NFFT,1,NULL,NULL);
	
	kiss_fft(icfg,out,in);
	    
	kiss_fft_free(in);
	kiss_fft_free(out);
	kiss_fft_free(icfg);
}
