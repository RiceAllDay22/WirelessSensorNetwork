import numpy as np
import pandas as pd
import os
import glob

import os
import sys


#File Selector
user      = str(sys.argv[1])
date      = str(sys.argv[2])
file      = date +'.csv'
os.chdir('D:')

extension = 'csv'
all_filenames = file

allUnixTime = np.array([])
allWindSpeed= np.array([])
allWindDir  = np.array([])
allGasData  = np.array([])

f = open(file, "rb")
filesize   = int(os.path.getsize(file))
headersize = 0
lines      = (filesize-headersize)//8

print('File :' , file, '\n', 'Bytes:' , filesize, '\n', 'Lines:' , lines)
first = False
counter = 0
        
for i in range(lines):
    if (first == False) and headersize > 0:
        filler = str(f.read(headersize), 'utf-8')
        first  = True
    unix = int.from_bytes(f.read(4), byteorder='big')
    ws   = int.from_bytes(f.read(1), byteorder='big')
    wd   = int.from_bytes(f.read(1), byteorder='big')
    gas  = int.from_bytes(f.read(2), byteorder='big')
    allUnixTime = np.append(allUnixTime, str(unix))
    allWindSpeed= np.append(allWindSpeed, ws)
    allWindDir  = np.append(allWindDir,  wd)
    allGasData  = np.append(allGasData, gas)

#allWindDir   *= 22.5
#allWindSpeed *= 1.492
CombineNP = np.column_stack((allUnixTime, allWindSpeed, allWindDir, allGasData))
CombineDF = pd.DataFrame(CombineNP)
CombineDF.columns  = ['UnixTime', 'Wind Speed', 'Wind Dir', 'GasData']
CombineDF.UnixTime = CombineDF.UnixTime.astype(int)

name = 'C-'+ str(file)[0:-8] + str('.csv')
CombineDF.to_csv(name, index=False, encoding='utf-8-sig')
