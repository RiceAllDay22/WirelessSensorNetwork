import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time


#Function: 4 bytes to unixtime
def byte_to_ut(b1, b2, b3, b4):
    ut = b1*256**3 + b2*256**2 + b3*256**1 + b4
    return ut


#Function: 2 bytes to ws and wd
def byte_to_wind(b1, b2):
    if b2 > 127:
        wd = b1*2 + 1
        ws = b2 - 128
    else:
        wd = b1*2
        ws = b2
    return ws, wd

#Function: 2 bytes to 16 bit
def byte_to_ppm(b1, b2):
    ppm = b1*256 + b2
    return ppm

#Function: 1 byte to 8 bit
def byte_to_temp(b1):
    temp = b1 - 40
    return temp



time_start = time.time()
#filename = 'Data_11-27.csv'
filename = 'Data_unix.csv'
dataPD = pd.read_csv(filename, sep=',', header=None)
dataNP = dataPD.to_numpy()



for i in range(0, len(dataNP)):
    row = dataNP[i]
    if np.isfinite(np.sum(row)):
        if row[1] == 0 and row[2] == 255:
            base_ut = byte_to_ut(row[3], row[4], row[5], row[6])
            print(base_ut)
        else:
            b_n, b_s, b_w1, b_w2, b_c1, b_c2, b_t = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            nid = b_n
            
            ut = base_ut + b_s
            base_ut = ut
            ws, wd = byte_to_wind(b_w1, b_w2)
            ppm = byte_to_ppm(b_c1, b_c2)
            temp = byte_to_temp(b_t)
            print(nid, ut, ws, wd, ppm, temp)

    else:
        print('nan')
    
time_end = time.time()
print('Execution Time:', time_end-time_start)