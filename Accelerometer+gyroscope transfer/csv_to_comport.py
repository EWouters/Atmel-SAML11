from time import sleep
import serial
import sys
import numpy as np
import matplotlib.pyplot as plt; plt.ion()

def sendline2(line):
    index = 0
    line = line.strip()
    length = len(line)

    while index < length - 1:
        to_send = line[index]
        ser.write(to_send.encode("utf-8"))
        index = index + 1

    ser.write('\n'.encode("utf-8"))   

with serial.Serial(port='COM3', baudrate=9600, dsrdtr=True, bytesize=8, parity='N', stopbits=1) as ser: 
   ser.setDTR(True)
   acc_file = open("input_acc.csv", "r")
   gyro_file = open("input_gyro.csv", "r")

   acc_file.readline()
   gyro_file.readline()

   stage = 0
   line = None

   x = []
   y = []

   for i in range (1000):
        line = ser.readline()
        line = str("".join(map(chr, line))).strip()
        #print("[RECV] " + line)

        if stage == 0: stage = 1
        elif stage == 1:
            x.append(float(line.split(",")[0]))
            y.append(float(line.split(",")[2]))
            print ("Drawing: " + str(x[i-1]) + "; " + str(y[i-1]))
            line_plot, = plt.plot(x,y, "b-")
            stage = 2
        elif stage == 2:
            x.append(float(line.split(",")[0]))
            y.append(float(line.split(",")[2]))
            print ("Drawing: " + str(x[i-1]) + "; " + str(y[i-1]))
            line_plot.set_data(x,y)
            line_plot.axes.relim()
            line_plot.axes.autoscale_view(True,True,True)

        
        plt.draw()

        send = acc_file.readline().strip() + "\0"
        #print("[SENDING] " + send)
        sendline2(send)
        #print("[SENT] " + send)

        send = gyro_file.readline().strip() + "\0"
        #print("[SENDING] " + send)
        sendline2(send)
        #print("[SENT] " + send)

        plt.pause(0.001)

   acc_file.close()
   gyro_file.close()
         
