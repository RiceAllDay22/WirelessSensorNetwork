import serial
import time
import sys

ser = serial.Serial('COM5', 9600, timeout=1)
ser.flushInput()



ser.write(bytes([0, 1, 2, 3, 4, 5, 6]))
data = ser.readline().decode('utf-8').strip('\n').strip('\r')
print(data)

# counter = 0
# while 1: 
#     ser.write(bytes([counter]))
#     data = ser.readline().decode('utf-8').strip('\n').strip('\r')
#     print(counter, hex(counter), data)
#     counter += 1
#     if counter == 256:
#         counter = 0
#     time.sleep(1)