import numpy as np
import pandas as pd
import os
import glob

month, day = 2, 4
extension = ''
#os.chdir('D:\\')
os.chdir('C:\\Users\\adria\\Desktop\\ComboTest')
#os.chdir('C:\\Users\\adria\\Desktop\\Combo\\Month'+str(month)+'Day'+str(day)+extension)

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]


AllUnixTime = np.array([])
AllGasData  = np.array([])
for each in all_filenames:
    data = pd.read_csv(each, skiprows = 1)
    UnixTime = np.array(data.iloc[:,0])
    GasData  = np.array(data.iloc[:,1])
    AllUnixTime = np.append(AllUnixTime, UnixTime)
    AllGasData  = np.append(AllGasData,  GasData)

CombineNP = np.column_stack((AllUnixTime, AllGasData))
CombineDF = pd.DataFrame(CombineNP)
CombineDF.columns = ['UNIXTIME', 'CO2']

CombineDF.to_csv("Combined.csv", index=False, encoding='utf-8-sig')