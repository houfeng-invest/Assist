import zipfile
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time

def extractLogs():
    for file in os.listdir("./zips"):
        if file[-4:] == ".zip":
            print(file[:-4])
            zipName =  file[:-4]
            f = zipfile.ZipFile("./zips/%s" % file ,'r')
            for zf in f.namelist():
                f.extract(zf,"./Logs/%s" % zipName)



logsCrashData = {}
salesInfoData = {}
def readLogs():
    logsPath = './Logs1/'
    totalFile = 0
    crashkeywords = "CRASH:"
    crashkeywords = "will start"
    saleskeywords = "commitSalesInfo"
    totalCrashCount = 0
    for logDir in os.listdir(logsPath):
        if os.path.isdir(os.path.join(logsPath,logDir)):
            for logFile in os.listdir(os.path.join(logsPath,logDir)):
                if "rlterm3log_" not  in logFile:
                    continue
                logFilePath = os.path.join(logsPath,logDir,logFile)
                startDataLocation = len("rlterm3log_")
                dateStr = logFile[startDataLocation:-4]
                if len(dateStr) > 8:
                    dateStr = dateStr[-8:]
                a = datetime.datetime.strptime(dateStr,'%Y%m%d')
                # if '201708' in dateStr:
                #     continue
                dateStr =  a.strftime('%Y-%m-%d')
                print(dateStr)
                totalFile += 1
                logsCrashData.setdefault(dateStr,0)
                f = open(logFilePath,'r',encoding='utf-8')
                startInFile = 0
                lineNo = 0
                for line in f.readlines():
                    if crashkeywords in line:
                        startInFile += 1
                        if startInFile > 1 or lineNo > 15:
                            logsCrashData[dateStr] = logsCrashData[dateStr] + 1
                    lineNo = lineNo + 1

                if totalFile > 50000:
                    break
            if totalFile > 50000:
                break


                #break
            #break
    print("一共有:" + str(totalFile) + "个文件")
    # print("一共有:" + str(totalCrashCount-totalFile) + "闪退")






def analyse():

    monthData = {}
    monthSalesData = {}

    for k ,v in logsCrashData.items():
         a = datetime.datetime.strptime(k,'%Y-%m-%d')
         monthStr =  a.strftime('%Y-%m')
         monthData.setdefault(monthStr,0)
         monthData[monthStr] = monthData[monthStr] + v


    monthData = monthData
    monthDataFrame = pd.DataFrame()
    monthDataFrame["date"]=monthData.keys()
    monthDataFrame["crash"]=monthData.values()
    monthDataFrame = monthDataFrame.sort_values(['date'],ascending=[True])




    print('----mouth-----')
    print(monthDataFrame)
    monthDataFrame.describe()

    daySeries = pd.Series(logsCrashData,name='crash')
    daySeries = daySeries.sort_values()
    print('days-----')
    print(daySeries.tail())
    print(daySeries.describe())

    monthIndexs = np.arange(len(monthData))
    crashCount =  monthDataFrame['crash']

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.grid(True)
    N = len(monthIndexs)
    width = 0.1
    ax.set_ylabel('Crash')
    ax.set_xticks(monthIndexs+width)
    ax.set_xticklabels(monthDataFrame['date'])
    reg = np.polyfit(monthIndexs,crashCount,deg=2)
    ry = np.polyval(reg,monthIndexs)

    p1 = plt.bar(monthIndexs ,crashCount,width=width, color='red')

    m,b = np.polyfit(monthIndexs,crashCount,1)

    pr = plt.plot(monthIndexs,ry,'-',label="crash")
    plt.show()




if __name__ == '__main__':
   print("start...")
   readLogs()
   analyse()

