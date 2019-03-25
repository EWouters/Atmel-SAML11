import queue
import os

from pydgilib_extra import DGILibAverages, DGILibPlot, LOGGER_OBJECT, DGILibExtra, LoggerData

def waitForCmd(cmdQueue, cmd="start", function_name = ""):
    msg = cmdQueue.get()
    if (msg == cmd):
            return # Start
    else:
        if function_name != "":
            raise ValueError(function_name + ": Unknown command received on queue")
        else:
            raise ValueError("Unknown command received on queue")

def timeToStop(cmdQueue, function_name = ""):
    try:
        msg = cmdQueue.get(block=True, timeout=0.0001)
        if (msg == "stop"):
                return True
    except queue.Empty:
        pass
    # else:
    #         if function_name != "":
    #             raise ValueError(function_name + ": Unknown command received by dgilib_logger_worker")
    #         else:
    #             raise ValueError("Unknown command received by dgilib_logger_worker")
    return False

def do_averages(data, preprocessed_data, write_to_file):
	avg = DGILibAverages(data = data, preprocessed_data = preprocessed_data)

	print("Calculating averages...")

	avg.calculate_averages_for_pin(2)
	avg.write_to_csv(write_to_file)

def show_plot_for_data(data):
    config_dict_plot = {
        "loggers": [LOGGER_OBJECT],
        "plot_pins_method": "highlight"
    }

    with DGILibExtra(**config_dict_plot) as dgilib:

        logger_data = LoggerData()
        for interface_id, interface in dgilib.interfaces.items():
            logger_data[interface_id] += interface.csv_read_file(
                os.path.join(dgilib.logger.log_folder,
                            (interface.file_name_base + '_' +
                            interface.name + ".csv")))
        
        plot = DGILibPlot(config_dict_plot)

        plot.update_plot(logger_data)

        plot.keep_plot_alive()

def show_plot_for_csv(log_folder, file_name_base):
    config_dict_plot = {
        "loggers": [LOGGER_OBJECT],
        "plot_pins_method": "highlight",
        "log_folder": log_folder,
        "file_name_base": file_name_base
    }

    with DGILibExtra(**config_dict_plot) as dgilib:

        logger_data = LoggerData()
        for interface_id, interface in dgilib.interfaces.items():
            logger_data[interface_id] += interface.csv_read_file(
                os.path.join(dgilib.logger.log_folder,
                             (interface.file_name_base + '_' +
                             interface.name + ".csv")))
        
        plot = DGILibPlot(config_dict_plot)

        plot.update_plot(logger_data)

        # dgilib.logger.calculate_averages_for_pin(2)
        # dgilib.logger.print_averages_for_pin(2)

        plot.keep_plot_alive()
    
    return logger_data

def load_from_csv(log_folder, file_name_base, showPlot = False):
    config_dict_plot = {
        "loggers": [LOGGER_OBJECT],
        "plot_pins_method": "highlight",
        "log_folder": log_folder,
        "file_name_base": file_name_base
    }

    with DGILibExtra(**config_dict_plot) as dgilib:

        logger_data = LoggerData()
        for interface_id, interface in dgilib.interfaces.items():
            logger_data[interface_id] += interface.csv_read_file(
                os.path.join(dgilib.logger.log_folder,
                             (interface.file_name_base + '_' +
                             interface.name + ".csv")))
        
        if showPlot:
            plot = DGILibPlot(config_dict_plot)

            plot.update_plot(logger_data)

            plot.keep_plot_alive()
    
    return logger_data