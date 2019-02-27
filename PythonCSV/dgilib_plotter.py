from pydgilib_extra import *
from dgilib_helpers import *
from dgilib_globals import *

import queue

import matplotlib.pyplot as plt; plt.ion()
from matplotlib.widgets import Slider, Button

from dgilib_globals import *

def power_plot_worker(queue, division = config['division'], max_seconds = config['max_seconds'], plot_width = config['plot_width'], plot_max = config['plot_max'], plot_min = config['plot_min']):
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

        visible_average = calculate_average_midpoint_multiple_intervals([xdata,ydata], all_hold_times, i, i+width) * 1000
        all_average = calculate_average_midpoint_multiple_intervals([xdata,ydata], all_hold_times, min(xdata), max(xdata)) * 1000

        axes.set_title("Visible average: %.6f mA;\n Total average: %.6f mA." % (visible_average, all_average))
        
    button.on_clicked(reset)

    all_hold_times = []
    all_hold_times_sum = 0.00

    i = 0.0
    # for i in np.arange(0.0, max_seconds, division):
    while i < max_seconds:
        if not plt.fignum_exists(fig.number): break

        if queue.empty(): 
            plt.pause(PAUSE_DURATION)
            continue

        data = queue.get()

        for j in range(len(data[INTERFACE_POWER][0]))[1:]:
            xdata.append(i + data[INTERFACE_POWER][0][j])
            ydata.append(data[INTERFACE_POWER][1][j])

        for hold_times in identify_hold_times(data, config['listen_to_pin_value'], 2, correction_forward = config['correction_forward'], shrink = config['shrink']):
            axes.axvspan(i+hold_times[0], i+hold_times[1], color='green', alpha=0.5)
            all_hold_times.append((i+hold_times[0], i+hold_times[1]))
            all_hold_times_sum += hold_times[1] - hold_times[0]

        lplt.set_xdata(xdata)
        lplt.set_ydata(ydata)

        if spos.val == i - width:
            axes.axis([i,i+width,plot_min,plot_max])
            spos.set_val(i)

        visible_average = calculate_average_midpoint_multiple_intervals([xdata,ydata], all_hold_times, i, i+width) * 1000
        all_average = calculate_average_midpoint_multiple_intervals([xdata,ydata], all_hold_times, min(xdata), max(xdata)) * 1000

        axes.set_title("Visible average: %.6f mA;\n Total average: %.6f mA; \n Total time: %.6f s." % (visible_average, all_average, all_hold_times_sum))

        plt.draw()
        plt.pause(PAUSE_DURATION)
        i = i + division

    while plt.fignum_exists(fig.number):
        plt.pause(PAUSE_DURATION)
