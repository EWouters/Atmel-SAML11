from pydgilib_extra import *
from dgilib_globals import *
from time import sleep

import numpy as np

import queue

config_dict = {
    "power_buffers": [{"channel": CHANNEL_A, "power_type": POWER_CURRENT}],
    "read_mode": [True, True, True, True],
    "write_mode": [False, False, False, False],
    "loggers": [LOGGER_OBJECT],
    "verbose": 0,
}

PAUSE_DURATION = 0.5

def energy_measurements_worker(queue1, queue2, division = config['division'], max_seconds = config['max_seconds'], pin_filter = config['pin_filter']):
    with DGILibExtra(**config_dict) as dgilib:
        for i in np.arange(0.0, max_seconds, division):
                        
            data = dgilib.logger(division)
            queue1.put(data)
            queue2.put(data)

            # with open("wtf.txt", "w") as f:
            #      f.write(str(data[INTERFACE_GPIO]))
