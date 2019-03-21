
from pydgilib_extra import INTERFACE_POWER, INTERFACE_GPIO, CHANNEL_A, POWER_CURRENT, LOGGER_PLOT, LOGGER_CSV, LOGGER_OBJECT

dgilib_config_dict = {
    "interfaces": [INTERFACE_POWER, INTERFACE_GPIO],
    "power_buffers": [{"channel": CHANNEL_A, "power_type": POWER_CURRENT}],
    "read_mode": [True, True, True, True],
    "write_mode": [False, False, False, False],
    "loggers": [LOGGER_OBJECT, LOGGER_PLOT], # LOGGER_PLOT, LOGGER_CSV
    "verbose": 0,
    "plot_xmax": 5,
    "plot_ymax": 0.0040,
    "plot_pins": [False, False, True, False],
    "plot_pins_values": [False, False, False, False],
    "plot_pins_method": "highlight",
    "automove_method" : "latest_data",
    "gpio_delay_time": 0.0015,
}