import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

#File Selector
#user      = 'adria'
user      = 'Adriann Liceralde'
file      = '2020-06-11--10.csv'
subfolder = 'SolarProduction'
os.chdir('C:\\Users\\'+str(user)+'\\Desktop\\Repository\\WirelessSensorNetwork\\Data\\Power\\'
         + str(subfolder))
os.getcwd()
data = pd.read_csv(file)

#Retrieve Data
timeArray    = np.array(data['Time'])
voltageArray = np.array(data['Voltage(V)'])
currentArray = np.array(data['Current(A)'])*1000
averageCurrentRaw = np.mean(currentArray)

left  = int(sys.argv[1])
right = int(sys.argv[2])
timeSlice    = right - left
voltageSlice = voltageArray[left:right]
currentSlice = currentArray[left:right]

#Display Data
print('Length:', len(timeArray)/3600)
print('Avg mA:', np.mean(currentSlice))
print('Sec:', timeSlice)
print('mAh:', np.mean(currentSlice)*timeSlice/3600)
plt.plot(currentArray[left:right], 'r')
#plt.plot(voltageArray[left:right], 'r')
plt.ylabel('Current (mA)')
plt.xlabel('Time (s)')
plt.show()

