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
logger_start_stop_queue = queue.Queue()
sender_start_stop_queue = queue.Queue()
logger_main_queue = queue.Queue()

dgilib_logger_thread = None
sender_thread = None
receive_thread = None

config = {
    "input_acc_file": "input/input_acc.csv",
    "input_gyro_file": "input/input_gyro.csv",
    "output_file": "output/output_arm.csv",
    "measurement_duration": 5,
    "measurement_iterations": 3
}

########
# Main #
########
def start(duration=config["measurement_duration"]):
    dgilib_logger_thread = threading.Thread(target=dgilib_logger_worker,
        kwargs={'cmdQueue': logger_start_stop_queue,
        'returnQueue': logger_main_queue,
        'measurement_duration': duration
        })
    sender_thread = threading.Thread(target=send_worker,
        kwargs={'queue': send_receive_queue,
        'cmdQueue': sender_start_stop_queue
        })
    receive_thread = threading.Thread(target=receive_worker,
        kwargs={'queue': send_receive_queue
        })
    # averages_thread = threading.Thread(target=dgilib_averages_worker,
    #     kwargs={'queue': logger_averages_queue,
    #     'typeQueue': sender_averages_queue
    #     })
    
    dgilib_logger_thread.start()
    sender_thread.start()
    receive_thread.start()
    # averages_thread.start()

    logger_start_stop_queue.put("start")
    sender_start_stop_queue.put("start")

    data = logger_main_queue.get()
    preprocessed_data = logger_main_queue.get()

    return (data, preprocessed_data)

################
# Threads stop #
################
def wait_dgilib():
    dgilib_logger_thread.join()
    
def wait_sendrecv():
    sender_thread.join()
    receive_thread.join()






