
import dgilib_threaded as dgi_t
from atprogram.atprogram import atprogram
from shutil import copy
import os

def use_baseline():
    base_dir = "C:\\Users\\Dragos\\Dropbox\\RISE\\Git\\KalmanARM"
    copy(base_dir + "\\main_baseline.c", base_dir + "\\STDIO_Redirect_w_TrustZone\\main.c")

def use_hash():
    base_dir = "C:\\Users\\Dragos\\Dropbox\\RISE\\Git\\KalmanARM"
    copy(base_dir + "\\main_hash.c", base_dir + "\\STDIO_Redirect_w_TrustZone\\main.c")


# Step 1: Compiling baseline
use_hash()
atprogram("C:\\Users\\Dragos\\Dropbox\\RISE\\Git\\KalmanARM\\STDIO_Redirect_w_TrustZone", verbose=1)

# Step 2: Running baseline
dgi_t.start()
dgi_t.wait()

# Step 3: Obtaining csv of results and comparing with Intelx86 results
copy(os.getcwd() + "\\output\\output_arm.csv", os.getcwd() + "\\exp1-output.csv")
