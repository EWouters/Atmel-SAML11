import queue

def waitForCmd(cmdQueue, cmd="start", function_name=""):
    msg = cmdQueue.get()
    if (msg == cmd):
        return  # Start
    else:
        if function_name != "":
            raise ValueError(
                function_name + ": Unknown command received on queue")
        else:
            raise ValueError("Unknown command received on queue")


def timeToStop(cmdQueue, function_name=""):
    try:
        msg = cmdQueue.get(block=True, timeout=0.0001)
        if (msg == "stop"):
            return True
    except queue.Empty:
        pass
    return False
