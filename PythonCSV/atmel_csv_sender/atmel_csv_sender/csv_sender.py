import serial

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
