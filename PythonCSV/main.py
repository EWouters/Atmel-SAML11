import sys
import threading
import queue

import serial
from atmel_csv_sender import *


q = queue.Queue()
q2 = queue.Queue()
q3 = queue.Queue()

kalmanThread = threading.Thread(target=kalman_worker, kwargs={'queue': q})
csvThread = threading.Thread(target=csv_worker, kwargs={'queue': q})
#plotThread = threading.Thread(target=plot_worker, kwargs={'queue': q})

powerThread = threading.Thread(target=energy_measurements_worker, kwargs={'queue1': q2, 'queue2': q3})
powerPlotThread = threading.Thread(target=power_plot_worker, kwargs={'queue': q2})
powerCsvThread = threading.Thread(target=power_csv_worker, kwargs={'queue': q3})

#plotThread.start()
csvThread.start()
kalmanThread.start()
powerThread.start()
powerPlotThread.start()
powerCsvThread.start()

csvThread.join()
kalmanThread.join()
#plotThread.join()
powerThread.join()
powerPlotThread.join()
powerCsvThread.join()
