import sys
import time
import serial
import datetime
import pytz

ser = serial.Serial('COM5', 9600, timeout=1)
ser.flushInput()

# RETRIEVE SYNC TIME - DATETIME
def get_datetime():
    dt = datetime.datetime.now(tz = pytz.timezone('UTC'))
    ut = int(dt.timestamp())
    print(dt, ut)

    y = dt.year - 2000
    m = dt.month
    d = dt.day
    hh = dt.hour
    mm = dt.minute
    ss = dt.second
    dt_array = ([y, m, d, hh, mm, ss])
    return dt_array


# SETUP FILE
file_dt = get_datetime()
Y, M, D, h, m, s  = map(int, (file_dt))
filename = str(Y+2000)+'-'+str(M)+'-'+str(D)+'--'+str(h)+'-'+str(m)+'.csv'
print(filename)
target = open(filename, 'a')


# WARMUP
for i in range(2):
    data = ser.readline().decode('utf-8').strip('\n').strip('\r')
    print(data)
    time.sleep(1)


#LOOP
counter = 0
try:
    while 1:
        data = ser.readline().decode('utf-8').strip('\n').strip('\r')
        if data:
            print(data)
            target.write(data)
            target.write("\n") 
        time.sleep(1)
        counter+=1

        if counter == 5:
            # TRANSMIT SYNC TIME
            sync_dt = get_datetime()
            ser.write(bytes(sync_dt))

finally:
    print('Close the File')
    target.close()



# #RETRIEVE SYNC TIME - UNIXTIME
# #ut = int(datetime.datetime.utcnow().timestamp())
# dt = datetime.datetime.utcnow()
# ut = int(dt.timestamp())
# print(dt)
# print(ut)

# b1 = ut >> 24
# b2 = ut >> 16 & 255
# b3 = ut >> 8 & 255
# b4 = ut & 255
# print(b1, b2, b3, b4)