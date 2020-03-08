import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime
from statistics import mean
import IPython.display

# Folder - Continiuous Data
year, month, day =  19, 12, 19
os.chdir('C:\\Users\\adria\\OneDrive - University of Utah\\Documents\\Research\\Project 4 Network\\Continuous Data')
data = pd.read_excel(str(month) + "-" + str(day) + "-" + str(year) + '.xlsx')

# Folder - Combo 
#month, day = 2, 4
#extension = ''
#os.chdir('C:\\Users\\adria\\Desktop\\ComboTest')

# Folder - ComboTest
#os.chdir('C:\\Users\\adria\\Desktop\\ComboTest')
#data = pd.read_csv('Combined.csv')
#pd.set_option('display.max_rows', 100000)


def importData(data):
    UnixTime = np.array(data['UNIXTIME'],  dtype = float)
    GasData  = np.array(data['CO2'],       dtype = float)
    RealData = np.ones((len(UnixTime), 1), dtype = float)
    Index    = np.arange(0, len(UnixTime))
    DateTime = np.array([])
    
    for i in range(0, len(UnixTime)):
        a = datetime.fromtimestamp(UnixTime[i])
        DateTime = np.append(DateTime, a)
    
    rawAllDataNP = np.column_stack((UnixTime, GasData, DateTime, RealData, Index))
    rawAllDataDF = pd.DataFrame(rawAllDataNP) 
    rawAllDataDF.columns = ['UnixTime', 'GasData', 'DateTime', 'RealData', 'Index']
    rawAllDataDF = rawAllDataDF.drop_duplicates(subset='UnixTime', keep='first')
    rawAllDataNP = rawAllDataDF.to_numpy()
    return rawAllDataNP, rawAllDataDF
#rawAllDataNP, rawAllDataDF = importData(data)
#rawAllDataDF
    
def importCheck(rawAllDataNP, rawAllDataDF):
    print('|----------DATA CHECKER ----------|')
    print(rawAllDataNP[0][0], type(rawAllDataNP[0][0]))
    print(rawAllDataNP[0][1], type(rawAllDataNP[0][1]))
    print(rawAllDataNP[0][2], type(rawAllDataNP[0][2]))
    print(rawAllDataNP[0][3], type(rawAllDataNP[0][3]))    
    print('')
#importCheck(rawAllDataNP, rawAllDataDF)
    
def dataFilterWhere(rawAllDataNP):
    #global gasZerosIndices, gasLowIndices, gasHighIndices, gasNegIndices #global timeZerosIndices, timeLowIndices, timeHighIndices, timeNegIndices #global fullRemovalIndices
    gasZerosIndices  = np.where( rawAllDataNP[:,1] == 0)
    gasLowIndices    = np.where((rawAllDataNP[:,1] <= 420) & (rawAllDataNP[:,1] > 0))
    gasHighIndices   = np.where( rawAllDataNP[:,1] >= 5000) 
    gasNegIndices    = np.where( rawAllDataNP[:,1] < 0 )
    timeZerosIndices = np.where( rawAllDataNP[:,0] == 0)
    timeLowIndices   = np.where((rawAllDataNP[:,0] <= 1576594500) & (rawAllDataNP[:,0] > 0))
    timeHighIndices  = np.where( rawAllDataNP[:,0] >= 2000000000)                                               
    timeNegIndices   = np.where( rawAllDataNP[:,0] < 0)

    fullRemovalIndices = np.concatenate((
        gasZerosIndices, gasLowIndices, gasHighIndices, gasNegIndices,
        timeZerosIndices,timeLowIndices,timeHighIndices,timeNegIndices), axis = None)
    
    print('|----------DATA REMOVED----------|')
    print('Gas  Zeros: ', len(gasZerosIndices[0]))
    print('Gas   Lows: ', len(gasLowIndices[0]))
    print('Gas  Highs: ', len(gasHighIndices[0]))
    print('Gas   Negs: ', len(gasNegIndices[0]))
    print('Time Zeros: ', len(timeZerosIndices[0]))
    print('Time  Lows: ', len(timeLowIndices[0]))
    print('Time Highs: ', len(timeHighIndices[0]))
    print('Time  Negs: ', len(timeNegIndices[0]))
    print('Total Remd: ', (len(gasZerosIndices[0]) + len(gasLowIndices[0]) + len(gasHighIndices[0]) + len(gasNegIndices[0]) + len(timeZerosIndices[0]) + len(timeLowIndices[0]) + len(timeHighIndices[0]) + len(timeNegIndices[0])))
    print('Total Remd: ', len(fullRemovalIndices))
    print('')
    return fullRemovalIndices

def dataFilterCreator(rawAllDataDF, fullRemovalIndices):
  filAllDataDF = rawAllDataDF[~rawAllDataDF.Index.isin(fullRemovalIndices)]
  filAllDataNP = filAllDataDF.to_numpy()
  return filAllDataNP, filAllDataDF

def windowSelect(filAllDataNP, leftFrame, rightFrame):
    leftFrameIndex, rightFrameIndex = 0, -1
    leftSuccess,    rightSuccess    = False, False

    for i in range(0, len(filAllDataNP)):
        if (    filAllDataNP[i][0] == leftFrame):
            leftFrameIndex = i
            leftSuccess = True
        if (    filAllDataNP[i][0] == rightFrame):
            rightFrameIndex = i
            rightSuccess = True
            break
    
    if leftSuccess == False:
        print("Left Frame is invalid")
    if rightSuccess == False:
        print("Right Frame is invalid")
    if (leftSuccess == True and rightSuccess == True):
        x  = filAllDataNP[leftFrameIndex:(rightFrameIndex+1),0]
        y1 = filAllDataNP[leftFrameIndex:(rightFrameIndex+1),1]
        y2 = filAllDataNP[leftFrameIndex:(rightFrameIndex+1),2]
        y3 = filAllDataNP[leftFrameIndex:(rightFrameIndex+1),3]
        theoFrameSpan  = int((rightFrame - leftFrame) + 1)
        trueFrameSpan  = len(x)
        
        plt.close('all')   
        plt.plot(x, y1, "ro")
        plt.plot(x, y1, "k-")
        plt.grid()
        
        print("|----------PLOT FRAME ----------|")
        print("Left  Index is", leftFrameIndex)
        print("Right Index is", rightFrameIndex)
        print("")
        print("Frame Span is", theoFrameSpan, "seconds")
        print("Frame  Amt is", trueFrameSpan, "points")
        print("Δ is", theoFrameSpan - trueFrameSpan)
        print("")
        
        fraAllDataNP = np.column_stack((x, y1, y2, y3))
        fraAllDataDF = pd.DataFrame(fraAllDataNP)
        fraAllDataDF.columns = ["UnixTime", "GasData", "DateTime", "RealData"]
    else:
        print("Frame Selection Failed") 
    return fraAllDataNP, fraAllDataDF



rawAllDataNP, rawAllDataDF = importData(data)
importCheck(rawAllDataNP, rawAllDataDF)
fullRemovalIndices = dataFilterWhere(rawAllDataNP)
filAllDataNP, filAllDataDF = dataFilterCreator(rawAllDataDF, fullRemovalIndices)
leftFrame  = filAllDataNP[0][0]
rightFrame = filAllDataNP[-1][0]
fraAllDataNP, fraAllDataDF = windowSelect(filAllDataNP, leftFrame, rightFrame)



############### FUNCTION: MISSING DETERMINER ###############
def missingDataDeterminer(data):
    leftFrameUnix  = data[0][0]
    rightFrameUnix = data[-1][0] 
    spanFrameUnix  = np.arange(leftFrameUnix, rightFrameUnix+1)
    
    missingData = np.array([])
    s = set(data[:,0])
    for i in range(0, len(spanFrameUnix)):
        if spanFrameUnix[i] not in s:
            missingData = np.append(missingData, spanFrameUnix[i]) 
    print(len(missingData), "missing points from", [name for name in globals() if globals()[name] is data])

    return missingData


############### FUNCTION: ESTIMATIONS ###############
def estimateData(missingFra):
    misDT, misGas, misReal = np.array([]), np.array([]), np.array([])
    for j in missingFra:
        a = datetime.fromtimestamp(j)
        misDT = np.append(misDT, a)
        left  = j - 1
        right = j + 1
        
        if ((left in filAllDataNP[:,0]) & (right in filAllDataNP[:,0])) == True:
            leftIndex  = np.where(filAllDataNP[:,0] == left)
            rightIndex = np.where(filAllDataNP[:,0] == right)
            leftData   = filAllDataNP[leftIndex[0][0]][1]
            rightData  = filAllDataNP[rightIndex[0][0]][1]
            if (abs(leftData - rightData) <= 5.0) :
                midData = (leftData + rightData) / 2
                misGas = np.append(misGas, midData)
                misReal = np.append(misReal, False)
            else:
                midData  = None
                misGas  = np.append(misGas, midData)
                misReal = np.append(misReal, False)  
            
        else:
            midData  = None
            misGas  = np.append(misGas, midData)
            misReal = np.append(misReal, False)
    
    unsUnix= np.concatenate((fraAllDataNP[:,0], missingFra), axis = 0)
    unsGas = np.concatenate((fraAllDataNP[:,1], misGas),     axis = 0)
    unsDT  = np.concatenate((fraAllDataNP[:,2], misDT),      axis = 0)
    unsReal= np.concatenate((fraAllDataNP[:,3], misReal),    axis = 0)
    Datum = {'UnixTime': unsUnix,
             'GasData' : unsGas,
             'DateTime': unsDT,
             'RealData': unsReal}
    df = pd.DataFrame(Datum, columns = ['UnixTime', 'GasData', 'DateTime', 'RealData'])
    dfs = df.sort_values(by = ['UnixTime'], inplace = False)
    
    dfs = dfs.reset_index(drop=True)
    dfs.UnixTime = dfs.UnixTime.astype(int)
    dfs.GasData  = dfs.GasData.astype(float)
    dfs.RealData = dfs.RealData.astype(int)
    dfs = dfs[dfs.GasData != 0.0]
    #dfs = dfs[dfs.GasData.notnull()]
    estAllDataDF = dfs.reset_index(drop=True)
    estAllDataNP = estAllDataDF.to_numpy()
    nanCounter = 0
    for k in estAllDataNP[:,1]:
        if np.isnan(k) == True:
            nanCounter += 1
    return estAllDataNP, estAllDataDF, nanCounter

    
############### FUNCTION: DATA AVERAGING
def averageData(estAllDataDF, interval):
    avgAllDataDF = estAllDataDF.groupby(pd.Grouper(key='DateTime', freq=interval)).mean().dropna()
    avgAllDataDF['UnixTime'] = avgAllDataDF['UnixTime'].astype(int)
    avgAllDataDF['DateTime'] = pd.to_datetime(avgAllDataDF['UnixTime'], unit = 's')
    avgAllDataNP = avgAllDataDF.to_numpy()
    return avgAllDataNP, avgAllDataDF


    #----------Missing Data----------#
print("|----------MISSING DATA ----------|")
missingRaw = missingDataDeterminer(rawAllDataNP)
missingFil = missingDataDeterminer(filAllDataNP)
missingFra = missingDataDeterminer(fraAllDataNP)
estAllDataNP, estAllDataDF, nanCounter = estimateData(missingFra)

