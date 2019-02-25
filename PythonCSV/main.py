import threading
import queue
from serial_csv import *
from dgilib_thread import *

q = queue.Queue()
q2 = queue.Queue()

kalmanThread = threading.Thread(target=kalman_worker, kwargs={'queue': q})
#csvThread = threading.Thread(target=csv_worker, kwargs={'queue': q})
#plotThread = threading.Thread(target=plot_worker, kwargs={'queue': q})

powerThread = threading.Thread(target=energy_measurements_worker, kwargs={'queue': q2})
powerPlotThread = threading.Thread(target=power_plot_worker, kwargs={'queue': q2})

#plotThread.start()
#csvThread.start()
kalmanThread.start()
powerThread.start()
powerPlotThread.start()

#csvThread.join()
kalmanThread.join()
#plotThread.join()
powerThread.join()
powerPlotThread.join()
