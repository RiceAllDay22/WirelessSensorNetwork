############### LIBRARIES ###############
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime
from statistics import mean

#NP = DF.to_numpy()
#DF = pd.DataFrame(NP)


############### DATA SELECTION ###############
year, month, day =  19, 12, 21.1
os.chdir("C:\\Users\\adria\\Desktop\\Continuous Data")
data = pd.read_excel(str(month) + "-" + str(day) + "-" + str(year) + '.xlsx')


############### FUNCTION: DATA IMPORT ###############
def importData(data):
    floatUnixTime, floatGasData, DateTime, RealData = np.array([]), np.array([]), np.array([]), np.array([])
    UnixTime = np.array(data['UNIXTIME'])
    GasData  = np.array(data['CO2'])
    
    for i in range(0, len(UnixTime)):
        a = datetime.fromtimestamp(UnixTime[i])
        b = float(UnixTime[i])
        c = float(GasData[i]) 
        floatUnixTime = np.append(floatUnixTime, b)
        floatGasData  = np.append(floatGasData,  c)
        DateTime = np.append(DateTime, a)
        RealData = np.append(RealData, True)
    
    
    rawAllDataNP = np.column_stack((floatUnixTime, floatGasData, DateTime, RealData))
    rawAllDataDF = pd.DataFrame(rawAllDataNP)  
    rawAllDataDF = pd.DataFrame({'UnixTime': rawAllDataNP[:,0], 
                                 'GasData' : rawAllDataNP[:,1],
                                 'DateTime': rawAllDataNP[:,2],
                                 'RealData': rawAllDataNP[:,3]})
    rawAllDataDF = rawAllDataDF.drop_duplicates(subset='UnixTime', keep='first')
    rawAllDataNP = rawAllDataDF.to_numpy()
    return rawAllDataNP, rawAllDataDF
#rawAllDataNP, rawAllDataDF = importData(data)

def importCheck(rawAllDataNP, rawAllDataDF):
    print('')
    print('|----------DATA CHECKER ----------|')
    print(rawAllDataNP[0][0])
    print(rawAllDataNP[0][1])
    print(rawAllDataNP[0][2])
    print(rawAllDataNP[0][3])
    
    print(type(rawAllDataNP[0][0]))
    print(type(rawAllDataNP[0][1]))
    print(type(rawAllDataNP[0][2]))
    print(type(rawAllDataNP[0][3]))
    
    print('')
#importCheck(rawAllDataNP, rawAllDataDF)

def columnExtraction():
    global rawAllDataNP_DateTime, rawAllDataNP_Gas, rawAllDataNP_UnixTime, rawAllDataNP_RealData
    global rawAllDataDF_DateTime, rawAllDataDF_Gas, rawAllDataDF_UnixTime, rawAllDataDF_RealData
    
    rawAllDataNP_DateTime = rawAllDataNP[:,0]
    rawAllDataNP_Gas      = rawAllDataNP[:,1]
    rawAllDataNP_UnixTime = rawAllDataNP[:,2]
    rawAllDataNP_RealData = rawAllDataNP[:,3]
    
    rawAllDataDF_DateTime = rawAllDataDF[0]
    rawAllDataDF_Gas      = rawAllDataDF[1]
    rawAllDataDF_UnixTime = rawAllDataDF[2]
    rawAllDataDF_RealData = rawAllDataDF[3]
#columnExtraction()


############### FUNCTION: DATA FILTER ###############
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
    
    def printFilter():
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
    printFilter()
    return fullRemovalIndices
#fullRemovalIndices = dataFilterWhere(rawAllDataNP)


def dataFilterCreator(rawAllDataNP, fullRemovalIndices):
    filUnixTime, filGasData, filDateTime, filRealData = np.array([]), np.array([]), np.array([]), np.array([])
    for i in range(0, len(rawAllDataNP[:,0])):
        if i not in fullRemovalIndices:
            a = rawAllDataNP[i][0]
            b = rawAllDataNP[i][1]
            c = rawAllDataNP[i][2]
            d = rawAllDataNP[i][3]
            filUnixTime = np.append(filUnixTime, a)
            filGasData  = np.append(filGasData,  b)
            filDateTime = np.append(filDateTime, c)
            filRealData = np.append(filRealData, d)
    
    filAllDataNP = np.column_stack((filUnixTime, filGasData, filDateTime, filRealData))
    filAllDataDF = pd.DataFrame(filAllDataNP) 
    filAllDataDF.columns = ["UnixTime", "GasData", "DateTime", "RealData"]
    
    return filAllDataNP, filAllDataDF
#filAllDataNP, filAllDataDF = dataFilterCreator(rawAllDataNP, fullRemovalIndices)


############### FUNCTION: FRAME SELECTION ###############
def windowSelect(filAllDataNP, leftFrame, rightFrame):
    leftFrameDT  = datetime.fromtimestamp(leftFrame)
    rightFrameDT = datetime.fromtimestamp(rightFrame)
    leftFrameIndex, rightFrameIndex = 0, -1
    leftSuccess,    rightSuccess = False, False

    for i in range(0, len(filAllDataNP)):
        if (    filAllDataNP[i][2].year   == leftFrameDT.year    and
                filAllDataNP[i][2].month  == leftFrameDT.month   and
                filAllDataNP[i][2].day    == leftFrameDT.day     and
                filAllDataNP[i][2].hour   == leftFrameDT.hour    and 
                filAllDataNP[i][2].minute == leftFrameDT.minute  and
                filAllDataNP[i][2].second == leftFrameDT.second):
            leftFrameIndex = i
            leftSuccess = True
        if (    filAllDataNP[i][2].year   == rightFrameDT.year   and
                filAllDataNP[i][2].month  == rightFrameDT.month  and
                filAllDataNP[i][2].day    == rightFrameDT.day    and      
                filAllDataNP[i][2].hour   == rightFrameDT.hour   and 
                filAllDataNP[i][2].minute == rightFrameDT.minute and
                filAllDataNP[i][2].second == rightFrameDT.second):
            rightFrameIndex = i
            rightSuccess = True
    
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
        
        def printFrame():
            print("|----------PLOT FRAME ----------|")
            print("Left  Index is", leftFrameIndex)
            print("Right Index is", rightFrameIndex)
            print("")
            print("Frame Span is", theoFrameSpan, "seconds")
            print("Frame  Amt is", trueFrameSpan, "points")
            print("Δ is", theoFrameSpan - trueFrameSpan)
            print("")
        printFrame()
        
        fraAllDataNP = np.column_stack((x, y1, y2, y3))
        fraAllDataDF = pd.DataFrame(fraAllDataNP)
        fraAllDataDF.columns = ["UnixTime", "GasData", "DateTime", "RealData"]
    else:
        print("Frame Selection Failed") 
    return fraAllDataNP, fraAllDataDF


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


#########################################
############### MAIN CODE ###############
#########################################
    

    #----------Import and Filter Data----------#
rawAllDataNP, rawAllDataDF = importData(data)
importCheck(rawAllDataNP, rawAllDataDF)
fullRemovalIndices = dataFilterWhere(rawAllDataNP)
filAllDataNP, filAllDataDF = dataFilterCreator(rawAllDataNP, fullRemovalIndices)

    #----------Frame Data----------#
leftFrame  = filAllDataNP[0][0]
rightFrame = filAllDataNP[-1][0]
    #leftFrame  = 1576647882.0
    #leftFrame  = datetime(2019, 12, 17, 22, 44, 42).timestamp()
fraAllDataNP, fraAllDataDF = windowSelect(filAllDataNP, leftFrame, rightFrame)

    #----------Missing Data----------#
print("|----------MISSING DATA ----------|")
missingRaw = missingDataDeterminer(rawAllDataNP)
missingFil = missingDataDeterminer(filAllDataNP)
missingFra = missingDataDeterminer(fraAllDataNP)
estAllDataNP, estAllDataDF, nanCounter = estimateData(missingFra)



    #----------Cut Out Data----------#
cutAllDataDF = estAllDataDF.dropna()
cutAllDataNP = cutAllDataDF.to_numpy()


    #----------Average Data----------#
#avgAllDataNP1, avgAllDataDF1 = averageData(estAllDataDF, '10s')
#avgAllDataNP2, avgAllDataDF2 = averageData(estAllDataDF, '30s')
#avgAllDataNP3, avgAllDataDF3 = averageData(estAllDataDF, '60s')

avgAllDataNP1, avgAllDataDF1 = averageData(cutAllDataDF, '10s')
avgAllDataNP2, avgAllDataDF2 = averageData(cutAllDataDF, '30s')
avgAllDataNP3, avgAllDataDF3 = averageData(cutAllDataDF, '60s')

    #----------Summarize Data----------#
def printNewSummary():
    print('')
    print('|----------NEW DATA SUMMARY----------|')
    print('RawNP: ', len(rawAllDataNP[:,0]), len(rawAllDataNP[:,1]), len(rawAllDataNP[:,2]), len(rawAllDataNP[:,3]))
    print('RawDF: ', len(rawAllDataDF[['UnixTime']]), len(rawAllDataDF[['GasData']]), len(rawAllDataDF[['DateTime']]), len(rawAllDataDF[['RealData']]))
    print('FilNP: ', len(filAllDataNP[:,0]), len(filAllDataNP[:,1]), len(filAllDataNP[:,2]), len(filAllDataNP[:,3]))
    print('FilDF: ', len(filAllDataDF[['UnixTime']]), len(filAllDataDF[['GasData']]), len(filAllDataDF[['DateTime']]), len(filAllDataDF[['RealData']]))
    print('Δ    : ', len(rawAllDataNP[:,0]) - len(filAllDataNP[:,0]), "points were filtered out")
    print('')
    print('Should Have:', int((filAllDataNP[-1][0] - filAllDataNP[0][0])+1), "points in data")
    print('Should Have:', int((fraAllDataNP[-1][0] - fraAllDataNP[0][0])+1), "points in frame")
    print('')
    print('FraNP: ', len(fraAllDataNP[:,0]), len(fraAllDataNP[:,1]), len(fraAllDataNP[:,2]), len(fraAllDataNP[:,3]))
    print('FraDF: ', len(fraAllDataDF[['UnixTime']]), len(fraAllDataDF[['GasData']]), len(fraAllDataDF[['DateTime']]), len(fraAllDataDF[['RealData']]))
    print('EstNP: ', len(estAllDataNP[:,0]), len(estAllDataNP[:,1]), len(estAllDataNP[:,2]), len(estAllDataNP[:,3]))
    print('EstDF: ', len(estAllDataDF[['UnixTime']]), len(estAllDataDF[['GasData']]), len(estAllDataDF[['DateTime']]), len(estAllDataDF[['RealData']]))
    print('Δ    : ', len(estAllDataDF[['UnixTime']]) - len(fraAllDataDF[['UnixTime']]), 'total were added in')
    print('nan  : ', nanCounter, 'are nan values')
    print('Thus : ', ((len(estAllDataDF[['UnixTime']]) - len(fraAllDataDF[['UnixTime']])) - nanCounter), 'real estimated points added')
    print('')
    print('CutNP: ', len(cutAllDataNP[:,0]), len(cutAllDataNP[:,1]), len(cutAllDataNP[:,2]), len(cutAllDataNP[:,3]))
    print('CutDF: ', len(cutAllDataDF[['UnixTime']]), len(cutAllDataDF[['GasData']]), len(cutAllDataDF[['DateTime']]), len(cutAllDataDF[['RealData']]))
    print('AvgNP: ', len(avgAllDataNP1[:,0]), len(avgAllDataNP1[:,1]), len(avgAllDataNP1[:,2]), len(avgAllDataNP1[:,3]))
    print('AvgDF: ', len(avgAllDataDF1[['UnixTime']]), len(avgAllDataDF1[['GasData']]), len(avgAllDataDF1[['DateTime']]), len(avgAllDataDF1[['RealData']]))
printNewSummary()

    #----------Plotting----------#
def plottingEst():
    plt.close('all')
    fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.set_facecolor("lightgrey")
    ax2.set_facecolor("lightgrey")
    ax3.set_facecolor("lightgrey")
    ax4.set_facecolor("lightgrey")
    fig1.patch.set_facecolor('darkgrey')
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    
    ax1.plot(estAllDataNP[:,0],  estAllDataNP[:,1],  'k')
    ax1.plot(avgAllDataNP1[:,0], avgAllDataNP1[:,1], 'lime')
    ax2.plot(estAllDataNP[:,0],  estAllDataNP[:,1],  'k')
    ax2.plot(avgAllDataNP2[:,0], avgAllDataNP2[:,1], 'r')
    ax3.plot(estAllDataNP[:,0],  estAllDataNP[:,1],  'k')
    ax3.plot(avgAllDataNP3[:,0], avgAllDataNP3[:,1], 'b')
#plottingEst()

def plottingCut():
    plt.close('all')
    fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.set_facecolor("lightgrey")
    ax2.set_facecolor("lightgrey")
    ax3.set_facecolor("lightgrey")
    ax4.set_facecolor("lightgrey")
    fig1.patch.set_facecolor('darkgrey')
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    
    ax1.plot(cutAllDataNP[:,0],  cutAllDataNP[:,1], 'k')
    ax1.plot(avgAllDataNP1[:,0], avgAllDataNP1[:,1],'lime')
    ax2.plot(cutAllDataNP[:,0],  cutAllDataNP[:,1], 'k')
    ax2.plot(avgAllDataNP2[:,0], avgAllDataNP2[:,1],'r')
    ax3.plot(cutAllDataNP[:,0],  cutAllDataNP[:,1], 'k')
    ax3.plot(avgAllDataNP3[:,0], avgAllDataNP3[:,1],'b')
plottingCut()

    #----------Save File----------#
#avgAllDataDF3.to_excel("Average.xlsx", index = None, header=True)

    
############### END OF OFFICIAL CODE ############### 

counter = 0
for p in estAllDataNP[:,3]:
    if p == 0.0:
        counter += 1


# plt.close('all')
# sns.lmplot(x = 'UnixTime', y ='GasData', 
#             data = estAllDataDF, fit_reg = False, 
#             hue = 'RealData', legend = False,
#             palette='Set1',
#             scatter_kws={"s": 100})

# plt.plot(estAllDataNP[:,0], estAllDataNP[:,1], 'k')
# plt.grid()


    
