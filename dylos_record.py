#This program collects amd stores serial data from the Dylos DC1100 Sensor
#in CSV format until a given date of the month is reached.
#For use on a Raspberry Pi.

#Author: Iarla Scaife

import csv
import serial
import time
import datetime
import os
import sys

#Serial port init. 9600 Baud, 8bits, one stopbit, no parity, infinite timeout
#Note: Serial port may also be "/dev/ttyUSB1" sometimes rather than "/dev/ttyUSB0"
port =serial.Serial(
    "/dev/ttyUSB0",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    writeTimeout = 0,
    timeout = 10,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False)

dateno = 0

#the program will terminate when this date of the month is reached
stopBeforeDate = "30"

#Open file.
with open ('dylos.csv','ab',newline=None) as csvfile:
    
     while dateno != stopBeforeDate:
         input=port.read(1)
         print("Data Received")
         #If carriage return detected, write a timestamp to the file...
         if input.decode('utf8') == "\r":
                print("<CR> detected")
                csvfile.write(",".encode())
                csvfile.write(time.strftime("%X").encode())
                csvfile.write(",".encode())
                csvfile.write(time.strftime("%x").encode())
                print("Date: ", time.strftime("%c"))
                csvfile.write(input)
         #...otherwise, just write the data to the file
         else:
                print("Regular byte detected")
                csvfile.write(input)
         #flush buffer and sync file so that unexpected termination won't corrupt data
         csvfile.flush()
         os.fsync(csvfile)
         #Update date of month variable
         dateno = time.strftime("%d")
         print(dateno)
