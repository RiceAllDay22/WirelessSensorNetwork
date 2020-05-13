import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


def importCheck(rawAllDataNP, rawAllDataDF):
    #Print datatypes
    print('|----------DATA CHECKER ----------|')
    print('UNIXTIME:', rawAllDataNP[0][0], type(rawAllDataNP[0][0]))
    print('GASDATA :', rawAllDataNP[0][1], type(rawAllDataNP[0][1]))
    print('REALDATA:', rawAllDataNP[0][2], type(rawAllDataNP[0][2])) 
    print('DATETIME:', rawAllDataNP[0][3], type(rawAllDataNP[0][3]), "\n")
    #Print extreme values
    print('Data Amt:', len(rawAllDataNP[:]))
    print('Gas  Min:', min(rawAllDataNP[:,1]))
    print('Gas  Max:', max(rawAllDataNP[:,1]))
    print('Unix Min:', min(rawAllDataNP[:,0]))
    print('Unix Min:', max(rawAllDataNP[:,0]))
    return


def importData(data):
    #Create columns
    UnixTime = np.array(data['UnixTime'])
    GasData  = np.array(data['GasData'])
    RealData = np.ones((len(UnixTime), 1))
    rawAllDataDF = pd.DataFrame(np.column_stack((UnixTime, GasData, RealData)))
    rawAllDataDF['DateTime'] = pd.to_datetime(rawAllDataDF.iloc[:,0], unit = 's')
    rawAllDataDF.columns     = ['UnixTime', 'GasData', 'RealData', 'DateTime']

    #Drop duplicates and change datatypes
    rawAllDataDF = rawAllDataDF.drop_duplicates(subset='UnixTime', keep='first')
    rawAllDataDF.UnixTime = rawAllDataDF.UnixTime.astype(int)
    rawAllDataDF.RealData = rawAllDataDF.RealData.astype(int)
    
    #Create dataframe
    rawAllDataNP = rawAllDataDF.to_numpy()
    return rawAllDataDF, rawAllDataNP


def dataFilterWhere(rawAllDataNP, rawAllDataDF):
    #Determine indices
    gasZerosIndices  = np.where( rawAllDataNP[:,1] == 0)
    gasLowIndices    = np.where((rawAllDataNP[:,1] <= 350) & (rawAllDataNP[:,1] > 0))
    gasHighIndices   = np.where( rawAllDataNP[:,1] >= 5000) 
    gasNegIndices    = np.where( rawAllDataNP[:,1] < 0 )
    timeZerosIndices = np.where( rawAllDataNP[:,0] == 0)
    timeLowIndices   = np.where((rawAllDataNP[:,0] <= 1576594500) & (rawAllDataNP[:,0] > 0))
    timeHighIndices  = np.where( rawAllDataNP[:,0] >= 2000000000)                            
    timeNegIndices   = np.where( rawAllDataNP[:,0] < 0)

    fullRemovalIndices = np.concatenate((
        gasZerosIndices, gasLowIndices, gasHighIndices, gasNegIndices,
        timeZerosIndices,timeLowIndices,timeHighIndices,timeNegIndices), axis = None)
        #Print removal info
    print('|----------DATA REMOVED----------|')
    print('Gas  Zeros: ', len(gasZerosIndices[0]))
    print('Gas   Lows: ', len(gasLowIndices[0]))
    print('Gas  Highs: ', len(gasHighIndices[0]))
    print('Gas   Negs: ', len(gasNegIndices[0]))
    print('Time Zeros: ', len(timeZerosIndices[0]))
    print('Time  Lows: ', len(timeLowIndices[0]))
    print('Time Highs: ', len(timeHighIndices[0]))
    print('Time  Negs: ', len(timeNegIndices[0]))
    print('Total Remd: ', (len(gasZerosIndices[0]) + len(gasLowIndices[0]) + 
        len(gasHighIndices [0]) + len(gasNegIndices[0]) + len(timeZerosIndices[0]) + 
        len(timeLowIndices[0]) + len(timeHighIndices[0]) + len(timeNegIndices[0])))
    print('Total Remd: ', len(fullRemovalIndices))

    #Create new dataframe
    filAllDataDF = rawAllDataDF[~rawAllDataDF.index.isin(fullRemovalIndices)]
    filAllDataNP = filAllDataDF.to_numpy()
    return filAllDataNP, filAllDataDF, fullRemovalIndices


def windowSelect(filAllDataNP, filAllDataDF, leftFrame, rightFrame):
    #Determine validity of selected frame
    leftFrameIndex   = np.where( filAllDataNP[:,0] == leftFrame)[0]
    rightFrameIndex  = (np.where( filAllDataNP[:,0] == rightFrame))[0]
    if leftFrameIndex.size == 1 and rightFrameIndex.size == 1 :
        
        #Create dataframe of fraAllData   
        fraAllDataDF = filAllDataDF.iloc[leftFrameIndex[0]:rightFrameIndex[0]+1,:]
        fraAllDataNP = fraAllDataDF.to_numpy()

        #Plot selected window frame
        plt.close('all')
        x  = fraAllDataNP[:,3]  
        y  = fraAllDataNP[:,1]
        fig, ax = plt.subplots()
        plt.plot_date(x, y, "r-", linewidth = 0.5)
        
        #Plot Formatting
        plt.title('Selected Frame', fontsize = 15)
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('CO2 ppm', fontsize=12)
        formatter = DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(formatter)
        plt.gcf().autofmt_xdate()#plt.plot(x, y, "k-")
        plt.grid()
        plt.show()

    else:
            print('Invalid selection')
    return fraAllDataNP, fraAllDataDF


def missingDataDeterminer(data):
    leftFrameUnix  = data[0][0]
    rightFrameUnix = data[-1][0] 
    spanFrameUnix  = np.arange(leftFrameUnix, rightFrameUnix+1)
    missingData    = np.array([])

    s = set(data[:,0])
    for i in range(0, len(spanFrameUnix)):
        if spanFrameUnix[i] not in s:
            missingData = np.append(missingData, spanFrameUnix[i]) 
    print(len(missingData), "missing points from", [name for name in globals() if globals()   
        [name] is data])
    return missingData


def estimateData(fraAllDataNP, missingFra):  
    misGas  = np.array([])
    misReal = np.zeros((len(missingFra)))
    missingFra = missingFra.astype(int) 

    #Perform estimation for every missing index
    for j in missingFra:
        left  = j - 1
        right = j + 1
        #Check that bordering points exist
        if((left in filAllDataNP[:,0])&(right in filAllDataNP[:,0]))==True:
            leftIndex  = np.where(filAllDataNP[:,0] == left)
            rightIndex = np.where(filAllDataNP[:,0] == right)
            leftData   = filAllDataNP[leftIndex[0][0]][1]
            rightData  = filAllDataNP[rightIndex[0][0]][1]
            #Check that bordering points are close in value
            if (abs(leftData - rightData) <= 1) :
                midData = (leftData + rightData) / 2
                misGas  = np.append(misGas, midData)
            else:
                misGas  = np.append(misGas, None)
        else:
            misGas  = np.append(misGas, None)
    print(missingFra)
    print(misGas)
    print(misReal)

    #Combine Estimated Data with Real Data
    estUnix = np.concatenate((fraAllDataNP[:,0], missingFra), axis = 0)    
    estGas  = np.concatenate((fraAllDataNP[:,1], misGas),     axis = 0)
    estReal = np.concatenate((fraAllDataNP[:,2], misReal),    axis = 0)
    df = pd.DataFrame(np.column_stack((estUnix, estGas, estReal)))
    df.columns     = ['UnixTime', 'GasData', 'RealData']

    dfs = df.sort_values(by = ['UnixTime'], inplace = False)
    dfs = dfs.reset_index(drop=True)
    dfs['DateTime'] = pd.to_datetime(dfs.iloc[:,0], unit = 's')
    dfs.GasData = dfs.GasData.astype(float)
    dfs.RealData = dfs.RealData.astype(int)

    #Drop Zeros and Null
    #dfs = dfs[dfs.GasData != 0.0]
    #dfs = dfs[dfs.GasData.notnull()]

    estAllDataDF = dfs
    estAllDataNP = estAllDataDF.to_numpy()
    nanCounter = estAllDataDF.GasData.isna().sum()
    return estAllDataNP, estAllDataDF, nanCounter


def averageData(estAllDataDF, interval):
    avgAllDataDF=estAllDataDF.groupby(pd.Grouper(key='DateTime',freq=interval)).mean().dropna()
    avgAllDataDF = avgAllDataDF.drop(columns=['RealData'])
    avgAllDataDF.reset_index(level=0, inplace=True)
    avgAllDataNP = avgAllDataDF.to_numpy()
    return avgAllDataNP, avgAllDataDF