import sys
import threading
import queue

import serial
from atmel_csv_sender import *

from dgilib_threaded.workers import *

##########
# Queues #
##########
send_receive_queue = queue.Queue()
logger_stop_queue = queue.Queue()
sender_start_queue = queue.Queue()
#logger_main_queue = queue.Queue()

dgilib_logger_thread = None
sender_thread = None
receiver_thread = None

########
# Main #
########
def measure(duration, iterations, dgilib_config_dict, input_acc_file, input_gyro_file, output_file, waitForPlot=False, verbose=2):
    global dgilib_logger_thread
    global sender_thread
    global receiver_thread

    sender_thread = threading.Thread(target=send_worker,
        kwargs={'queue': send_receive_queue,
        'cmdQueue': sender_start_queue,
        'max_iterations': iterations,
        'input_acc_file': input_acc_file,
        'input_gyro_file': input_gyro_file,
        'verbose': verbose
        })
    receiver_thread = threading.Thread(target=receive_worker,
        kwargs={'queue': send_receive_queue,
        'stopQueue': logger_stop_queue,
        'max_iterations': iterations,
        'output_file': output_file,
        'verbose': verbose
        })
    
    sender_thread.start()
    receiver_thread.start()

    data, preprocessed_data = dgilib_logger(duration, dgilib_config_dict, logger_stop_queue, sender_start_queue, waitForPlot, verbose)

    sender_thread.join()
    receiver_thread.join()

    return data, preprocessed_data





