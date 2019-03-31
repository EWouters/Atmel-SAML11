import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

import pandas as pd
import os
from sys import platform
from time import time, sleep
from shutil import copy

from pydgilib_extra import LOGGER_OBJECT, LOGGER_CSV, LOGGER_PLOT
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

def loop(experiment, iterations, attempt=1, hash_size=8, epsilon=0.5, mod_precision=10, program=True, duration=9999, output_dir="output", verbose=1):
    # Get hash size in the experiment's name
    hash_size_str = ""
    epsilon_str=""
    mod_precision_str = ""
    if experiment == "hash":
        hash_size_str = str(hash_size) + "_"
        epsilon_str = "eps_" + str(epsilon) + "_"
        mod_precision_str = "mod_" + str(mod_precision) + "_"
    exprm_file_name_base = experiment + "_" + hash_size_str + epsilon_str + mod_precision_str + str(iterations) + "iter" + "_" + str(attempt)

    # File locations for experiments
    project_base_dir = os.path.join(os.path.dirname(os.getcwd()),"KalmanARM")
    project_dir = os.path.join(project_base_dir, "STDIO_Redirect_w_TrustZone")

    exprm_base_dir = os.path.join(os.getcwd(), output_dir)
    main_file_from = os.path.join(project_base_dir, "main_" + experiment + ".c")
    main_file_to = os.path.join(project_dir, "main.c")

    initial_output = os.path.join(exprm_base_dir, "output_arm.csv")

    # File locations for plotting
    exprm_output_base_folder = os.path.join(os.getcwd(), output_dir, exprm_file_name_base)
    original_output_path = os.path.join(os.getcwd(), output_dir, "original_output.csv")

    exprm_output_name = exprm_file_name_base + "_output.csv"
    exprm_averages_name = exprm_file_name_base + "_averages.csv"
    #exprm_averages_name_pulse = exprm_file_name_base + "_averages_pulse.csv"
    exprm_output_path = os.path.join(exprm_output_base_folder, exprm_output_name)
    exprm_averages_path = os.path.join(exprm_output_base_folder, exprm_averages_name)
    #exprm_averages_path_pulse = os.path.join(exprm_output_base_folder, exprm_averages_name_pulse)

    # DGILib constants
    config = {
        "input_acc_file": os.path.join("input", "input_acc.csv"),
        "input_gyro_file": os.path.join("input", "input_gyro.csv"),
        "output_file": exprm_output_path
    }

    dgilib_config_dict = {
        "loggers": [LOGGER_OBJECT, LOGGER_CSV],
        "plot_pins_method": "highlight",
        "gpio_delay_time": 0.0015,
        "log_folder": exprm_output_base_folder,
        "file_name_base": exprm_file_name_base
    }

    props_and_values = {
        "HASHSIZE": hash_size,
        "ITERATIONS": iterations,
        "EPSILON" : '{0:f}'.format(epsilon),
        "EPSILON_MOD": int(epsilon * mod_precision),
        "MOD_PRECISION" : mod_precision
    }

    try:
        os.mkdir(exprm_base_dir)
        if verbose >= 2: print("Folder '" + exprm_base_dir + "' created.")
    except FileExistsError:
        if verbose >= 2: print("WARNING: Folder '" + exprm_base_dir + "' already exists.")
        pass

    try:
        os.mkdir(exprm_output_base_folder)
        if verbose >= 2: print("Folder '" + exprm_output_base_folder + "' created.")
    except FileExistsError:
        if verbose >= 2: print("WARNING: Folder '" + exprm_output_base_folder + "' already exists.")
        pass

    # KalmanC++
    if "hash" in experiment:
        x86_kalman_dir = os.path.join(os.path.dirname(os.getcwd()),"KalmanC++")
        x86_kalman_hash_header = os.path.join(x86_kalman_dir, "HashTable", "hashtable.h")
        
        hashtable_header_file_path = x86_kalman_hash_header
        hashtable_header_file_clone_path = os.path.join(x86_kalman_dir, "Originals", "hashtable.h")
        replace_define_value_in_file(hashtable_header_file_clone_path, hashtable_header_file_path, props_and_values)
        #replace_define_value_in_file(hashtable_header_file_clone_path, hashtable_header_file_path, "MOD_PRECISION", mod_precision)
        #replace_define_value_in_file(hashtable_header_file_clone_path, hashtable_header_file_path, "EPSILON", epsilon)

        if verbose >= 2: print("File '" + hashtable_header_file_path + "' now contains:")
        if verbose >= 2: print_file(hashtable_header_file_path, "#define HASHSIZE")
        if verbose >= 2: print_file(hashtable_header_file_path, "#define EPSILON")
        if verbose >= 2: print_file(hashtable_header_file_path, "#define MOD_PRECISION")
        if verbose >= 2: print_file(hashtable_header_file_path, "#define EPSILON_MOD")

        compile_hash()
        run_hash(verbose=verbose)

        output_file_from = os.path.join(x86_kalman_dir, "debug.txt")
        output_file_to = os.path.join(exprm_output_base_folder, exprm_file_name_base + "_table_stats.txt")
        copy(output_file_from, output_file_to)
        if verbose >= 1: print("Copied '" + output_file_from + "' to '" + output_file_to + "'")

    # KalmanARM
    if "hash" in experiment:
        hashtable_header_file_clone_path = os.path.join(project_base_dir, "hashtable.h")
        hashtable_header_file_path = os.path.join(project_dir, "HashTable", "hashtable.h")
        replace_define_value_in_file(hashtable_header_file_clone_path, hashtable_header_file_path, props_and_values)
        #replace_define_value_in_file(hashtable_header_file_clone_path, hashtable_header_file_path, "MOD_PRECISION", mod_precision)
        #replace_define_value_in_file(hashtable_header_file_clone_path, hashtable_header_file_path, "EPSILON", epsilon)

        if verbose >= 2: print("File '" + hashtable_header_file_path + "' now contains:")
        if verbose >= 2: print_file(hashtable_header_file_path, "#define HASHSIZE")
        if verbose >= 2: print_file(hashtable_header_file_path, "#define EPSILON")
        if verbose >= 2: print_file(hashtable_header_file_path, "#define MOD_PRECISION")
        if verbose >= 2: print_file(hashtable_header_file_path, "#define EPSILON_MOD")

    copy(main_file_from, main_file_to)
    if verbose >= 2: print("Copied '"+ main_file_from + "' to '" + main_file_to + "'")

    if program: atprogram(project_dir, verbose=max(verbose-1,0))

    # Measurement
    data, preprocessed_data = dgi_t.measure(duration, iterations, dgilib_config_dict, input_acc_file=config["input_acc_file"], input_gyro_file=config["input_gyro_file"], output_file=config["output_file"], waitForPlot=True, verbose=verbose)
    
    # Averages
    avg = Averages(data = data, preprocessed_data = preprocessed_data, average_function="leftpoint")
    avg.calculate_averages_for_pin(1)
    avg.write_to_csv(exprm_averages_path, verbose=verbose)

    # avg2 = DGILibAverages(data = data, preprocessed_data = preprocessed_data, average_function="pulse")
    # avg2.calculate_averages_for_pin(1)
    # avg2.write_to_csv(exprm_averages_path_pulse, verbose=verbose)
