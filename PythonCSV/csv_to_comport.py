from time import sleep
import serial
import sys
import numpy as np
import matplotlib.pyplot as plt; plt.ion()

plotting_or_outputting_csv = "output_csv" # options are: "output_csv" or "plot"
prevline = ""

def sendline_(ser, line, prevline):
    sendline2(ser,line)
    
    recv = ser.readline()
    recv = str("".join(map(chr, recv))).strip().rstrip('\x00')

    line = line.strip().rstrip('\x00')

    print("[CORR] Received: " + recv)

    if (len(recv) != 0) or (not (recv is None)):
        if recv[0] == "b":
            sendline2(ser,prevline)
            print("[CORR] Recorrection requested by device. Sending: " + prevline)
            return -1
        elif recv[0] == "f":
            print("[CORR] Device is confused. Resending same data.")
            return -1
        elif recv == line:
            print("[CORR] OK string")
            sendline2(ser, "kkkkk")
            return 0
        else: # What was received is not equal to what was sent
            print("[CORR] Recorrection requested. Sending 'r'.")
            sendline2(ser,"rrrrr")
            return -1
    else:
        sendline(ser,"rrrrr")
        return -1
        
def sendline(ser, line):
    global prevline
    while sendline_(ser, line, prevline) != 0: continue
    prevline = line

def sendline2(ser, line):
    index = 0
    line = line.strip()
    length = len(line)

    while index < length - 1:
        to_send = line[index]
        ser.write(to_send.encode("utf-8"))
        sleep(0.001)
        index = index + 1

    ser.write('\n'.encode("utf-8"))   

with serial.Serial(port='COM3', baudrate=9600, dsrdtr=True, bytesize=8, parity='N', stopbits=1) as ser: 
   ser.setDTR(True)
   acc_file = open("input_acc.csv", "r")
   gyro_file = open("input_gyro.csv", "r")
   output_file = None

   acc_file.readline()
   gyro_file.readline()

   stage = 0
   line = None

   x = []
   y = []

   for i in range (3):
        line = ser.readline()
        line = str("".join(map(chr, line))).strip()
        print("[RECV] " + line)

        if stage == 0:
            stage = 1
            if plotting_or_outputting_csv == "output_csv":
                output_file = open("output.csv", "w")
                #print("Outputting: " + line)
                #output_file.write(line + "\r\n")
        elif stage == 1 and plotting_or_outputting_csv == "plot":
            x.append(float(line.split(",")[0]))
            y.append(float(line.split(",")[2]))
            print ("Drawing: " + str(x[i-1]) + "; " + str(y[i-1]))
            line_plot, = plt.plot(x,y, "b-")
            plt.draw()
            stage = 2
        elif stage == 2 and plotting_or_outputting_csv == "plot":
            x.append(float(line.split(",")[0]))
            y.append(float(line.split(",")[2]))
            print ("Drawing: " + str(x[i-1]) + "; " + str(y[i-1]))
            line_plot.set_data(x,y)
            line_plot.axes.relim()
            line_plot.axes.autoscale_view(True,True,True)
            plt.draw()
        elif stage > 0 and plotting_or_outputting_csv == "output_csv":
            print("Outputting: " + line)
            output_file.write(line + "\n")
        

        send = acc_file.readline().strip() + "\0"
        #print("[SENDING] " + send)
        sendline(ser,send)
        print("[SENT] " + send)

##        line = ser.readline()
##        line = str("".join(map(chr, line))).strip()
##        print("[RECV] " + line)

        send = gyro_file.readline().strip() + "\0"
        #print("[SENDING] " + send)
        sendline(ser,send)
        print("[SENT] " + send)

##        line = ser.readline()
##        line = str("".join(map(chr, line))).strip()
##        print("[RECV] " + line)

        plt.pause(0.001)

   acc_file.close()
   gyro_file.close()
         
