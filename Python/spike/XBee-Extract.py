import serial
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sys import stdin, stdout


computer_time = datetime.datetime.now()
Y = computer_time.year
M = computer_time.month
D = computer_time.day
H = computer_time.hour
m = computer_time.minute

filename = str(Y)+'-'+str(M)+'-'+str(D)+'-'+str(H)+'-'+str(m)+'.csv'
open(filename, 'w').close()


ser = serial.Serial('COM5', 9600, timeout=1)
ser.flushInput()

target = open(filename, 'a')

while 1:
    data = ser.readline().decode('utf-8').strip('\n').strip('\r')
    if data != '':
        print(data)
        target.write(data)
        target.write("\n") 
    
    
    stdout.buffer.write(bytes([22]))
    print(22)
    #sys.stdout.write('22')
    #sys.stdin.buffer.write(bytes(22))
    #sys.stdout.buffer.write(bytes(22))
        