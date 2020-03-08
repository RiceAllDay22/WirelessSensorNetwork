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
year, month, day =  19, 12, 17
os.chdir('C:\\Users\\adria\\OneDrive - University of Utah\\Documents\\Research\\Project 4 Network\\Continuous Data')
data = pd.read_excel(str(month) + "-" + str(day) + "-" + str(year) + '.xlsx')

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



rawAllDataNP, rawAllDataDF = importData(data)
importCheck(rawAllDataNP, rawAllDataDF)
fullRemovalIndices = dataFilterWhere(rawAllDataNP)
filAllDataNP, filAllDataDF = dataFilterCreator(rawAllDataNP, fullRemovalIndices)

leftFrame  = filAllDataNP[0][0]
rightFrame = filAllDataNP[-1][0]
fraAllDataNP, fraAllDataDF = windowSelect(filAllDataNP, leftFrame, rightFrame)

