# IMPORT LIBRARIES
import numpy as np
import matplotlib.pyplot as pyplot
import pandas as pd
import os

# LOAD FILE
os.chdir('C:\\Users\\adria\\Desktop\\Repo\\WirelessSensorNetwork\\Python\\Central\\Process')
colnames = ['bn', 'u1', 'u2', 'u3', 'u4', 'c1', 'c2', 'ws', 'wd', 'bt']
filename = 'C-2022-6-18--1-52.csv'
df = pd.read_csv(filename, names = colnames, header = None)
df = df.dropna()
print(df.head())

# CONVERT BYTES TO INTEGERS
df['ut'] = df['u1']*256**3 + df['u2']*256**2 + df['u3']*256 + df['u4']
df['conc'] = df['c1']*256 + df['c2']
df['inter'] = np.where(df['bt'] > 127, True, False)
df['dir'] = np.where(df['inter'] == True, df['wd']*2+1, df['wd']*2)
df['temp'] = np.where(df['inter'] == True, df['bt']-40-128, df['bt']-40)

# REARRANGE DATAFRAME
df.drop(['u1', 'u2', 'u3', 'u4', 'c1', 'c2', 'wd', 'bt', 'inter'], axis=1, inplace=True)
df = df[['bn', 'ut', 'conc', 'ws', 'dir', 'temp']]

print(df.head())
print(df.tail())

# EXPORT FILE
df.to_csv('Processed'+str(filename), index=False, encoding='utf-8-sig')
