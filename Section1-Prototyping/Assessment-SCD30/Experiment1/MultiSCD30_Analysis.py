import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

filename = 'Lab_10-26_raw.csv'

dataPD = pd.read_csv(filename)
dataNP = dataPD.to_numpy()


x_Licor = dataNP[:,1]
y_Licor = dataNP[:,2]

x_SCD = dataNP[:,4]
y_SCD1 = dataNP[:,5]
y_SCD2 = dataNP[:,6]
y_SCD3 = dataNP[:,7]
y_SCD4 = dataNP[:,8]


start = 700
end =  900

start_licor = start*3
end_licor = end*3

plt.plot(x_Licor[start_licor:end_licor], y_Licor[start_licor:end_licor], 'r--', label = 'LiCor')
plt.plot(x_SCD[start:end], y_SCD1[start:end], 'b', label = 'SCD30 # 1')
plt.plot(x_SCD[start:end], y_SCD2[start:end], 'g', label = 'SCD30 # 2')
plt.plot(x_SCD[start:end], y_SCD3[start:end], 'y', label = 'SCD30 # 3')
plt.plot(x_SCD[start:end], y_SCD4[start:end], 'm', label = 'SCD30 # 4')

plt.title('CO2 vs Time with different sensors')
# #plt.title('CO2 vs Time with different sensors: ' + filename)
plt.xlabel('Time (sec)')
plt.ylabel('CO2 (ppm)')
plt.grid()
plt.legend()
plt.show()

#print(x_Licor)