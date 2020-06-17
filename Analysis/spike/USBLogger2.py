import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import datetime

#File Selector
user      = 'adria'
file      = '2020-06-11--10.csv'
subfolder = 'SolarProduction'
os.chdir('C:\\Users\\'+str(user)+'\\Desktop\\Repository\\WirelessSensorNetwork\\Data\\Power\\'
         + str(subfolder))
os.getcwd()
dataPD = pd.read_csv(file)
dataPD = dataPD.iloc[int(sys.argv[1]):int(sys.argv[2])]

#Summarize Info
dataPD['mWh'] = dataPD['Current(A)']*1000/3600*dataPD['Voltage(V)']
totalWh = round(dataPD['mWh'].sum()/1000, 2)
startTime  = datetime.datetime.strptime(dataPD['Time'].iloc[0] , '%H:%M:%S')
endTime    = datetime.datetime.strptime(dataPD['Time'].iloc[-1], '%H:%M:%S')

maxmA = round(dataPD['Current(A)'].max()  , 4)
avgmA = round(dataPD['Current(A)'].mean() , 4)

maxV  = round(dataPD['Voltage(V)'].max() , 4)
avgV  = round(dataPD['Voltage(V)'].mean(), 4)
print('Start:' , startTime.time())
print('End:  ' , endTime.time())
print('Total:' , endTime - startTime)
print('')
print('Max mA:' , maxmA)
print('Avg mA:' , avgmA)
print('Max V:'  , maxV)
print('Avg V:'  , avgV)
print('Wh:   ' , totalWh)

dataNP = dataPD.to_numpy()
print(dataNP[:,0])
if len(sys.argv) > 3:
    if int(sys.argv[3]) == 1:
        plt.plot(dataNP[:,0], dataNP[:,2], 'r')
        plt.show()



