
from pydgilib_extra import DGILibExtra, DGILibPlot
from atmel_csv_sender import sendline
from config import *
from time import time, sleep
from helpers import waitForStart, timeToStop
import serial
import sys

def dgilib_logger_worker(cmdQueue, measurement_duration = config["measurement_duration"], yield_rate = 0, queue1 = None, queue2 = None):
    
    with DGILibExtra(**dgilib_config_dict) as dgilib:
        #plot = DGILibPlot(**dgilib_config_dict)
        plot = dgilib.logger.plotobj
        keepItUp = True

        waitForStart(cmdQueue, "dgilib_logger_worker")
        dgilib.device_reset()
        
        dgilib.logger.start()
        
        end_time = time() + measurement_duration
        while time() < end_time:
                dgilib.logger.update_callback()
                #plot.update_plot(dgilib.data)

                #queue1.put(dgilib.data)
                #queue2.put(dgilib.data)
                sleep(yield_rate)

                if timeToStop(cmdQueue, "dgilib_logger_worker") or not(plot.plot_still_exists()):
                        keepItUp = False
                        end_time = 0
        
        dgilib.logger.stop()

        dgilib.logger.calculate_averages_for_pin(2)
        dgilib.logger.print_averages_for_pin(2)

        while keepItUp:
                if timeToStop(cmdQueue, "dgilib_logger_worker"):
                        keepItUp = False

                if plot.plot_still_exists():
                        plot.refresh_plot()
                else:
                        keepItUp = False

# def dgilib_plot_worker(queue):
#         plot = DGILibPlot(**dgilib_config_dict)

#         work = True
#         while work:
#                 data = queue.get()

#                 if type(data) == str:
#                         if data == "stop":
#                                 work = False
#                 else:
#                         plot.update_plot(data)

#         plot.keep_plot_alive()

def receive_worker(queue, max_iterations = 1000, output_file="output/output_arm.csv"):
    for i in range(max_iterations):
        outf = None
        if i == 0: outf = open(output_file, "w")
        else: outf = open(output_file, "a")
        data = queue.get()
        outf.write(",".join(data) + "\r\n")
        outf.close()

def send_worker(queue, cmdQueue, input_acc_file="input/input_acc.csv", input_gyro_file="input/input_gyro.csv", max_iterations = config["measurement_iterations"], verbose=1):
    with serial.Serial(port='COM3', baudrate=9600, dsrdtr=True, bytesize=8, parity='N', stopbits=1) as ser:
        
       waitForStart(cmdQueue, "send_worker")

       ser.setDTR(True)
       acc_file = open(input_acc_file, "r")
       gyro_file = open(input_gyro_file, "r")

       # Ignore first line
       acc_file.readline()
       gyro_file.readline()

       line = None

       for i in range(max_iterations):
            if verbose >= 1: sys.stdout.write("\rReading line " + str(i) + "/" + str(max_iterations))
            if verbose >= 1: sys.stdout.flush()

            line = ser.readline()
            line = str("".join(map(chr, line))).strip()
            if verbose == 2: print("[RECV] " + line)

            if not ("RDY" in line): queue.put(line.split(","))

            send = acc_file.readline().strip() + "\0"
            sendline(ser,send)
            if verbose == 2: print("[SENT] " + send)

            send = gyro_file.readline().strip() + "\0"
            sendline(ser,send)
            if verbose == 2: print("[SENT] " + send)

       acc_file.close()
       gyro_file.close()