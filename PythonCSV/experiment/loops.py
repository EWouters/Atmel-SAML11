
import os
import sys
from time import time
from shutil import copy
import math

from pydgilib_extra import LOGGER_CSV, LOGGER_PLOT, DGILibExtra
from experiment.averages import Averages
from experiment.plotting import *
from experiment.helpers import *
from experiment.tee import Tee

import dgilib_threaded as dgi_t
from atprogram.atprogram import atprogram, get_project_size

import traceback

import errno

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass


def process_folder_namings(experiment, iterations, output_dir, hash_size=8,
                           epsilon=0.5, mod_precision=10, attempt=1):
    # Get hash size in the experiment's name
    hash_size_str = ""
    epsilon_str = ""
    mod_precision_str = ""
    if experiment == "hash":
        hash_size_str = str(hash_size) + "_"
        epsilon_str = "eps_" + str(epsilon) + "_"
        mod_precision_str = "mod_" + str(mod_precision) + "_"
    experiment_name = experiment + "_" + hash_size_str + epsilon_str + \
        mod_precision_str + str(iterations) + "iter" + "_" + str(attempt)

    # File locations for experiments
    arm_kalman_solution_parent_folder_path = os.path.join(
        os.path.dirname(os.getcwd()), "KalmanARM")
    arm_kalman_solution_path = os.path.join(
        arm_kalman_solution_parent_folder_path, "STDIO_Redirect_w_TrustZone")

    # Results (averages, size) csv locations
    attempt_folder = "attempt_" + str(attempt)
    exprm_output_folder_path = os.path.join(output_dir, attempt_folder,
            experiment_name)
    original_output_path = os.path.join(output_dir, "original_output.csv")

    exprm_output_name = experiment_name + "_output.csv"
    exprm_averages_name = experiment_name + "_averages.csv"
    exprm_output_csv_path = os.path.join(
        exprm_output_folder_path, exprm_output_name)
    averages_csv_path = os.path.join(
        exprm_output_folder_path, exprm_averages_name)

    log_file_name = experiment_name + "_unnamed_log.txt"
    log_file_path = os.path.join(exprm_output_folder_path, log_file_name)

    power_gpio_folder_path = os.path.join(output_dir, "power_gpio", attempt_folder)

    return (experiment_name, exprm_output_folder_path, exprm_output_csv_path,
            power_gpio_folder_path, averages_csv_path,
            arm_kalman_solution_parent_folder_path, arm_kalman_solution_path,
            original_output_path, log_file_path)

def create_folder(folder_path, verbose):
    try:
        os.mkdir(folder_path)
        if verbose >= 2:
            print("Folder '" + folder_path + "' created.")
    except FileExistsError:
        if verbose >= 2:
            print("WARNING: Folder '" + folder_path +
                    "' already exists.")
        pass

def experiment_loop(experiment, iterations, output_dir, attempt=1, hash_size=8,
                    epsilon=0.5, mod_precision=10, program=True, duration=9999,
                    verbose=1, output_to_console=True, output_to_file=True):

    start_time_ = time()

    (experiment_name, exprm_output_folder_path, exprm_output_csv_path,
     power_gpio_folder_path, _,
     arm_kalman_solution_parent_folder_path, arm_kalman_solution_path,
     _, log_file_path) = \
        process_folder_namings(experiment, iterations,
                               output_dir, hash_size,
                               epsilon, mod_precision, attempt)

    # This object will help print both on the console and in a log file.
    # All information and especially errors will go to the log file now, at
    #  the path 'log_file_path'

    with Tee(log_file_path.replace("unnamed", "experiment"),
             output_to_console=output_to_console,
             output_to_file=output_to_file) as log:

        # DGILib constants
        config = {
            "input_acc_file": os.path.join("input", "input_acc.csv"),
            "input_gyro_file": os.path.join("input", "input_gyro.csv"),
            "output_file": exprm_output_csv_path
        }

        dgilib_config_dict = {
            "loggers": [LOGGER_CSV],
            "plot_pins_method": "highlight",
            "gpio_delay_time": 0.0015,
            "log_folder": power_gpio_folder_path,
            "file_name_base": experiment_name
        }

        props_and_values = {
            "HASHSIZE": hash_size,
            "ITERATIONS": iterations,
            "EPSILON": '{0:f}'.format(epsilon),
            "EPSILON_MOD": int(epsilon * mod_precision),
            "MOD_PRECISION": mod_precision
        }

        create_folder(output_dir, verbose)
        create_folder(exprm_output_folder_path, verbose)
        create_folder(power_gpio_folder_path, verbose)

        # KalmanC++
        if "hash" in experiment:
            x86_kalman_dir = os.path.join(
                os.path.dirname(os.getcwd()), "KalmanC++")
            x86_kalman_hash_header = os.path.join(
                x86_kalman_dir, "HashTable", "hashtable.h")

            hashtable_header_file_path = x86_kalman_hash_header
            hashtable_header_file_clone_path = os.path.join(
                x86_kalman_dir, "Originals", "hashtable.h")
            replace_define_value_in_file(
                hashtable_header_file_clone_path, hashtable_header_file_path,
                props_and_values)

            if verbose >= 2:
                print("File '" + hashtable_header_file_path +
                      "' now contains:")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define HASHSIZE")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define EPSILON")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define MOD_PRECISION")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define EPSILON_MOD")

            compile_hash()
            run_hash(verbose=verbose)

            output_file_from = os.path.join(x86_kalman_dir, "debug.txt")
            output_file_to = os.path.join(
                exprm_output_folder_path, experiment_name + "_hash.txt")
            copy(output_file_from, output_file_to)
            if verbose >= 1:
                print("Copied '" + output_file_from +
                      "' to '" + output_file_to + "'")

        # KalmanARM
        if "hash" in experiment:
            hashtable_header_file_clone_path = os.path.join(
                arm_kalman_solution_parent_folder_path, "hashtable.h")
            hashtable_header_file_path = os.path.join(
                arm_kalman_solution_path, "HashTable", "hashtable.h")
            replace_define_value_in_file(
                hashtable_header_file_clone_path, hashtable_header_file_path,
                props_and_values)

            if verbose >= 2:
                print("File '" + hashtable_header_file_path +
                      "' now contains:")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define HASHSIZE")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define EPSILON")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define MOD_PRECISION")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define EPSILON_MOD")

        main_file_from = os.path.join(
            arm_kalman_solution_parent_folder_path, "main_" + experiment +
            ".c")
        main_file_to = os.path.join(arm_kalman_solution_path, "main.c")

        copy(main_file_from, main_file_to)
        if verbose >= 2:
            print("Copied '" + main_file_from + "' to '" +
                  main_file_to + "'")

        if program:
            atprogram(arm_kalman_solution_path, verbose=max(verbose-1, 0))

        # Measurement
        dgi_t.measure(duration, iterations, dgilib_config_dict,
                      input_acc_file=config["input_acc_file"],
                      input_gyro_file=config["input_gyro_file"],
                      output_file=config["output_file"], waitForPlot=True,
                      verbose=verbose)
        
        duration_ = math.ceil(time() - start_time_)
        if verbose >= 1:
            print("Experiment loop took {0} seconds...".format(duration))

def averages_loop(experiment, iterations, output_dir, attempt=1, hash_size=8,
                  epsilon=0.5, mod_precision=10, verbose=1,
                  output_to_file=True, output_to_console=True):

    start_time_ = time()

    (experiment_name, exprm_output_folder_path, exprm_output_csv_path,
        power_data_folder_path, averages_csv_path,
        arm_kalman_solution_parent_folder_path, arm_kalman_solution_path,
        original_output_path, log_file_path) = \
        process_folder_namings(experiment, iterations,
                               output_dir, hash_size,
                               epsilon, mod_precision, attempt)

    with Tee(log_file_path.replace("unnamed", "averages"),
             output_to_file=output_to_file,
             output_to_console=output_to_console) as log:

        start_time = 0

        if verbose >= 2:
            print("Loading dgilib data into memory for averging from " +
                  "csv files: " +
                  os.path.join(power_data_folder_path,
                               experiment_name) +
                  "_[power/gpio].csv")
            start_time = time()
        data = get_dgilib_data_from_csv(power_data_folder_path,
                                        experiment_name)

        if verbose >= 2:
            duration = math.ceil(time() - start_time)
            print(
                "Finished getting dgilib data. Took " +
                "{0} seconds...".format(duration))

        if verbose >= 2:
            print("Calculating averages... ")
            start_time = time()
        avg = Averages(data=data, average_function="leftpoint",
                       verbose=verbose)

        ignore_first_average = False
        if verbose >= 1:
            print("Ignore first average is {0}!".format(ignore_first_average))

        avg.calculate_averages_for_pin(1, ignore_first_average=
                                        ignore_first_average)

        if verbose >= 2:
            duration = math.ceil(time() - start_time)
            print("Done calculating averages! Took" +
                  " {0} seconds. Writing averages csv...".format(duration))
        avg.write_to_csv(averages_csv_path)

        duration_ = math.ceil(time() - start_time_)

        if verbose >= 1:
            print("Averages loop took {0} seconds...".format(duration))


def sizes_loop(experiment, iterations, output_dir, attempt=1, hash_size=8,
               epsilon=0.5, mod_precision=10, program=False, verbose=1,
               output_to_console=True, output_to_file=True):

    start_time_ = time()

    (experiment_name, exprm_output_folder_path, _,
     power_data_folder_path, averages_csv_path,
     arm_kalman_solution_parent_folder_path, arm_kalman_solution_path,
     original_output_path, log_file_path) = \
        process_folder_namings(experiment, iterations,
                               output_dir, hash_size,
                               epsilon, mod_precision, attempt)

    with Tee(log_file_path.replace("unnamed", "sizes"),
             output_to_console=output_to_console,
             output_to_file=output_to_file) as log:

        if verbose >= 2:
            print("Compiling in order to obtain the program sizes...")

        props_and_values = {
            "HASHSIZE": hash_size,
            "ITERATIONS": iterations,
            "EPSILON": '{0:f}'.format(epsilon),
            "EPSILON_MOD": int(epsilon * mod_precision),
            "MOD_PRECISION": mod_precision
        }

        # KalmanARM
        if "hash" in experiment:
            hashtable_header_file_clone_path = os.path.join(
                arm_kalman_solution_parent_folder_path, "hashtable.h")
            hashtable_header_file_path = os.path.join(
                arm_kalman_solution_path, "HashTable", "hashtable.h")
            replace_define_value_in_file(
                hashtable_header_file_clone_path, hashtable_header_file_path,
                props_and_values)

            if verbose >= 2:
                print("File '" + hashtable_header_file_path +
                      "' now contains:")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define HASHSIZE")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define EPSILON")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define MOD_PRECISION")
            if verbose >= 2:
                print_file(hashtable_header_file_path, "#define EPSILON_MOD")

        main_file_from = os.path.join(
            arm_kalman_solution_parent_folder_path,
            "main_" + experiment + ".c")
        main_file_to = os.path.join(arm_kalman_solution_path, "main.c")

        copy(main_file_from, main_file_to)
        if verbose >= 2:
            print("Copied '" + main_file_from +
                  "' to '" + main_file_to + "'")

        result = get_project_size(
            arm_kalman_solution_path, verbose=max(verbose - 1, 0))

        project_size_file_path = os.path.join(
            exprm_output_folder_path, experiment_name + "_size.txt")
        with open(project_size_file_path, "w") as f:
            for k, v in result.items():
                f.write(str(k) + ": " + str(v) + "\n")

        if verbose >= 2:
            print("Written project size details to: '" +
                  project_size_file_path + "'\n")

        duration_ = math.ceil(time() - start_time_)

        if verbose >= 1:
            print("Size loop took {0} seconds...".format(duration_))
