import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

user      = 'adria'
#subfolder = 'Pintern_Lab_CU-1106'
subfolder = 'Pintern_Union_CU-1106'
os.chdir('C:\\Users\\'+str(user)+
         '\\Desktop\\Repo\\WirelessSensorNetwork\\Data\\'+str(subfolder))

#all_data_DF = pd.read_csv("Lab_All_Data.csv")
all_data_DF = pd.read_csv("Union_All_Data.csv")
all_data_NP = all_data_DF.to_numpy()


# Offsets for Lab Data
# x_C = all_data_NP[:, 0]
# y_C = all_data_NP[:, 1] - 400

# x_HNS = all_data_NP[:, 3]
# y_HNS = all_data_NP[:, 4] - 100

# x_SLN = all_data_NP[:, 6]
# y_SLN = all_data_NP[:, 7] + 100

# x_SLNS = all_data_NP[:, 9]
# y_SLNS = all_data_NP[:, 10] + 100

# x_licor = all_data_NP[:, 12] - 1250 #1150 #-1250
# y_licor = all_data_NP[:, 14] # + 150 # 500


# Offsets for Union Data
x_C = all_data_NP[:, 0]
y_C = all_data_NP[:, 1] - 400 #- 400

x_HNS = all_data_NP[:, 3]
y_HNS = all_data_NP[:, 4] #- 100

x_SLN = all_data_NP[:, 6]
y_SLN = all_data_NP[:, 7] # + 100

x_SLNS = all_data_NP[:, 9]
y_SLNS = all_data_NP[:, 10] # + 100

x_licor = all_data_NP[:, 12] + 160
y_licor = all_data_NP[:, 14]


#start = 0
#end = 2500
#plt.plot(x_C[start:end], y_C[start:end],
#        'r', linestyle = '-', linewidth = 1, label = 'C')
#plt.plot(x_HNS[start:end], y_HNS[start:end],
#        'lime', linestyle = '-', linewidth = 1, label = 'HNS')
#plt.plot(x_SLN[start:end], y_SLN[start:end],
#        'b', linestyle = '-', linewidth = 1, label = 'SLN')
#plt.plot(x_SLNS[start:end], y_SLNS[start:end],
#        'm', linestyle = '-', linewidth = 1, label = 'SLNS')

start = 0
end = 3700
plt.plot(x_licor[start:end], y_licor[start:end],
        'k', linestyle = '--', linewidth = 1, label = 'Licor')

#plt.savefig("Figure3_CU1106_Union_All.png")
plt.title("CO2 vs Time with CU-1106 models and LI-800")
plt.xlabel("Time (sec)")
plt.ylabel("CO2 (ppm)")
plt.legend()
plt.grid()
plt.show()