from time import sleep
import serial
import sys
import numpy
import queue
import matplotlib.pyplot as plt; plt.ion()

#plotting_or_outputting_csv = "output_csv" # options are: "output_csv" or "plot"

def sendline(ser, line, verbose = 1):
    prevline = ""
    while sendline_(ser, line, prevline, verbose) != 0: continue
    prevline = line

def sendline_(ser, line, prevline, verbose):
    sendline__(ser,line)
    
    recv = ser.readline()
    recv = str("".join(map(chr, recv))).strip().rstrip('\x00')

    line = line.strip().rstrip('\x00')

    if verbose == 2: print("[CORR] Received: " + recv)

    if (len(recv) != 0) or (not (recv is None)):
        if recv[0] == "b":
            sendline__(ser,prevline)
            if verbose == 2: print("[CORR] Recorrection requested by device. Sending: " + prevline)
            return -1
        elif recv[0] == "f":
            if verbose == 2: print("[CORR] Device is confused. Resending same data.")
            return -1
        elif recv == line:
            if verbose == 2: print("[CORR] OK string")
            sendline__(ser, "kkkkk")
            return 0
        else: # What was received is not equal to what was sent
            if verbose == 2: print("[CORR] Recorrection requested. Sending 'r'.")
            sendline__(ser,"rrrrr")
            return -1
    else:
        sendline(ser,"rrrrr")
        return -1


def sendline__(ser, line):
    index = 0
    line = line.strip()
    length = len(line)

    while index < length - 1:
        to_send = line[index]
        ser.write(to_send.encode("utf-8"))
        index = index + 1

    ser.write('\n'.encode("utf-8"))   

def csv_worker(queue, max_iterations = 1000, output_file="output_arm.csv"):

    for i in range(max_iterations):
        outf = None
        if i == 0: outf = open(output_file, "w")
        else: outf = open(output_file, "a")
        data = queue.get()
        outf.write(",".join(data))
        outf.close()

def plot_worker(queue, max_iterations = 1000, plot_width = 50):

    plot_max = 30
    plot_min = -30

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
        ydata.append(float(data[2]))

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

def kalman_worker(input_acc_file="input_acc.csv", input_gyro_file="input_gyro.csv", max_iterations = 1000, queue = None, verbose=1):
    
    with serial.Serial(port='COM3', baudrate=9600, dsrdtr=True, bytesize=8, parity='N', stopbits=1) as ser: 
       ser.setDTR(True)
       acc_file = open(input_acc_file, "r")
       gyro_file = open(input_gyro_file, "r")

       # Ignore first line
       acc_file.readline()
       gyro_file.readline()

       line = None

       #data = []

       for i in range(max_iterations):
            if verbose == 1: sys.stdout.write("\rReading line " + str(i) + "/" + str(max_iterations))
            if verbose == 1: sys.stdout.flush()

            line = ser.readline()
            line = str("".join(map(chr, line))).strip()
            if verbose == 2: print("[RECV] " + line)

            #data = data.append(line.split(","))

            if not ("RDY" in line): queue.put(line.split(","))

            # if stage == 0:
            #     stage = 1
            #     if plotting_or_outputting_csv == "output_csv":
            #         output_file = open("output_arm.csv", "w")
            # elif stage == 1 and plotting_or_outputting_csv == "plot":
            #     x.append(float(line.split(",")[0]))
            #     y.append(float(line.split(",")[2]))
            #     if verbose == 2: print ("Drawing: " + str(x[i-1]) + "; " + str(y[i-1]))
            #     line_plot, = plt.plot(x,y, "b-")
            #     plt.draw()
            #     stage = 2
            # elif stage == 2 and plotting_or_outputting_csv == "plot":
            #     x.append(float(line.split(",")[0]))
            #     y.append(float(line.split(",")[2]))
            #      if verbose == 2:  print ("Drawing: " + str(x[i-1]) + "; " + str(y[i-1]))
            #     line_plot.set_data(x,y)
            #     line_plot.axes.relim()
            #     line_plot.axes.autoscale_view(True,True,True)
            #     plt.draw()
            # elif stage > 0 and plotting_or_outputting_csv == "output_csv":
            #      if verbose == 2: print("Outputting: " + line)
            #     output_file.write(line + "\n")
            

            send = acc_file.readline().strip() + "\0"
            sendline(ser,send)
            if verbose == 2: print("[SENT] " + send)

            send = gyro_file.readline().strip() + "\0"
            sendline(ser,send)
            if verbose == 2: print("[SENT] " + send)

            #plt.pause(0.001)

       acc_file.close()
       gyro_file.close()
         
