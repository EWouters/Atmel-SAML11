import queue

def waitForStart(cmdQueue, function_name = ""):
    msg = cmdQueue.get()
    if (msg == "start"):
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