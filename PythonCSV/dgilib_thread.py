from pydgilib_extra import *
from time import sleep
import numpy as np
import queue
import matplotlib.pyplot as plt; plt.ion()
from matplotlib.widgets import Slider, Button

config_dict = {
    "power_buffers": [{"channel": CHANNEL_A, "power_type": POWER_CURRENT}],
    "read_mode": [True, True, True, True],
    "write_mode": [False, False, False, False],
    "loggers": [LOGGER_OBJECT],
    "verbose": 0,
}

def energy_measurements_worker(queue, division = 5, max_seconds = 50, pin_filter = 3):
    with DGILibExtra(**config_dict) as dgilib:
        for i in np.arange(0.0, max_seconds, division):
                        
            data = dgilib.logger(division)
            queue.put(data)

            # with open("wtf.txt", "w") as f:
            #      f.write(str(data[INTERFACE_GPIO]))

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

def power_plot_worker(queue, division = 5, max_seconds = 50, plot_width = 5, plot_max = 0.005, plot_min = 0):
    xdata = []
    ydata = []

    fig = plt.figure()
    plt.subplots_adjust(bottom=0.25)

    plt.grid()
    plt.show()

    axes = plt.gca()
    axes.set_xlim(0, plot_width)
    axes.set_ylim(plot_min, plot_max)
    lplt, = axes.plot(xdata, ydata, 'r-')

    width = plot_width

    axcolor = 'lightgoldenrodyellow'
    axpos = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    axwidth = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])

    spos = Slider(axpos, 'Position', 0, max_seconds-width, valinit=0, valstep=0.5)
    swidth = Slider(axwidth, 'Width', 0, max_seconds, valinit=plot_width, valstep=0.5)
    
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

    def update(val):
        pos = spos.val
        width = swidth.val

        if pos > (max_seconds - width):
            pos = max_seconds - width

        axpos.clear()
        spos.__init__(axpos, 'Position', 0, max_seconds-width, valinit=pos, valstep=0.5)
        spos.on_changed(update)

        axes.axis([pos,pos+width,plot_min,plot_max])

        visible_average = calculate_average_midpoint_multiple_intervals([xdata,ydata], all_hold_times, i, i+width) * 1000
        all_average = calculate_average_midpoint_multiple_intervals([xdata,ydata], all_hold_times, min(xdata), max(xdata)) * 1000

        axes.set_title("Visible average: %.6f mA;\n Total average: %.6f mA." % (visible_average, all_average))

        fig.canvas.draw_idle()

    spos.on_changed(update)
    swidth.on_changed(update)

    def reset(event):
        swidth.reset()
        spos.__init__(axpos, 'Position', 0, max_seconds-plot_width, valinit=0, valstep=0.5)
        spos.on_changed(update)
        spos.reset()

        axes.set_title(f"Visible average: {visible_average} mA; Total average: {all_average} mA.")
        
    button.on_clicked(reset)

    all_hold_times = []

    i = 0.0
    # for i in np.arange(0.0, max_seconds, division):
    while i < max_seconds:
        if not plt.fignum_exists(fig.number): break

        if queue.empty(): 
            plt.pause(0.1)
            continue

        data = queue.get()

        for j in range(len(data[INTERFACE_POWER][0]))[1:]:
            xdata.append(i + data[INTERFACE_POWER][0][j])
            ydata.append(data[INTERFACE_POWER][1][j])

        for hold_times in identify_hold_times(data, True, 2, correction_forward=0.0005, shrink=0.0010):
            axes.axvspan(i+hold_times[0], i+hold_times[1], color='green', alpha=0.5)
            all_hold_times.append((i+hold_times[0], i+hold_times[1]))

        lplt.set_xdata(xdata)
        lplt.set_ydata(ydata)

        if spos.val == i - width:
            axes.axis([i,i+width,plot_min,plot_max])
            spos.set_val(i)

        visible_average = calculate_average_midpoint_multiple_intervals([xdata,ydata], all_hold_times, i, i+width) * 1000
        all_average = calculate_average_midpoint_multiple_intervals([xdata,ydata], all_hold_times, min(xdata), max(xdata)) * 1000

        axes.set_title("Visible average: %.6f mA;\n Total average: %.6f mA." % (visible_average, all_average))

        plt.draw()
        plt.pause(0.1)
        i = i + division

    while plt.fignum_exists(fig.number):
        plt.pause(0.1)
