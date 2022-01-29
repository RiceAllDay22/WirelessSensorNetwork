import sys
import time
import serial
import datetime
import pytz

ser = serial.Serial('COM4', 9600, timeout=1)
ser.flushInput()

def get_datetime():
    #a = time.time()
    dt = datetime.datetime.now(tz = pytz.timezone('UTC'))
    ut = int(dt.timestamp())
    ##print(dt, ut)

    y = dt.year - 2000
    m = dt.month
    d = dt.day
    hh = dt.hour
    mm = dt.minute
    ss = dt.second
    dt_array = ([y, m, d, hh, mm, ss])
    #time.sleep(0.1)
    #b = time.time()
    #print(b-a)
    return dt_array


# SETUP FILE
file_dt = get_datetime()
Y, M, D, h, m, s  = map(int, (file_dt))
filename = str(Y+2000)+'-'+str(M)+'-'+str(D)+'--'+str(h)+'-'+str(m)+'.csv'
print(filename)
target = open(filename, 'a')



try:
    while 1:
        data = ser.readline().decode('utf-8').strip('\n').strip('\r')
        if data:
            print(data)
            target.write(data)
            target.write("\n") 
        time.sleep(0.02)

finally:
    print('Close the File')
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



# finally:
#     print('Close the File')
#     target.close()

