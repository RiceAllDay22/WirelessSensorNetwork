'''
    Last updated: 2-9-2022
    Adriann Liceralde
    Wireless Sensor Network Project
'''

#IMPORT LIBRARIS
import sys
import time
import serial
import datetime
import pytz
import sys

record = int(sys.argv[1])

# SETUP SERIAL
ser = serial.Serial('COM14', 9600, timeout=1)
ser.flushInput()


# GET CURRENT TIME
# Takes roughly 0.015 seconds to run get_datetime()
def get_datetime():
    # a = time.time()
    dt = datetime.datetime.now(tz = pytz.timezone('UTC'))
    ut = int(dt.timestamp())

    y = dt.year - 2000
    m = dt.month
    d = dt.day
    hh = dt.hour
    mm = dt.minute
    ss = dt.second
    dt_array = ([y, m, d, hh, mm, ss])

    # time.sleep(0.001)
    # b = time.time()
    # print(b-a)
    return dt_array

print(get_datetime())
# Y, M, D, h, m, s  = map(int, (file_dt))

# SETUP FILE
def create_file():
    file_dt = get_datetime()
    Y, M, D, h, m, s  = map(int, (file_dt))
    filename = 'T-'+str(Y+2000)+'-'+str(M)+'-'+str(D)+'--'+str(h)+'-'+str(m)+'.csv'
    return filename


# LOOP
try:
    if record == 1:
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
            if record == 1:
                target.write(data)
                target.write("\n") 

        # Create New File
        # Takes 0.015 seconds to run the checker
        dt = get_datetime()
        if dt[4] == 0 and dt[5] == 0:
            print("New File")
            if record == 1:
                target.close()
                filename = create_file()
                target = open(filename, 'a')

        # Unixtime Synchronization
        if dt[3] == 0:
            sync_dt = get_datetime()
            ser.write(bytes(sync_dt))
        time.sleep(0.02)

        
finally:
    print('Close the File')
    if record == 1:
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
