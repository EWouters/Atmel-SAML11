from pydgilib_extra import *
from dgilib_globals import *

import queue

config_dict = {
    "power_buffers": [{"channel": CHANNEL_A, "power_type": POWER_CURRENT}],
    "read_mode": [True, True, True, True],
    "write_mode": [False, False, False, False],
    "loggers": [LOGGER_OBJECT],
    "verbose": 0,
}

def identify_hold_times(whole_data, true_false, pin, correction_forward = 0.00, shrink = 0.00):
    data = whole_data[INTERFACE_GPIO]
    hold_times = []
    start = data[0][0]
    end = data[0][0]
    in_hold = true_false
    not_in_hold = not true_false
    search = not true_false

    interval_sizes = []

    for i in range(len(data[0])):
        if search == not_in_hold: # Searching for start of hold time 
            if data[1][i][pin] == search:
                start = data[0][i]
            else:
                end = data[0][i]
                search = not search

        if search == in_hold: # Searching for end of hold time
            if data[1][i][pin] == search:
                end = data[0][i]
            else:
                search = not search
                to_add = (start+correction_forward+shrink,end+correction_forward-shrink)
                if ((to_add[0] != to_add[1]) and (to_add[0] < to_add[1])):
                    hold_times.append(to_add)
                    interval_sizes.append(to_add[1] - to_add[0])
                start = data[0][i]

    should_add_last_interval = True
    for ht in hold_times:
        if (ht[0] == start): should_add_last_interval = False

    if should_add_last_interval:

        invented_end_time = whole_data[INTERFACE_POWER][0][-1]+correction_forward-shrink

        # This function ASSUMES that the intervals are about the same in size.
        # ... If the last interval that should be highlighted on the graph is
        # ... abnormally higher than the maximum of the ones that already happened 
        # ... correctly then cancel highlighting with the help of 'invented_end_time' 
        # ... and highlight using the minimum from the 'interval_sizes' list, to get
        # ... an average that is most likely unaffected by stuff happening at the end
        # ... of the interval, which the power interface from the board failed to
        # ... communicate to us.
        if ((invented_end_time - start) > max(interval_sizes)):
            invented_end_time = start + min(interval_sizes)

        to_add = (start+correction_forward+shrink,invented_end_time)

        if ((to_add[0] != to_add[1]) and (to_add[0] < to_add[1])):
            hold_times.append(to_add)

    return hold_times

def calculate_average_midpoint_single_interval(power_data, start_time = None, end_time = None):
    # Calculate average value using midpoint Riemann sum
    sum = 0
 
    actual_start_time = -1
    actual_end_time = -1
 
    for i in range(len(power_data[0]) - 1)[1:]:
        first_current_value = power_data[1][i]
        second_current_value = power_data[1][i+1]
        timestamp = power_data[0][i+1]
        last_time = power_data[0][i]
 
        if ((last_time >= start_time) and (last_time < end_time)):
            sum += ((first_current_value + second_current_value)/2) * (timestamp - last_time)
 
            # We have to select the actual start time and the actual 
            if (actual_start_time == -1): actual_start_time = power_data[0][i]
 
        if (timestamp >= end_time):
            actual_end_time = power_data[0][i-1]
            break
 
    return sum / (actual_end_time - actual_start_time)   

def calculate_average_midpoint_multiple_intervals(power_data, intervals, start_time = None, end_time = None):
    # Calculate average value using midpoint Riemann sum
    sum = 0
    to_divide = 0

    for intv in intervals:
        if ((intv[0] >= start_time) and (intv[0] <= end_time) and (intv[1] >= start_time) and (intv[1] <= end_time)):
            sum += calculate_average_midpoint_single_interval(power_data, intv[0], intv[1])
            to_divide += 1

    return sum / to_divide