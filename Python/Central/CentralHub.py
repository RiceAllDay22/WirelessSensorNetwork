'''
    Title:      Central Hub Continuous Extraction Code
    Project:    Wireless Sensor Network
    By:         Adriann Liceralde
    Updated:    4-19-2022
    
    This code is intended for the Central Hub of the Wireless Sensor Network.
    The Central Hub consists of a Digi3 XBee3 RF Module attached to a computer.
    The XBee3 receives all data from the Mesh Network and stores it into the computer.
    Running this code on the Windows Powershell will continuously save any incoming data from the XBee3.
'''

# IMPORT LIBRARIES
import sys
import time
import serial
import datetime
import pytz

# SYSTEM ARGUMENTS
record_on = int(sys.argv[1]) # Determines if incoming data is saved to the computer. 0 = not saved. 1 = saved.
com_port = str(sys.argv[2]) # Specifies the Serial port of the XBee 3 module. For example, 'COM12'

# SETUP SERIAL PORT
ser = serial.Serial(com_port, 9600, timeout=1) # Sets the Serial port
ser.flushInput() # Clears the Serial port    

# FUNCTION: GET CURRENT TIME (Takes roughly 0.015 seconds to run get_datetime() )
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

# FUNCTION: CREATE FILE
def create_file():
    file_dt = get_datetime()
    Y, M, D, h, m, s  = map(int, (file_dt))
    filename = 'C-'+str(Y+2000)+'-'+str(M)+'-'+str(D)+'--'+str(h)+'-'+str(m)+'.csv'
    return filename

# CREATE NEW FILE
if record_on == 1:
    filename = create_file()
    target = open(filename, 'a')

# MAIN LOOP OF THE CODE
try:
    print('Time:', get_datetime())
    print('File:', filename)
    
    while 1:
        # wait = ser.inWaiting()
        # print(wait)
        # if wait > 0:
        #     print('wait:', wait)

        # CHECK FOR INCOMING DATA
        data = ser.readline().decode('utf-8').strip('\n').strip('\r')

        # Check if new data is available
        if data:
            print(data)

            # Check if data was a Time Sync Request
            if data == '[256, 1, 256]':
                sync_dt = get_datetime()
                sync_dt.insert(0, 255)
                sync_dt.append(255)
                ser.write(bytes(sync_dt))

            # Save normal Node data to file
            else:
                if record_on == 1:
                    target.write(data)
                    target.write("\n") 
        else:
            print('No data')

        # Check if it is a new hour to create a new save file
        dt = dt = get_datetime()
        if dt[4] == 0 and dt[5] == 0:
            print("New File")
            if record == 1:
                target.close()
                filename = create_file()
                target = open(filename, 'a')

            # Check if it is a new day to broadcast a timestamp synchronization
            if dt[3] == 0:
                sync_dt = get_datetime()
                sync_dt.insert(0, 255)
                sync_dt.append(255)
                ser.write(bytes(sync_dt))
  
finally:
    if record_on == 1:
        print('Close the File')
        target.close()
