
from experiment.helpers import replace_define_value_in_file
import os

compile_base_dir = os.path.join(os.path.dirname(os.getcwd()),"KalmanARM")
hashtable_header_file_path = os.path.join(compile_base_dir, "STDIO_Redirect_w_TrustZone", "HashTable", "hashtable.h")
replace_define_value_in_file(hashtable_header_file_path, "HASHSIZE", "31")