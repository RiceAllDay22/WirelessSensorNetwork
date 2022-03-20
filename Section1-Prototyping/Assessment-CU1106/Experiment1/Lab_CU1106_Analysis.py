#Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Import File
filename = 'Lab_All_Data.csv'
dataPD = pd.read_csv(filename)
dataNP = dataPD.to_numpy()

# Normal Values
x_C = dataNP[:, 0]
y_C = dataNP[:, 1]
x_HNS = dataNP[:, 2]
y_HNS = dataNP[:, 3]
x_SLN = dataNP[:, 4]
y_SLN = dataNP[:, 5]
x_SLNS = dataNP[:, 6]
y_SLNS = dataNP[:, 7]
x_licor = dataNP[:, 8] - 1250
y_licor = dataNP[:, 9]


#Adjusted Values
# x_C = dataNP[:, 0]
# y_C = dataNP[:, 1] -350
# x_HNS = dataNP[:, 2]
# y_HNS = dataNP[:, 3] - 100
# x_SLN = dataNP[:, 4]
# y_SLN = dataNP[:, 5] + 100
# x_SLNS = dataNP[:, 6]
# y_SLNS = dataNP[:, 7] + 100
# x_licor = dataNP[:, 8] - 1250
# y_licor = dataNP[:, 9]


#Plot CU1106 data
start = 0
end =  900
plt.plot(x_C[start:end], y_C[start:end], 'r', linestyle = '-', linewidth = 0.5, label = 'C')
plt.plot(x_HNS[start:end], y_HNS[start:end], 'lime', linestyle = '-', linewidth = 0.5, label = 'HNS')
plt.plot(x_SLN[start:end], y_SLN[start:end], 'b', linestyle = '-', linewidth = 0.5, label = 'SLN')
plt.plot(x_SLNS[start:end], y_SLNS[start:end],'m', linestyle = '-', linewidth = 0.5, label = 'SLNS')

#Plot Licor data
start = 1
end = 1350
plt.plot(x_licor[start:end], y_licor[start:end], 'k', linestyle = '--', linewidth = 1, label = 'Licor')
plt.legend()
#plt.savefig("Lab_Data_Full.jpeg")
plt.grid()
plt.xlabel("Time (sec)")
plt.ylabel("CO2 (ppm)")
plt.show()
