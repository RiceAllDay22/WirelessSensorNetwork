import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

filename = '11-01-21_Trial1.csv'

dataPD = pd.read_csv(filename)
dataNP = dataPD.to_numpy()


x = dataNP[:,1]
y_Licor = dataNP[:,2]
y_SCD1 = dataNP[:,3]
y_SCD2 = dataNP[:,4]
y_SCD3 = dataNP[:,5]
y_SCD4 = dataNP[:,6]

start = 0
end =  -1

plt.plot(x[start:end], y_Licor[start:end], 'r--', label = 'LiCor')
plt.plot(x[start:end], y_SCD1[start:end], 'b', label = 'SCD30 # 1')
plt.plot(x[start:end], y_SCD2[start:end], 'g', label = 'SCD30 # 2')
plt.plot(x[start:end], y_SCD3[start:end], 'y', label = 'SCD30 # 3')
plt.plot(x[start:end], y_SCD4[start:end], 'm', label = 'SCD30 # 4')

plt.title('CO2 vs Time with different sensors')
# #plt.title('CO2 vs Time with different sensors: ' + filename)
plt.xlabel('Time (sec)')
plt.ylabel('CO2 (ppm)')
plt.grid()
plt.legend()
plt.show()

#print(x_Licor)