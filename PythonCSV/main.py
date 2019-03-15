import sys
import threading
import queue

import serial
from atmel_csv_sender import *
from workers import *

##########
# Queues #
##########
send_receive_queue = queue.Queue()
#power_data_queue = queue.Queue()
q3 = queue.Queue()

logger_start_stop_queue = queue.Queue()
sender_start_stop_queue = queue.Queue()

####################################
# Threads initialization and start #
####################################
dgilib_logger_thread = threading.Thread(target=dgilib_logger_worker, kwargs={'cmdQueue': logger_start_stop_queue})
sender_thread = threading.Thread(target=send_worker, kwargs={'queue': send_receive_queue, 'cmdQueue': sender_start_stop_queue})
receive_thread = threading.Thread(target=receive_worker, kwargs={'queue': send_receive_queue})

dgilib_logger_thread.start()
sender_thread.start()
receive_thread.start()


########
# Main #
########
logger_start_stop_queue.put("start")
sender_start_stop_queue.put("start")
send_receive_queue.put("start")


################
# Threads stop #
################
dgilib_logger_thread.join()
sender_thread.join()
receive_thread.join()

