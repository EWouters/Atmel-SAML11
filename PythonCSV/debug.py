from pydgilib_extra import LOGGER_OBJECT, LOGGER_CSV, LOGGER_PLOT
import dgilib_threaded as dgi_t
import os
from atprogram.atprogram import *

dgilib_config_dict = {
    "loggers": [LOGGER_OBJECT, LOGGER_CSV, LOGGER_PLOT],
    "plot_pins": [False, True, False, False],
    "plot_pins_values": [False, True, False, False],
    "plot_pins_method": "highlight",
    "gpio_delay_time": 0.0015
}

config = {
    "input_acc_file": os.path.join("input", "input_acc.csv"),
    "input_gyro_file": os.path.join("input", "input_gyro.csv"),
    "output_file": os.path.join("output", "output_arm_debug.csv")
}

atprogram("C:\\Users\\Dragos\\Dropbox\\RISE\\Git\\KalmanARM\\STDIO_Redirect_w_TrustZone", verbose=1)

data, processed_data = dgi_t.measure(
    duration=5, iterations=5, dgilib_config_dict=dgilib_config_dict,
    input_acc_file=config["input_acc_file"], input_gyro_file=config["input_gyro_file"], output_file=config["output_file"], waitForPlot=True
)

dgi_t.show_plot_for_data(data)

