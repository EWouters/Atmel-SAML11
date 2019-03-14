
from os import getcwd, path
import pickle

from pydgilib_extra import *
from atprogram.atprogram import atprogram

def experiment_aes(project_root=getcwd(), verbose=1):
    project_path = path.join(project_root, "AES-S")
    atprogram(project_path, verbose=verbose)

    config_dict = {
        "interfaces": [INTERFACE_POWER, INTERFACE_GPIO],
        "loggers": [LOGGER_OBJECT, LOGGER_CSV],
        "gpio_delay_time" : 0.0007,
        "file_name_base": "experiment_aes",
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

    encrypt_charge, encrypt_time = power_and_time_per_pulse(data, 2, stop_function=stop_function)
    decrypt_charge, decrypt_time = power_and_time_per_pulse(data, 3, stop_function=stop_function)

    # Save Charge amount list into pickle file
    pickle.dump(encrypt_charge, open(path.join(project_root, "aes_encrypt_charge.p"), "wb"))
    pickle.dump(decrypt_charge, open(path.join(project_root, "aes_decrypt_charge.p"), "wb"))
    
    if verbose:
        print(f"Saved results in: {path.join(project_root)}")

if __name__ == "__main__":
   experiment_aes()
