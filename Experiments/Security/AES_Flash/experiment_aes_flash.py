
from os import getcwd, path
import pickle

from pydgilib_extra import *
from atprogram.atprogram import atprogram

def experiment_aes_flash(project_root=getcwd(), verbose=1):
    project_path = path.join(project_root, "AES_Flash-S")
    atprogram(project_path, verbose=verbose)

    config_dict = {
        "interfaces": [INTERFACE_POWER, INTERFACE_GPIO],
        "loggers": [LOGGER_OBJECT, LOGGER_CSV],
        "gpio_delay_time" : 0.0007,
        "file_name_base": "experiment_aes_flash",
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

    aes_charge, aes_time = power_and_time_per_pulse(data, 2, stop_function=stop_function)
    flash_charge, flash_time = power_and_time_per_pulse(data, 3, stop_function=stop_function)

    aes_encrypt_charge = aes_charge[0::2]
    aes_decrypt_charge = aes_charge[1::2]
    aes_encrypt_time = aes_time[0::2]
    aes_decrypt_time = aes_time[1::2]

    flash_write_charge = flash_charge[0::2]
    flash_read_charge = flash_charge[1::2]
    flash_write_time = flash_time[0::2]
    flash_read_time = flash_time[1::2]

    # Save Charge amount list into pickle file
    pickle.dump(aes_encrypt_charge, open(path.join(project_root, "aes_flash_encrypt_charge.p"), "wb"))
    pickle.dump(aes_decrypt_charge, open(path.join(project_root, "aes_flash_decrypt_charge.p"), "wb"))
    pickle.dump(flash_write_charge, open(path.join(project_root, "aes_flash_write_charge.p"), "wb"))
    pickle.dump(flash_read_charge, open(path.join(project_root, "aes_flash_read_charge.p"), "wb"))
    
    if verbose:
        print(f"Saved results in: {path.join(project_root)}")

if __name__ == "__main__":
   experiment_aes_flash()
