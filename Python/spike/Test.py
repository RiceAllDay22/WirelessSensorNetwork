import serial
import time
import sys

ser = serial.Serial('COM5', 9600, timeout=1)
ser.flushInput()







for i in range(5):
    data = ser.readline().decode('utf-8').strip('\n').strip('\r')
    print(data)
    time.sleep(1)


#ser.write(bytes([0, 1, 2, 3, 4, 5, 6]))
#counter = 0
while 1: 
    #ser.write(bytes([counter]))
    data = ser.readline().decode('utf-8').strip('\n').strip('\r')
    print(data)
    #print(counter, hex(counter), data)
    #counter += 1
    #if counter == 256:
    #    counter = 0
    time.sleep(1)