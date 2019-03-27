from tempfile import mkstemp
from shutil import copy
from os import fdopen, remove
from time import sleep

import os
import subprocess

def replace_define_value_in_file(clone_file_path, file_path, props_and_values, sleep_time = 0.01):
    #remove(file_path)
    #sleep(sleep_time)
    with open(clone_file_path,'r') as old_file:
        with open(file_path, 'w') as new_file:
            for line in old_file:
                written = False
                for prop, value in props_and_values.items():
                    if (("#define " + prop) in line):
                        new_file.write("#define {0} {1}\n".format(prop, str(value)))
                        #print("--> " + line + " <-- changed to: " + "#define {0} {1}\n".format(prop, str(value)), end='')
                        written = True
                        break
                if not written: new_file.write(line)
                        #print(line, end='')

    # loop = True
    # while loop:
    #     try:
    #         sleep(sleep_time)
            
    #     except PermissionError:
    #         loop = True
    #     else:
    #         loop = False

    # loop = True
    # while loop:
    #     try:
    #         sleep(sleep_time)
            
    #     except PermissionError:
    #         loop = True
    #     else:
    #         loop = False
    

def print_file(file_path, specific_search=""):
    with open(file_path) as f:
        for line in f:
            if specific_search == "":
                print(line.strip())
            elif specific_search in line:
                print(line.strip())

def compile_hash(verbose = 1):
    gcc_folder = "C:\\mingw32\\bin"
    gpp = "g++"
    gpp_path = os.path.join(gcc_folder, gpp)

    project_folder = "C:\\Users\\Dragos\\Dropbox\\RISE\\Git\\KalmanC++"
    hashtable_folder = os.path.join(project_folder, "HashTable")
    source_files = [os.path.join(project_folder, "main_hash.cpp"),
                    os.path.join(project_folder, "HashTable", "hashtable.c")]
    exe_path = os.path.join(project_folder, "kalman-hash")

    with open("subprocess-call.txt", "w") as f:
        subprocess.call([gpp_path, "-m32", "-g", "-Wall", "-I" + project_folder, "-I" + hashtable_folder, "-o", exe_path, "-lm", "-O0"] + source_files, stdout=f, stderr=f, shell=True)

    if verbose >= 1:
        with open("subprocess-call.txt", "r") as f:
            for line in f:
                print(line.strip())

def run_hash(verbose=1):
    project_folder = "C:\\Users\\Dragos\\Dropbox\\RISE\\Git\\KalmanC++"
    exe_path = os.path.join(project_folder, "kalman-hash.exe")

    #with open("subprocess-call-2.txt", "w") as f:
    if verbose >= 3: print("Executing " + str([exe_path]))
    subprocess.call([exe_path], cwd=project_folder, shell=True)

    # if print_output:
    #     with open("subprocess-call.txt", "r") as f:
    #         for line in f:
    #             print(line.strip())

    if verbose >= 2:
        debug_path = os.path.join(project_folder, "debug.txt")
        with open(debug_path, "r") as f:
            for line in f:
                print(line.strip())