import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

import pandas as pd
import os
from sys import platform
from time import time
from shutil import copy
import math

from pydgilib_extra import LOGGER_OBJECT, LOGGER_CSV, LOGGER_PLOT, DGILibExtra
from experiment.averages import Averages
from experiment.plotting import *
from experiment.helpers import *

import dgilib_threaded as dgi_t
from atprogram.atprogram import atprogram

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass


def process_folder_namings(experiment, iterations, output_dir, hash_size=8, epsilon=0.5, mod_precision=10, attempt=1):
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

    # File locations for plotting
    exprm_output_folder_path = os.path.join(output_dir, experiment_name)
    original_output_path = os.path.join(output_dir, "original_output.csv")

    exprm_output_name = experiment_name + "_output.csv"
    exprm_averages_name = experiment_name + "_averages.csv"
    exprm_output_csv_path = os.path.join(
        exprm_output_folder_path, exprm_output_name)
    exprm_averages_csv_path = os.path.join(
        exprm_output_folder_path, exprm_averages_name)

    return (experiment_name, exprm_output_folder_path, exprm_output_csv_path,
            exprm_averages_csv_path, arm_kalman_solution_parent_folder_path, arm_kalman_solution_path,
            original_output_path)


def experiment_loop(experiment, iterations, output_dir, attempt=1, hash_size=8,
                    epsilon=0.5, mod_precision=10, program=True, duration=9999, verbose=1):

    (experiment_name, exprm_output_folder_path, exprm_output_csv_path,
     exprm_averages_csv_path, arm_kalman_solution_parent_folder_path, arm_kalman_solution_path,
     original_output_path) = \
        process_folder_namings(experiment, iterations,
                               output_dir, hash_size,
                               epsilon, mod_precision)

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
        "log_folder": exprm_output_folder_path,
        "file_name_base": experiment_name
    }

    props_and_values = {
        "HASHSIZE": hash_size,
        "ITERATIONS": iterations,
        "EPSILON": '{0:f}'.format(epsilon),
        "EPSILON_MOD": int(epsilon * mod_precision),
        "MOD_PRECISION": mod_precision
    }

    try:
        os.mkdir(output_dir)
        if verbose >= 2:
            print("Folder '" + output_dir + "' created.")
    except FileExistsError:
        if verbose >= 2:
            print("WARNING: Folder '" + output_dir + "' already exists.")
        pass

    try:
        os.mkdir(exprm_output_folder_path)
        if verbose >= 2:
            print("Folder '" + exprm_output_folder_path + "' created.")
    except FileExistsError:
        if verbose >= 2:
            print("WARNING: Folder '" +
                  exprm_output_folder_path + "' already exists.")
        pass

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
            print("File '" + hashtable_header_file_path + "' now contains:")
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
            exprm_output_folder_path, experiment_name + "_table_stats.txt")
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
            print("File '" + hashtable_header_file_path + "' now contains:")
        if verbose >= 2:
            print_file(hashtable_header_file_path, "#define HASHSIZE")
        if verbose >= 2:
            print_file(hashtable_header_file_path, "#define EPSILON")
        if verbose >= 2:
            print_file(hashtable_header_file_path, "#define MOD_PRECISION")
        if verbose >= 2:
            print_file(hashtable_header_file_path, "#define EPSILON_MOD")

    main_file_from = os.path.join(
        arm_kalman_solution_parent_folder_path, "main_" + experiment + ".c")
    main_file_to = os.path.join(arm_kalman_solution_path, "main.c")

    copy(main_file_from, main_file_to)
    if verbose >= 2:
        print("Copied '" + main_file_from + "' to '" + main_file_to + "'")

    if program:
        atprogram(arm_kalman_solution_path, verbose=max(verbose-1, 0))

    # Measurement
    dgi_t.measure(duration, iterations, dgilib_config_dict,
                  input_acc_file=config["input_acc_file"],
                  input_gyro_file=config["input_gyro_file"],
                  output_file=config["output_file"], waitForPlot=True,
                  verbose=verbose)

    # Averages
    # avg = Averages(data=data, preprocessed_data=preprocessed_data,
    #                average_function="leftpoint")
    # avg.calculate_averages_for_pin(1)
    # avg.write_to_csv(exprm_averages_path, verbose=verbose)


def averages_loop(experiment, iterations, output_dir, attempt=1, hash_size=8,
                  epsilon=0.5, mod_precision=10, program=True, duration=9999, verbose=1):

    (experiment_name, exprm_output_folder_path, exprm_output_csv_path,
     exprm_averages_csv_path, arm_kalman_solution_parent_folder_path, arm_kalman_solution_path,
     original_output_path) = \
        process_folder_namings(experiment, iterations,
                               output_dir, hash_size,
                               epsilon, mod_precision)

    start_time = 0
    if verbose >= 2:
        print("Loading dgilib data into memory for averging from csv files: " +
              os.path.join(output_dir, experiment_name, experiment_name) + "_[power/gpio].csv")
        start_time = time()
    data = get_dgilib_data_from_csv(output_dir, experiment_name)
    if verbose >= 2:
        duration = math.ceil(time() - start_time)
        print(
            "Finished getting dgilib data. Took {0} seconds...".format(duration))

    if verbose >= 2:
        print("Calculating averages... ")
        start_time = time()
    avg = Averages(data=data, average_function="leftpoint", verbose=verbose)

    avg.calculate_averages_for_pin(1)
    if verbose >= 2:
        duration = math.ceil(time() - start_time)
        print("Done calculating averages! Took {0} seconds. Writing averages csv...".format(
            duration))
    avg.write_to_csv(exprm_averages_csv_path)
