from tempfile import mkstemp
from shutil import copy
from os import fdopen, remove

import os
import subprocess

from experiment.averages import Averages
from pydgilib_extra import DGILibExtra, LOGGER_OBJECT, LoggerData, DGILibInterfaceGPIO, DGILibInterfacePower, INTERFACE_GPIO, INTERFACE_POWER

kalman_c_folder = "C:\\Users\\Dragos\\Dropbox\\College\\MasThesis\\Git\\KalmanC++"

############################################################
# Replacing #define values both in KalmanARM and KalmanC++ #
############################################################


def replace_define_value_in_file(clone_file_path, file_path, props_and_values):
    with open(clone_file_path, 'r') as old_file:
        with open(file_path, 'w') as new_file:
            for line in old_file:
                written = False
                for prop, value in props_and_values.items():
                    if (("#define " + prop + " ") in line):
                        new_file.write(
                            "#define {0} {1}\n".format(prop, str(value)))
                        written = True
                        break
                if not written:
                    new_file.write(line)


def print_file(file_path, specific_search="", extra_space=" "):
    with open(file_path) as f:
        for line in f:
            if specific_search == "":
                print(line.strip())
            elif specific_search + extra_space in line:
                print(line.strip())


################################################################
# Dealing with Kalman hash table hits counting on the computer #
################################################################


def compile_hash(verbose=1):
    global kalman_c_folder

    gcc_folder = "C:\\mingw32\\bin"
    gpp = "g++"
    gpp_path = os.path.join(gcc_folder, gpp)

    hashtable_folder = os.path.join(
        kalman_c_folder, "HashTable")
    source_files = [os.path.join(kalman_c_folder, "main_hash.cpp"),
                    os.path.join(kalman_c_folder, "HashTable", "hashtable.c")]
    exe_path = os.path.join(
        kalman_c_folder, "kalman-hash")

    with open("subprocess-call.txt", "w") as f:
        subprocess.call([gpp_path, "-m32", "-g", "-Wall", "-I" + kalman_c_folder, "-I" + hashtable_folder,
                         "-o", exe_path, "-lm", "-O0"] + source_files, stdout=f, stderr=f, shell=True)

    if verbose >= 1:
        with open("subprocess-call.txt", "r") as f:
            for line in f:
                print(line.strip())


def run_hash(verbose=1):
    global kalman_c_folder
    exe_path = os.path.join(
        kalman_c_folder, "kalman-hash.exe")

    if verbose >= 3:
        print("Executing " + str([exe_path]))
    subprocess.call([exe_path], cwd=kalman_c_folder, shell=True)

    if verbose >= 2:
        debug_path = os.path.join(
            kalman_c_folder, "debug.txt")
        with open(debug_path, "r") as f:
            for line in f:
                print(line.strip())


##############################################################################
# Dealing with power and gpio **csv's** after running experiment with DGILib #
#  (in order to show plots and calculate averages)                           #
##############################################################################


def get_dgilib_data_from_csv(output_dir, experiment_name):
    # For some reason, on 64 bit the dgilib.dll is not found
    # We need 64 bit to read big CSV
    # Therefore DGILibExtra is not used here

    interfaces = {INTERFACE_GPIO: DGILibInterfaceGPIO(),
                  INTERFACE_POWER: DGILibInterfacePower()}
    dgilib_logger_log_folder = os.path.join(output_dir, experiment_name)
    interface_file_name_base = experiment_name

    logger_data = LoggerData()

    for interface_id, interface in interfaces.items():
        logger_data[interface_id] += interface.csv_read_file(
            os.path.join(dgilib_logger_log_folder,
                         (interface_file_name_base + '_' +
                          interface.name + ".csv")))

    return logger_data


####################################################################################
# Dealing with power and gpio **data object** after running experiment with DGILib #
#  (in order to show plot)                                                         #
####################################################################################


def show_plot_for_dgilib_data(data):
    config_dict_plot = {
        "loggers": [LOGGER_OBJECT],
        "plot_pins_method": "highlight",
    }

    plot = DGILibPlot(config_dict_plot)

    plot.update_plot(logger_data)

    plot.keep_plot_alive()
