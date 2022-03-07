############### LIBRARIES ###############
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from statistics import mean

############### DATA SELECTION ###############
year, month, day =  19, 12, 18
os.chdir("C:\\Users\\adria\\Desktop\\Continuous Data")
data = pd.read_excel(str(month) + "-" + str(day) + "-" + str(year) + '.xlsx')


############### FUNCTION: DATA IMPORT ###############
def importData(data): 
    DateTime  = []
    GasData  = np.array(data['CO2'])
    UnixTime = np.array(data['UNIXTIME'])
    
    for i in range(0, len(UnixTime)):
        a = datetime.fromtimestamp(UnixTime[i])
        DateTime.append(a)

    rawAllData = [DateTime, GasData, UnixTime]
    return rawAllData


############### FUNCTION: DATA FILTER ###############
def filterData(rawAllData): 
    global gasZerosIndices,  gasLowIndices,  gasHighIndices
    global timeZerosIndices, timeLowIndices, timeHighIndices
    global fullRemovalIndices
    gasZerosIndices = np.where(rawAllData[1] == 0)
    gasLowIndices   = np.where((rawAllData[1] <= 420) & (rawAllData[1] > 0))
    gasHighIndices  = np.where(rawAllData[1] >= 5000) 
    timeZerosIndices= np.where(rawAllData[2] == 0)
    timeLowIndices  = np.where((rawAllData[2] <= 1576594500) & (rawAllData[2] > 0))
    timeHighIndices = np.where(rawAllData[2] >= 2000000000)                                               

    fullRemovalIndices     = np.concatenate((
                                 gasZerosIndices,
                                 gasLowIndices,
                                 gasHighIndices,
                                 timeZerosIndices,
                                 timeLowIndices,
                                 timeHighIndices), axis = None)
    def printout1():
        print("|----------DATA REMOVED----------|")
        print("Gas  Zeros: ", len(gasZerosIndices[0]))
        print("Gas   Lows: ", len(gasLowIndices[0]))
        print("Gas  Highs: ", len(gasHighIndices[0]))
        print("Time Zeros: ", len(timeZerosIndices[0]))
        print("Time   Low: ", len(timeLowIndices[0]))
        print("Time  High: ", len(timeHighIndices[0]))
        print("Total Remd: ", (len(gasZerosIndices[0]) + len(gasLowIndices[0]) + len(gasHighIndices[0]) + len(timeZerosIndices[0]) + len(timeLowIndices[0]) + len(timeHighIndices[0])))
        print("Total Remd: ", len(fullRemovalIndices))
        print("")
    printout1()

    newDateTime, newGasData, newUnixTime = [], [], []
    for i in range(0, len(rawAllData[0])):
        if i not in fullRemovalIndices:
            a = rawAllData[0][i]
            b = rawAllData[1][i]
            c = rawAllData[2][i]
            newDateTime.append(a)
            newGasData.append(b)
            newUnixTime.append(c)
    
    newAllData = [newDateTime, newGasData, newUnixTime]
    
    def printout2():
        print("|----------DATA SUMMARY----------|")
        print("Raw: ", len(rawAllData[0]), len(rawAllData[1]), len(rawAllData[2]))
        print("New: ", len(newAllData[0]), len(newAllData[1]), len(newAllData[2]))
        print("Δ  : ", len(rawAllData[0]) - len(newAllData[0]))
        print("")
    printout2()
    
    return newAllData


############### FUNCTION: FRAME SELECTION ###############
def windowSelect(newAllData, leftFrame, rightFrame):
    leftFrameIndex, rightFrameIndex = 0, -1
    leftSuccess, rightSuccess = False, False
    for i in range(0, len(newAllData[0])):
        if (    newAllData[0][i].year   == leftFrame.year    and
                newAllData[0][i].month  == leftFrame.month   and
                newAllData[0][i].day    == leftFrame.day     and
                newAllData[0][i].hour   == leftFrame.hour    and 
                newAllData[0][i].minute == leftFrame.minute  and
                newAllData[0][i].second == leftFrame.second):
            leftFrameIndex = i
            leftSuccess = True
        if (    newAllData[0][i].year   == rightFrame.year   and
                newAllData[0][i].month  == rightFrame.month  and
                newAllData[0][i].day    == rightFrame.day    and      
                newAllData[0][i].hour   == rightFrame.hour   and 
                newAllData[0][i].minute == rightFrame.minute and
                newAllData[0][i].second == rightFrame.second):
            rightFrameIndex = i
            rightSuccess = True
    
    if leftSuccess == False:
        print("Left Frame is invalid")
    if rightSuccess == False:
        print("Right Frame is invalid")
    
    if (leftSuccess == True and rightSuccess == True): 
        x  = np.array(newAllData[0][leftFrameIndex:rightFrameIndex+1])
        y1 = np.array(newAllData[1][leftFrameIndex:rightFrameIndex+1])
        y2 = np.array(newAllData[2][leftFrameIndex:rightFrameIndex+1])
        
        plt.plot(x, y1, "ro")
        plt.plot(x, y1, "k-")
        plt.grid()
    
        theoFrameSpan  = rightFrame - leftFrame
        trueFrameSpan  = len(x)
        frameAllData = np.concatenate([[x], [y1], [y2]], axis = 0)

        def printout3():
            print("|----------PLOT FRAME ----------|")
            print("Left  Index is ", leftFrameIndex)
            print("Right Index is ", rightFrameIndex)
            print("")
            print("Span is ", theoFrameSpan.seconds + 1, " seconds")
            print("Amt  is ", trueFrameSpan, " points")
            print("Δ    is ", theoFrameSpan.seconds + 1 - trueFrameSpan)
            print("")
        printout3()
        
    else:
        print("Frame Selection Failed")  
        
    return frameAllData


############### FUNCTION: Missing Data Determiner ###############
def missingDataDeterminer(data):
    leftFrame  = data[0][0]
    rightFrame = data[0][-1] 
    leftFrameUnix  = datetime.timestamp(leftFrame)
    rightFrameUnix = datetime.timestamp(rightFrame)
    spanFrameUnix  = np.arange(leftFrameUnix, rightFrameUnix+1)
    
    missingData = []
    s = set(data[2])
    
    for i in range(0, len(spanFrameUnix)):
        if spanFrameUnix[i] not in s:
            missingData.append(spanFrameUnix[i])
    print(len(missingData), "missing points from", [name for name in globals() if globals()[name] is data])

    return missingData


############### MAIN CODE ###############
plt.close('all')
rawAllData = importData(data)
newAllData = filterData(rawAllData)


leftFrame  = newAllData[0][3500]
rightFrame = newAllData[0][-1]
#leftFrame  = datetime.fromtimestamp(1576720628.0)
#rightFrame = datetime.fromtimestamp(1576728628.0)
#leftFrame  = datetime(2019, 12, 17, 16, 44, 40)
#rightFrame = datetime(2019, 12, 17, 10, 20, 25)
#leftFrame  = newAllData[0][280]
#rightFrame = newAllData[0][300]
frameAllData = windowSelect(newAllData, leftFrame, rightFrame)

print("|----------MISSING DATA ----------|")
missingRaw  = missingDataDeterminer(rawAllData)
missingNew  = missingDataDeterminer(newAllData)
missingFrame= missingDataDeterminer(frameAllData)


a = rawAllData[2]
element, count = np.unique(a, return_counts = True)
resultA = np.asarray((element, count))




############### ESTIMATIONS FOR MISSING ###############
misDT, misGas, misUnix = [], [],[]
estDT, estGas, estUnix = np.array([]), np.array([]), np.array([])
floatGasData, estBool = np.array([]), np.array([])

for i in range(0, len(missingFrame)):
    a = datetime.fromtimestamp(missingFrame[i])
    b = int(missingFrame[i])
    misDT = np.append(misDT, a)
    misUnix.append(b)
    
for j in range(0, len(frameAllData[1])):
    a = float(frameAllData[1][j])
    floatGasData = np.append(floatGasData, a)
    estBool = np.append(estBool, False)

for k in misUnix:
    left  = k-1
    right = k+1
    if ((left in rawAllData[2]) & (right in rawAllData[2])) == True:
        leftIndex  = np.where(rawAllData[2] == left)
        rightIndex = np.where(rawAllData[2] == right)
        leftData   = rawAllData[1][leftIndex]
        rightData  = rawAllData[1][rightIndex]
        midData    = (leftData[0] + rightData[0]) / 2
        misGas = np.append(misGas, midData)
        estBool = np.append(estBool, True)
        
          
#plt.plot(misDT, misGas, "o")

estDT   = np.concatenate((frameAllData[0], misDT  ))
estGas  = np.concatenate((floatGasData,    misGas ))
estUnix = np.concatenate((frameAllData[2], misUnix))

Datum = {'DT'  : estDT,
          'Gas' : estGas,
          'Unix': estUnix,
          'Bool': estBool}
#df = pd.DataFrame(Datum, columns = ['DT', 'Gas', 'Unix', 'Bool'])
#dfs = df.sort_values(by = ['Unix'], inplace = False)
#dfsr = dfs.reset_index(drop=True)

# npdf = dfsr.to_numpy()



