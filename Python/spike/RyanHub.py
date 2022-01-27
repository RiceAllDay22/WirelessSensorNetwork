import sys
import time
import serial
import datetime
import pytz

ser = serial.Serial('COM4', 9600, timeout=1)
ser.flushInput()





#LOOP
try:
    while 1:
        wait = ser.inWaiting()
        if wait > 0:
            data = ser.readline().decode('utf-8').strip('\n').strip('\r')
            if data:
                print(data)
        else:
            time.sleep(0.1)



finally:
    print('Close the File')

