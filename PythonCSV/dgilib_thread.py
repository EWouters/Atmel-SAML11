from pydgilib_extra import *
from time import sleep

config_dict = {
    "power_buffers": [{"channel": CHANNEL_A, "power_type": POWER_CURRENT}],
    "read_mode": [True, True, True, True],
    "write_mode": [False, False, False, False],
    "loggers": [LOGGER_CSV, LOGGER_OBJECT],
    "verbose": 0,
}

def energy_measurements_worker(queue, max_seconds=300, pin_filter = 3):
	division = 1

	with DGILibExtra(**config_dict) as dgilib:
		for i in range(max_seconds/division):
			data = dgilib.logger(division)

			q.put(data[INTERFACE_POWER])

def power_plot_worker(queue, plot_width = 50):
    plot_max = 1
    plot_min = -1

    xdata = [0]
    ydata = [0]

    fig1 = plt.figure()

    plt.grid()
    plt.show()

    axes = plt.gca()
    axes.set_xlim(0, plot_width)
    axes.set_ylim(plot_min, plot_max)
    lplt, = axes.plot(xdata, ydata, 'r-')

    for i in range(max_iterations):
        if not plt.fignum_exists(fig1.number): break

        data = queue.get()

        xdata.append(int(data[0]))
        ydata.append(float(data[1]))

        # Weirdly, if we want the width of the plot to be plot_width,
        # we need to check if xdata is bigger than HALF of the plot_width
        if (len(xdata) > plot_width/2):
            del xdata[0]
            del ydata[0]

        axes.set_xlim(min(xdata), max(plot_width, max(xdata)))
        axes.set_ylim(min(plot_min,min(ydata)), max(plot_max, max(ydata)))

        lplt.set_xdata(xdata)
        lplt.set_ydata(ydata)

        plt.draw()
        plt.pause(0.1)

    while plt.fignum_exists(fig1.number):
        plt.pause(0.001)