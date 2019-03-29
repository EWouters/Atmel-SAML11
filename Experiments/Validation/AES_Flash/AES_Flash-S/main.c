#include <atmel_start.h>



/* typedef for non-secure callback functions */
typedef void (*ns_funcptr_void) (void) __attribute__((cmse_nonsecure_call));

/* TZ_START_NS: Start address of non-secure application */
#define TZ_START_NS 0x00002000

#define MIN_AES_BLOCKS 1
#define MAX_AES_BLOCKS 100 //880

#define AES_KEY_SIZE 256

#define PULSE_GPIO
#define DELAY delay_ms(1);
#define SLEEP

#ifndef FLASH_PAGE_SIZE
#define FLASH_PAGE_SIZE 64
#endif

#ifndef NVMCTRL_FLASH_SIZE
#define NVMCTRL_FLASH_SIZE 65536
#endif

#ifndef NVMCTRL_ROW_PAGES
#define NVMCTRL_ROW_PAGES 4
#endif

#ifndef NVMCTRL_ROW_SIZE
#define NVMCTRL_ROW_SIZE (NVMCTRL_PAGE_SIZE * NVMCTRL_ROW_PAGES)
#endif

void load_ns_application(void)
{
	ns_funcptr_void NonSecure_ResetHandler;
	/* - Set non-secure main stack (MSP_NS) */
	__TZ_set_MSP_NS(*((uint32_t *)(TZ_START_NS)));
	/* - Get non-secure reset handler */
	NonSecure_ResetHandler = (ns_funcptr_void)(*((uint32_t *)((TZ_START_NS) + 4U)));
	/* Start non-secure state software application */
	NonSecure_ResetHandler();
}

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	
	size_t num_bytes = MAX_AES_BLOCKS * 16;
	
	uint32_t target_addr = FLASH_ADDR + FLASH_SIZE - num_bytes;
	target_addr -= target_addr % NVMCTRL_ROW_SIZE;
			
	for (uint32_t page_index = 0; page_index * FLASH_PAGE_SIZE < num_bytes; page_index += 1) {
		if (page_index % NVMCTRL_ROW_PAGES == 0) {
			/* Erase row in flash */
			FLASH_0_erase_row(target_addr + page_index * FLASH_PAGE_SIZE);
		}
	}
	
	// Load non-secure application
	load_ns_application();
}

void HardFault_Handler(void)
{
	// This indicates that an application has been denied access to a secure memory region
	while(1);
}