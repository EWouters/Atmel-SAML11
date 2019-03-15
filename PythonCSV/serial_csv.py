from time import sleep
import serial
import sys
import queue

def csv_worker(queue, max_iterations = 1000, output_file="output_arm.csv"):

    for i in range(max_iterations):
        outf = None
        if i == 0: outf = open(output_file, "w")
        else: outf = open(output_file, "a")
        data = queue.get()
        outf.write(",".join(data))
        outf.close()
