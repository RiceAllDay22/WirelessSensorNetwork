'''Written by Adriann Liceralde
   Wireless Sensor Network Project
   Script for analyzing the Real-Time Clock's time drift
   Last Updated 3/18/2022
'''
#Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Import File
filename = 'Dataset.csv'
dataPD = pd.read_csv(filename)
dataNP = dataPD.to_numpy()

#Create Arrays
local_date = dataNP[:,0]
local_hour = dataNP[:,1]
local_min = dataNP[:,2]
local_sec = dataNP[:,3]
rtc1_min = dataNP[:,4]
rtc1_sec = dataNP[:,5]
rtc2_min = dataNP[:,6]
rtc2_sec = dataNP[:,7]
rtc3_min = dataNP[:,8]
rtc3_sec = dataNP[:,9]
rtc4_min = dataNP[:,10]
rtc4_sec = dataNP[:,11]

#Calculate Raw Differences
delta_rtc1 = rtc1_sec - local_sec
delta_rtc2 = rtc2_sec - local_sec
delta_rtc3 = rtc3_sec - local_sec
delta_rtc4 = rtc4_sec - local_sec

#Reconcile 0 second and 60 second
delta_rtcs = [delta_rtc1, delta_rtc2, delta_rtc3, delta_rtc4]
rtcs_sec = [rtc1_sec, rtc2_sec, rtc3_sec, rtc4_sec]
for j in range(len(delta_rtcs)):
    for i in range(len(delta_rtcs[j])):
        if (delta_rtcs[j][i] < -50):
            delta_rtcs[j][i] = rtcs_sec[j][i] - local_sec[i] + 60
        elif delta_rtcs[j][i] > 50:
            delta_rtcs[j][i] = rtcs_sec[j][i] - local_sec[i] - 60

#Determine Hourly Average
amount = len(local_sec)//3600
y_1 = np.array([])
y_2 = np.array([])
y_3 = np.array([])
y_4 = np.array([])

for i in range(0, amount):
    avg_delta_rtc1 = np.average(delta_rtc1[i*3600:(i+1)*3600])
    avg_delta_rtc2 = np.average(delta_rtc2[i*3600:(i+1)*3600])
    avg_delta_rtc3 = np.average(delta_rtc3[i*3600:(i+1)*3600])
    avg_delta_rtc4 = np.average(delta_rtc4[i*3600:(i+1)*3600])
    y_1 = np.append(y_1, avg_delta_rtc1)
    y_2 = np.append(y_2, avg_delta_rtc2)
    y_3 = np.append(y_3, avg_delta_rtc3)
    y_4 = np.append(y_4, avg_delta_rtc4)

# Shift the Hourly Averages to make the baseline by at Zero Deviation
y_1 = y_1 - y_1[0]
y_2 = y_2 - y_2[0]
y_3 = y_3 - y_3[0]
y_4 = y_4 - y_4[0]

# Plot Hourly Average
# x = np.arange(amount)
# plt.plot(x, y_1, 'r', label = "RTC#1")
# plt.plot(x, y_2, 'g', label = "RTC#2")
# plt.plot(x, y_3, 'b', label = "RTC#3")
# plt.plot(x, y_4, 'y', label = "RTC#4")
# plt.axhline(y = 0, color = 'k', linestyle = '--', label = 'Baseline')
# plt.title("Hourly Average of the Time Deviation")
# plt.xlabel("Time (Hours)")
# plt.ylabel("Deviation from Universal Time (Seconds)")
# plt.legend()
# plt.grid()
# plt.show()

# #Plot Entire Dataset
start = 148000
end = 150000
#x = np.arange(len(local_sec)-1)
x = np.arange(end-start)
plt.plot(x, delta_rtc1[start:end], 'r', label = "RTC#1")
plt.plot(x, delta_rtc2[start:end], 'g', label = "RTC#2")
plt.plot(x, delta_rtc3[start:end], 'b', label = "RTC#3")
plt.plot(x, delta_rtc4[start:end], 'y', label = "RTC#4")
plt.title("Entire Time Deviation")
plt.xlabel("Time (Seconds)")
plt.ylabel("Deviation from Baseline (Seconds)")
plt.legend()
plt.grid()
plt.show()
