/*
 * Code generated from Atmel Start.
 *
 * This file will be overwritten when reconfiguring your Atmel Start project.
 * Please copy examples or other code you want to keep to a separate file
 * to avoid losing it when reconfiguring.
 */

#include "driver_init.h"
#include <peripheral_clk_config.h>
#include <utils.h>
#include <hal_init.h>

#if (defined(__ARM_FEATURE_CMSE) && (__ARM_FEATURE_CMSE != 3U))
/* Weak Non-secure callable function. Real one should be in secure gateway library. */
WEAK int32_t nsc_periph_clock_init(uint32_t gclk_id, uint32_t gclk_src)
{
	(void)gclk_id;
	(void)gclk_src;
	return 0;
}
#endif

/**
 * \brief NVMCTRL initialization function
 *
 * Enables NVMCTRL peripheral, clocks and initializes driver
 */
void FLASH_0_clock_init(void)
{
#if (defined(__ARM_FEATURE_CMSE) && (__ARM_FEATURE_CMSE == 3U))
	hri_mclk_set_AHBMASK_NVMCTRL_bit(MCLK);
	hri_mclk_set_APBBMASK_NVMCTRL_bit(MCLK);
#endif
}

void TARGET_IO_PORT_init(void)
{
	gpio_set_pin_level(DGI_GPIO0, GPIO_LOW);
	gpio_set_pin_level(DGI_GPIO1, GPIO_LOW);
	gpio_set_pin_level(DGI_GPIO2, GPIO_LOW);
	gpio_set_pin_level(DGI_GPIO3, GPIO_LOW);

	// Set pin direction to output
	gpio_set_pin_direction(DGI_GPIO0, GPIO_DIRECTION_OUT);
	gpio_set_pin_direction(DGI_GPIO1, GPIO_DIRECTION_OUT);
	gpio_set_pin_direction(DGI_GPIO2, GPIO_DIRECTION_OUT);
	gpio_set_pin_direction(DGI_GPIO3, GPIO_DIRECTION_OUT);

	gpio_set_pin_function(DGI_GPIO0, GPIO_PIN_FUNCTION_OFF);
	gpio_set_pin_function(DGI_GPIO1, GPIO_PIN_FUNCTION_OFF);
	gpio_set_pin_function(DGI_GPIO2, GPIO_PIN_FUNCTION_OFF);
	gpio_set_pin_function(DGI_GPIO3, GPIO_PIN_FUNCTION_OFF);
}

void system_init(void)
{
#if (defined(__ARM_FEATURE_CMSE) && (__ARM_FEATURE_CMSE == 3U))
	/* Only initialize MCU clock when the project is TrustZone secure project  */
	init_mcu();
#endif

	FLASH_0_clock_init();
	FLASH_0_init();
	
	TARGET_IO_PORT_init();
}
