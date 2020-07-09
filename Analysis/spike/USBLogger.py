import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import datetime

#File Selector
user      = 'adria'
#user      = 'Adriann Liceralde'
date      =  sys.argv[1]
file      = date +'.csv'
subfolder = 'SolarProduction'
#subfolder = 'Charge'
#subfolder = 'Discharge'
os.chdir('C:\\Users\\'+str(user)+'\\Desktop\\Repository\\WirelessSensorNetwork\\Data\\Power\\'
         + str(subfolder))
os.getcwd()
dataPD = pd.read_csv(file)
dataPD = dataPD.iloc[int(sys.argv[2]):int(sys.argv[3])]

#Summarize Info
dataPD['mAh'] = (dataPD['Current(A)']+0.020) * 1000/3600
#dataPD['mWh'] = dataPD['mAh']*dataPD['Voltage(V)']

totalAh = dataPD['mAh'].sum()/1000
totalWh = totalAh*3.7 

startTime  = datetime.datetime.strptime(dataPD['Time'].iloc[0] , '%H:%M:%S')
endTime    = datetime.datetime.strptime(dataPD['Time'].iloc[-1], '%H:%M:%S')

maxmA = round(dataPD['Current(A)'].max()  , 4)
minmA = round(dataPD['Current(A)'].min()  , 4)
avgmA = round(dataPD['Current(A)'].mean() , 4)

maxV  = round(dataPD['Voltage(V)'].max() , 4)
minV  = round(dataPD['Voltage(V)'].min() , 4)
avgV  = round(dataPD['Voltage(V)'].mean(), 4)

print('')
print('Start:' , startTime.time())
print('End:  ' , endTime.time())
print('Total:' , endTime - startTime)
print('')
print('Max A:' , maxmA)
print('Min A:' , minmA)
print('Avg A:' , avgmA)
print('Max V:'  , maxV)
print('Min V:'  , minV)
print('Avg V:'  , avgV)
print('')
print('Wh:  ' , round(totalWh,3))
print('Ah:  ' , round(totalAh,3))
print('')

timeArray    = np.array(dataPD['Time'])
currentArray = np.array(dataPD['Current(A)'])
voltageArray = np.array(dataPD['Voltage(V)'])
if len(sys.argv) > 4:
    if int(sys.argv[4]) == 1:
        plt.plot(currentArray, 'r')
        plt.xlabel('Index')
        plt.ylabel('Current')
        plt.title(file[0:-4])
        plt.show()
    elif int(sys.argv[4]) == 2:
        plt.plot(voltageArray, 'b')
        plt.xlabel('Index')
        plt.ylabel('Voltage')
        plt.title(file[0:-4])
        plt.show()
    
    
    elif int(sys.argv[4]) == 3:
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        
        ax1.plot(currentArray, 'r')
        ax2.plot(voltageArray, 'b-')

        ax1.set_xlabel('Index')
        ax1.set_ylabel('Current')
        ax2.set_ylabel('Voltage')
        plt.title(file[0:-4])
        plt.show()



