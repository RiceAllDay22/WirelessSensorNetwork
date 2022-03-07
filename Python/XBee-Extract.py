import serial
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
import time

computer_time = datetime.datetime.now()
Y = computer_time.year
M = computer_time.month
D = computer_time.day
H = computer_time.hour
m = computer_time.minute

#filename = str(Y)+'-'+str(M)+'-'+str(D)+'-'+str(H)+'-'+str(m)+'.csv'
#open(filename, 'w').close()

ser = serial.Serial('COM5', 9600, timeout=1)
ser.flushInput()

target = open(filename, 'a')

#while 1:
    #data = ser.readline().decode('utf-8').strip('\n').strip('\r')
    #if data != '':
    #    print(data)
    #    target.write(data)
    #    target.write("\n") 
    

    #print(22)
    #-----ERRORS-----#
    #ser.write('22') #TypeError: unicode strings are not supported, please encode to bytes: '22'
    #sys.stdout.write(22) #TypeError: write() argument must be str, not int
    #sys.stdout.write(bytes([22])) #TypeError: write() argument must be str, not bytes
    #sys.stdout.buffer.write(22) # TypeError: a bytes-like object is required, not 'int'
    #sys.stdout.buffer.write('22') # TypeError: a bytes-like object is required, not 'str'
    #sys.stdin.write(22) # TypeError: write() argument must be str, not int
    #sys.stdin.write('22') # io.UnsupportedOperation: not writable
    #sys.stdin.write(str(22)) # io.UnsupportedOperation: not writable
    #sys.stdin.write(bytes([22])) # TypeError: write() argument must be str, not bytes
    #sys.stdin.buffer.write(22) #io.UnsupportedOperation: write
    #sys.stdin.buffer.write(bytes([22])) #io.UnsupportedOperation: write
    


    #-----WORKS-----#
    #ser.write(bytes([22]))    # Return: b'\xff'
    #ser.write(bytes([0]))      # Return: b'\x00'
    #ser.write(bytes([10]))     # Return: b'\n'
    #ser.write(bytes([20]))     # Return: b'\x14'

    #-----POSSIBLE-----#

    #ser.write(bytes([22]))
    #ser.write(bytes([255, 250, 230, 220]))         # Return: b'\xff\xfa\xe6\xdc'
    #ser.write(bytes([255, 250, 230, 220, 40]))      # Return: b'\xff\xfa\xe6\xdc('
    #ser.write(bytes([255, 250, 230])) 
    
    




    #-----NOT REALLY-----#
    #ser.write(22) # Return: 
    #ser.write(bytes([0, 1, 2, 3, 4, 5])) # continuous soft reboot
    #sys.stdout.buffer.write(bytes([22])) # Return ▬
    #sys.stdout.write('22') # Return: 22
    #sys.stdout.write(str(22)) # Return: 22



    
    #data = ser.read()


    #ser.write(bytes([22]))    # Return: b'\xff'
    #ser.write(bytes([0]))      # Return: b'\x00'
    #ser.write(bytes([10]))     # Return: b'\n'
    #ser.write(bytes([20]))     # Return: b'\x14'

    #data = ser.readline().decode('utf-8').strip('\n').strip('\r')
    #print(data)
    #time.sleep(0.1)

counter = 0


#RETRIEVE SYNC TIME
#ut = int(datetime.datetime.utcnow().timestamp())
#b1 = ut >> 24
#b2 = ut >> 16 & 255
#b3 = ut >> 8 & 255
#b4 = ut & 255
#print(b1, b2, b3, b4)


while 1:
    #ser.write(bytes([126]))
    #ser.write(bytes([250, 240, 230, 220, 210, 200, 190, 180, 170, 160, 150, 140, 130]))
    
    ut = int(datetime.datetime.utcnow().timestamp())
    b1 = ut >> 24
    b2 = ut >> 16 & 255
    b3 = ut >> 8 & 255
    b4 = ut & 255
    
    ser.write(bytes([b1, b2, b3, b4]))
    #data = ser.read()
    data = ser.readline().decode('utf-8').strip('\n').strip('\r')
    print(data)
    time.sleep(1)

    #counter += 1
    #if counter == 5:
    #    print('SYNCHRONIZE')
    #    ser.write(bytes([127]))

#data = ser.readline().decode('utf-8').strip('\n').strip('\r')


#counter = 4
#while 1: 

#    ser.write(bytes([counter]))
#    data = ser.readline().decode('utf-8').strip('\n').strip('\r')
#    print(counter, hex(counter), data)
#    counter += 1
#    if counter == 256:
#        counter = 0
#    time.sleep(1)
