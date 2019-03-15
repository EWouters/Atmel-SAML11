
import serial
import sys

def output_worker(queue, max_iterations = 1000, output_file="output_arm.csv"):
    for i in range(max_iterations):
        outf = None
        if i == 0: outf = open(output_file, "w")
        else: outf = open(output_file, "a")
        data = queue.get()
        outf.write(",".join(data))
        outf.close()

def input_worker(queue, input_acc_file="input/input_acc.csv", input_gyro_file="input/input_gyro.csv", max_iterations = 1000, verbose=1):
    
    with serial.Serial(port='COM3', baudrate=9600, dsrdtr=True, bytesize=8, parity='N', stopbits=1) as ser: 
       ser.setDTR(True)
       acc_file = open(input_acc_file, "r")
       gyro_file = open(input_gyro_file, "r")

       # Ignore first line
       acc_file.readline()
       gyro_file.readline()

       line = None

       for i in range(max_iterations):
            if verbose == 1: sys.stdout.write("\rReading line " + str(i) + "/" + str(max_iterations))
            if verbose == 1: sys.stdout.flush()

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