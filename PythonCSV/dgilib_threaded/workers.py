
from pydgilib_extra import DGILibExtra, DGILibPlot, DGILibAverages
from atmel_csv_sender import sendline

from dgilib_threaded.config import *
from dgilib_threaded.helpers import waitForCmd, timeToStop

from pydgilib_extra import power_and_time_per_pulse

import serial
import sys
from time import time, sleep
from shutil import copy
import os

def dgilib_averages_worker(queue, typeQueue):
	preprocessed_data = queue.get()
	data = queue.get()

	avg = DGILibAverages(None, preprocessed_data = preprocessed_data)
	print("Calculating averages...")
	start_time = time()
	avg.calculate_averages_for_pin(2, data = data)
	duration = start_time - time()
	print("Time spent on calculate_averages_for_pin: {0} s", duration)
	avg.print_averages_for_pin(2)

	print(data)

	start_time = time()
	power_and_time_per_pulse(data, 2, 0.01, data.power.timestamps[-1]-1, pulse_direction=False)
	duration = start_time - time()
	print("Time spent on power_and_time_per_pulse: {0} s", duration)

	hash_ = typeQueue.get()
	avg.write_to_csv(os.getcwd() + "\\output\\exp1\\exp1-averages-" + hash_ + ".csv")
	
	

def dgilib_logger_worker(cmdQueue, averagesQueue, measurement_duration=config["measurement_duration"], yield_rate=0):

	with DGILibExtra(**dgilib_config_dict) as dgilib:
		# plot = DGILibPlot(**dgilib_config_dict)
		plot = dgilib.logger.plotobj
		keepItUp = True

		waitForCmd(cmdQueue, "start", "dgilib_logger_worker")
		dgilib.device_reset()

		dgilib.logger.start()
		#dgilib.logger.log()

		end_time = time() + measurement_duration
		while time() < end_time:
			dgilib.logger.update_callback()
			# plot.update_plot(dgilib.data)

			# queue1.put(dgilib.data)
			# queue2.put(dgilib.data)
			sleep(yield_rate)

		if timeToStop(cmdQueue, "dgilib_logger_worker") or not(plot.plot_still_exists()):
			keepItUp = False
			end_time = 0

		dgilib.logger.stop()

		averagesQueue.put(dgilib.logger.plotobj.preprocessed_averages_data)
		averagesQueue.put(dgilib.data)

		while keepItUp:
			if timeToStop(cmdQueue, "dgilib_logger_worker"):
				keepItUp = False

			if plot.plot_still_exists():
				plot.refresh_plot()
			else:
				keepItUp = False

def receive_worker(queue, max_iterations=config["measurement_iterations"], output_file=config["output_file"]):
	with open(output_file, "w") as f:
		for i in range(max_iterations):
			data = queue.get()
			f.write(",".join(data) + "\n")
		
		print("Written Kalman output to CSV")


def send_worker(queue, cmdQueue, typeQueue, input_acc_file=config["input_acc_file"], input_gyro_file=config["input_gyro_file"], max_iterations=config["measurement_iterations"] + 1, verbose=1):
	with serial.Serial(port='COM3', baudrate=9600, dsrdtr=True, bytesize=8, parity='N', stopbits=1) as ser:

		waitForCmd(cmdQueue, "start", "send_worker")

		ser.setDTR(True)
		acc_file = open(input_acc_file, "r")
		gyro_file = open(input_gyro_file, "r")

		# Ignore first line
		acc_file.readline()
		gyro_file.readline()

		line = None
		hash = None

		for i in range(max_iterations):
			if verbose >= 1: sys.stdout.write( \
				"\rReading line " + str(i+1) + "/" + str(max_iterations))
			if verbose >= 1: sys.stdout.flush()

			line = ser.readline()
			line = str("".join(map(chr, line))).strip()
			if verbose == 2: print("[RECV] " + line)

			if ("Hash" in line):
				hash = line.split(":")[1]
				print("Hash is {0}".format(hash))
			elif not ("RDY" in line): 
				queue.put(line.split(","))

			send = acc_file.readline().strip() + "\0"
			sendline(ser, send)
			if verbose == 2: print("[SENT] " + send)

			send = gyro_file.readline().strip() + "\0"
			sendline(ser, send)
			if verbose == 2: print("[SENT] " + send)
			
		if hash is None:
			typeQueue.put("baseline")
		else:
			typeQueue.put("hash-" + hash)

		acc_file.close()
		gyro_file.close()

		print("\r\nDone!")
