
from os import getcwd, path
import pickle

from pydgilib_extra import *
from atprogram.atprogram import atprogram

def experiment_trustzone(project_root=getcwd(), verbose=1):
    project_path_s = path.join(project_root, "TrustZone-S")
    project_path_ns = path.join(project_root, "TrustZone-NS")
    atprogram(project_path_ns, verbose=verbose)
    atprogram(project_path_s, verbose=verbose, erase=False)

    config_dict = {
        "interfaces": [INTERFACE_POWER, INTERFACE_GPIO],
        "power_buffers": [{"channel": CHANNEL_A, "power_type": POWER_CURRENT}],
        "read_mode": [True, True, True, True],
        "loggers": [LOGGER_OBJECT, LOGGER_CSV],
        "gpio_delay_time" : 0.0007,
        "file_name_base": "experiment_trustzone",
        "log_folder": project_root,
        "verbose": verbose-1
    }
    
    def stop_fn(logger_data):
        return all(logger_data.gpio.values[-1])
    
    if verbose:
        print(f"Start DGILibExtra with config: \n{config_dict}\n")

    data = []
    with DGILibExtra(**config_dict) as dgilib:
        dgilib.device_reset()
        dgilib.logger.log(1000,stop_fn)
        data = dgilib.data
        
    if verbose:
        print(f"DGILibExtra data: {data}")

    def stop_function(pin_values):
        return all(pin_values)

    nsc_store_charge, nsc_store_time = power_and_time_per_pulse(data, 2, stop_function=stop_function)
    nsc_load_charge, nsc_load_time = power_and_time_per_pulse(data, 3, stop_function=stop_function)

    # Save Charge amount list into pickle file
    pickle.dump(nsc_store_charge, open(path.join(project_root, "trustzone_store_charge.p"), "wb"))
    pickle.dump(nsc_load_charge, open(path.join(project_root, "trustzone_load_charge.p"), "wb"))
    
    if verbose:
        print(f"Saved results in: {path.join(project_root)}")

if __name__ == "__main__":
   experiment_trustzone()
