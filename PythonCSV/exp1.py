
import dgilib_threaded as dgi_t
from experiment.helpers import restore_averages
#from experiment.plots import error_barchart, wait_for_plot
from atprogram.atprogram import atprogram
from shutil import copy
import os

program = True
output_filename_extension = "hash-32"

def use_baseline():
    output_filename_extension = "baseline"
    base_dir = "C:\\Users\\Dragos\\Dropbox\\RISE\\Git\\KalmanARM"
    copy(base_dir + "\\main_baseline.c", base_dir + "\\STDIO_Redirect_w_TrustZone\\main.c")

def use_hash():
    output_filename_extension = "hash-32"
    base_dir = "C:\\Users\\Dragos\\Dropbox\\RISE\\Git\\KalmanARM"
    copy(base_dir + "\\main_hash.c", base_dir + "\\STDIO_Redirect_w_TrustZone\\main.c")

# Step 1: Compiling
if program: 
    use_baseline()
    atprogram("C:\\Users\\Dragos\\Dropbox\\RISE\\Git\\KalmanARM\\STDIO_Redirect_w_TrustZone", verbose=1)

# Step 2: Running baseline
dgi_t.start()
dgi_t.wait_main()

# Step 3: Obtaining csv of results and comparing with Intelx86 results
print("Copying output to '" + "\\output\\exp1\\exp1-kalman-output-" + output_filename_extension + ".csv'")
copy(os.getcwd() + "\\output\\output_arm.csv", os.getcwd() + "\\output\\exp1\\exp1-kalman-output-" + output_filename_extension + ".csv")

dgi_t.wait_plot()

