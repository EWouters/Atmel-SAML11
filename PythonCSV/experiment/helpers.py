from tempfile import mkstemp
from shutil import move
from os import fdopen, remove

import os
import subprocess

def replace_define_value_in_file(file_path, prop, value):
    #Create temp file
    filetemp_path, abs_path = mkstemp()
    with fdopen(filetemp_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if ("#define" in line) and (prop in line):
                    new_file.write("#define {0} {1}\n".format(prop, str(value)))
                else:
                    new_file.write(line)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def print_file(file_path, specific_search=""):
    with open(file_path) as f:
        for line in f:
            if specific_search == "":
                print(line.strip())
            elif specific_search in line:
                print(line.strip())

def compile_hash(print_output=True):
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

    if print_output:
        with open("subprocess-call.txt", "r") as f:
            for line in f:
                print(line.strip())

def run_hash(print_output=True, print_debug=True):
    project_folder = "C:\\Users\\Dragos\\Dropbox\\RISE\\Git\\KalmanC++"
    exe_path = os.path.join(project_folder, "kalman-hash.exe")

    #with open("subprocess-call-2.txt", "w") as f:
    print("Executing " + str([exe_path]))
    subprocess.call([exe_path], cwd=project_folder, shell=True)

    # if print_output:
    #     with open("subprocess-call.txt", "r") as f:
    #         for line in f:
    #             print(line.strip())

    if print_debug:
        debug_path = os.path.join(project_folder, "debug.txt")
        with open(debug_path, "r") as f:
            for line in f:
                print(line.strip())