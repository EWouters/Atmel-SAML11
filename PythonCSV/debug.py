from pydgilib_extra import LOGGER_OBJECT, LOGGER_CSV, LOGGER_PLOT, DGILibAverages
import dgilib_threaded as dgi_t
import os
from atprogram.atprogram import *

dgilib_config_dict = {
    "loggers": [LOGGER_OBJECT, LOGGER_CSV],
    "plot_pins": [False, True, False, False],
    "plot_pins_values": [False, True, False, False],
    "plot_pins_method": "highlight",
    "gpio_delay_time": 0.0015,
    "log_folder": os.path.join(os.getcwd(), "output"),
    "file_name_base": "debug_log"
}

config = {
    "input_acc_file": os.path.join("input", "input_acc.csv"),
    "input_gyro_file": os.path.join("input", "input_gyro.csv"),
    "output_file": os.path.join("output", "output_arm_debug.csv")
}

#atprogram("C:\\Users\\Dragos\\Dropbox\\RISE\\Git\\KalmanARM\\STDIO_Redirect_w_TrustZone", verbose=1)

data, processed_data = dgi_t.measure(
    duration=120, iterations=20, dgilib_config_dict=dgilib_config_dict,
    input_acc_file=config["input_acc_file"], input_gyro_file=config["input_gyro_file"], output_file=config["output_file"], waitForPlot=True
)

#dgi_t.show_plot_for_data(data)

data = dgi_t.load_from_csv(dgilib_config_dict["log_folder"], dgilib_config_dict["file_name_base"])
avg = DGILibAverages(data = data, average_function="leftpoint")
avg.calculate_averages_for_pin(1, ignore_first_average=False)

#avg.print_averages_for_pin(1,5)

averages_path = os.path.join(dgilib_config_dict["log_folder"], "debug_averages.csv")
avg.write_to_csv(averages_path)

avg2 = DGILibAverages(average_function="leftpoint")
avg2.read_from_csv(averages_path)
#avg2.write_to_csv(averages_path)

avg2.calculate_averages_for_pin(1)
avg2.print_averages_for_pin(1)

