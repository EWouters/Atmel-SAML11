from dgilib_helpers import *
from dgilib_globals import *

import queue


def power_csv_worker(queue, division = config['division'], max_seconds = config['max_seconds'], output_file = config['output_file']):
    xdata = []
    ydata = []

    i = 0.0
    # for i in np.arange(0.0, max_seconds, division):

    with (open(output_file, "w")) as f: 
        while i < max_seconds:
            data = queue.get()

            for j in range(len(data[INTERFACE_POWER][0]))[1:]:
                xdata.append(i + data[INTERFACE_POWER][0][j])
                ydata.append(data[INTERFACE_POWER][1][j])

            for hold_times in identify_hold_times(data, config['listen_to_pin_value'], 2, correction_forward = config['correction_forward'], shrink = config['shrink']):
                #print(str(hold_times[0]))
                average = calculate_average_midpoint_multiple_intervals([xdata,ydata], hold_times, i+hold_times[0], i+hold_times[1]) * 1000

                f.write(",".join(i+hold_times[0], i+hold_times[1], hold_times[1]-hold_times[0], average))


            i = i + division
