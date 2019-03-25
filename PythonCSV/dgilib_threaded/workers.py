
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

def dgilib_logger_worker(cmdQueue, returnQueue, measurement_duration, dgilib_config_dict, yield_rate=0):

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
			sleep(yield_rate)

		if timeToStop(cmdQueue, "dgilib_logger_worker") or not(plot.plot_still_exists()):
			keepItUp = False
			end_time = 0

		dgilib.logger.stop()

		# averagesQueue.put(dgilib.logger.plotobj.preprocessed_averages_data)
		# averagesQueue.put(dgilib.data)

		returnQueue.put(dgilib.data)
		returnQueue.put(dgilib.logger.plotobj.preprocessed_averages_data)
		print("Sent measurement data and preprocessed averages data to main thread.")
		print("Measurement thread waiting for plot...")

		while keepItUp:
			if timeToStop(cmdQueue, "dgilib_logger_worker"):
				keepItUp = False

			if plot.plot_still_exists():
				plot.refresh_plot()
			else:
				keepItUp = False

		print("Measurement thread done!")
	
def dgilib_logger(measurement_duration, dgilib_config_dict, stopQueue, startQueue, waitForPlot = False):

	end_time_adjustment = 2

	with DGILibExtra(**dgilib_config_dict) as dgilib:
		if hasattr(dgilib.logger, 'plotobj'):
			plot = dgilib.logger.plotobj
		else:
			plot = None
			waitForPlot = False

		dgilib.device_reset()

		dgilib.logger.start()

		#startQueue.put("start")

		end_time = time() + measurement_duration
		while time() < end_time:
			#print("Doing {0} out of {1}".format(time(), end_time))
			dgilib.logger.update_callback()
			
			if timeToStop(stopQueue, "dgilib_logger (simple)"):
				print("Measurement thread: Got stop command!")
				end_time = time() + end_time_adjustment

		dgilib.logger.stop()

		if LOGGER_CSV in dgilib.logger.loggers:
			for interface_id, interface in dgilib.interfaces.items():
				print("Wrote " + interface.name + " data to " + os.path.join(dgilib.logger.log_folder, interface.file_name_base + '_' +
								interface.name + ".csv'"))

		if waitForPlot and (plot is not None):
			print("Measurement thread waiting for plot...")
			while plot.plot_still_exists():
				plot.refresh_plot()

		print("Measurement thread done!")

		if hasattr(dgilib.logger, 'plotobj'):
			return dgilib.data, dgilib.logger.plotobj.preprocessed_averages_data
		else:
			return dgilib.data

def receive_worker(queue, stopQueue, max_iterations, output_file):
	with open(output_file, "w") as f:
		for i in range(max_iterations):
			data = queue.get()
			f.write(",".join(data) + "\n")
		
		print("\n\nWritten Kalman output to '" + output_file + "'")
		print("\nReceiving thread done!")

	stopQueue.put("stop")

def send_worker(queue, cmdQueue, input_acc_file, input_gyro_file, max_iterations, verbose=1):
	max_iterations += 1
	
	with serial.Serial(port='COM3', baudrate=9600, dsrdtr=True, bytesize=8, parity='N', stopbits=1) as ser:

		#waitForCmd(cmdQueue, "start", "send_worker")

		ser.setDTR(True)
		acc_file = open(input_acc_file, "r")
		gyro_file = open(input_gyro_file, "r")

		# Ignore first line
		acc_file.readline()
		gyro_file.readline()

		line = None
		#hash = None

		for i in range(max_iterations):
			if verbose >= 1: sys.stdout.write( \
				"\rReading line " + str(i+1) + "/" + str(max_iterations))
			if verbose >= 1: sys.stdout.flush()

			line = ser.readline()
			line = str("".join(map(chr, line))).strip()
			if verbose == 2: print("[RECV] " + line)

			if ("Hash" in line):
				hash_ = line.split(":")[1]
				print("Hash is {0}".format(hash_))
			elif not ("RDY" in line): 
				queue.put(line.split(","))

			send = acc_file.readline().strip() + "\0"
			sendline(ser, send)
			if verbose == 2: print("[SENT] " + send)

			send = gyro_file.readline().strip() + "\0"
			sendline(ser, send)
			if verbose == 2: print("[SENT] " + send)
			
		# if hash is None:
		# 	typeQueue.put("baseline")
		# else:
		# 	typeQueue.put("hash-" + hash)

		acc_file.close()
		gyro_file.close()

		print("Sending thread done!")

