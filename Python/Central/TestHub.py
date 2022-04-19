'''
    Title:      Central Hub Continuous Extraction Code [TEST VERSION]
    Project:    Wireless Sensor Network
    By:         Adriann Liceralde
    Updated:    3-25-2022
    
    This code is intended for the Central Hub of the Wireless Sensor Network.
    The Central Hub consists of a Digi3 XBee3 RF Module attached to a computer.
    The XBee3 receives all data from the Mesh Network and stores it into the computer.
    Running this code on the Windows Powershell will continuously ave any incoming data from the XBee3.
'''

#IMPORT LIBRARIS
import sys
import time
import serial
import datetime
import pytz

#SYSTEM ARGUMENTS
record_on = int(sys.argv[1]) # Determines if incoming data is saaved to the computer
com_port = str(sys.argv[2]) # Specifies the Serial port of the XBee 3 module

# SETUP SERIAL
ser = serial.Serial(com_port, 9600, timeout=1) # Sets the Serial port
ser.flushInput() # Clears the Serial port                            

# FUNCTION TO GET CURRENT TIME # Takes roughly 0.015 seconds to run get_datetime()
def get_datetime():
    dt = datetime.datetime.now(tz = pytz.timezone('UTC'))
    ut = int(dt.timestamp())
    y = dt.year - 2000
    m = dt.month
    d = dt.day
    hh = dt.hour
    mm = dt.minute
    ss = dt.second
    dt_array = ([y, m, d, hh, mm, ss])
    return dt_array

print(get_datetime())
# Y, M, D, h, m, s  = map(int, (file_dt))
# FUNCTION TO CREATE FILE
def create_file():
    file_dt = get_datetime()
    Y, M, D, h, m, s  = map(int, (file_dt))
    filename = 'T-'+str(Y+2000)+'-'+str(M)+'-'+str(D)+'--'+str(h)+'-'+str(m)+'.csv'
    return filename


# MAIN LOOP OF THE CODE
try:
    if record_on == 1:
        filename = create_file()
        print(filename)
        target = open(filename, 'a')

    while 1:
        #wait = ser.inWaiting()
        #print(wait)
        # if wait > 0:

        # Check for data, then save if there is
        data = ser.readline().decode('utf-8').strip('\n').strip('\r')
        if data:
            print(data)
            if record_on == 1:
                target.write(data)
                target.write("\n") 

        # Create New File
        # Takes 0.015 seconds to run the checker
        dt = get_datetime()
        #if dt[4] == 0 and dt[5] == 0:
            #print(dt, "New File-------------------------------------------")
            #if record == 1:
            #    target.close()
            #    filename = create_file()
            #    target = open(filename, 'a')

        # Unixtime Synchronization
        if dt[3] == 0:
            sync_dt = get_datetime()
            ser.write(bytes(sync_dt))
        time.sleep(0.02)

        
finally:
    print('Close the File')
    if record_on == 1:
        target.close()








#LOOP
# try:
#     while 1:
#         wait = ser.inWaiting()
#         if wait > 0:
#             data = ser.readline().decode('utf-8').strip('\n').strip('\r')
#             if data:
#                 print(data)
#                 target.write(data)
#                 target.write("\n") 
#         else:
#             time.sleep(0.1)
