import queue

from pydgilib_extra import DGILibAverages

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
    if not(cmdQueue.empty()):
        msg = cmdQueue.get()
        if (msg == "stop"):
                return True
        else:
                if function_name != "":
                    raise ValueError(function_name + ": Unknown command received by dgilib_logger_worker")
                else:
                    raise ValueError("Unknown command received by dgilib_logger_worker")
    return False

def do_averages(data, preprocessed_data, write_to_file):
	avg = DGILibAverages(preprocessed_data = preprocessed_data)

	print("Calculating averages...")

	avg.calculate_averages_for_pin(2, data = data)
	avg.write_to_csv(write_to_file)