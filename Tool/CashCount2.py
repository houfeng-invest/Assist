import datetime
import os
import shutil
import zipfile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import openpyxl

def extractLogs():
    for file in os.listdir("./zips"):
        if file[-4:] == ".zip":
            print(file[:-4])
            zipName = file[:-4]
            f = zipfile.ZipFile("./zips/%s" % file, 'r')
            for zf in f.namelist():
                f.extract(zf, "./Logs/%s" % zipName)


filesData = {}

logsCrashData = {}
salesInfoData = {}
ipadData = {}
repeatCount = 0

cidsData = {}

maxDayCount = 0

mouthAndClient = {}


def readLogs():
    logsPath = './Logs/'
    testPaths = './LogsTest/test/'
    totalFile = 0
    crashkeywords = "CRASH:"
    crashkeywords = "will start"
    saleskeywords = "commit sales info OK!"
    updateIposKeywords = "[RLUpdateView alertView:clickedButtonAtIndex:]"
    totalCrashCount = 0
    for logDir in os.listdir(logsPath):
        if os.path.isdir(os.path.join(logsPath, logDir)) and logDir[0] != '.':
            for logFile in os.listdir(os.path.join(logsPath, logDir)):

                if "rlterm3log_" not in logFile:
                    continue

                logFilePath = os.path.join(logsPath, logDir, logFile)

                startDataLocation = len("rlterm3log_")
                dateStr = logFile[startDataLocation:-4]
                if len(dateStr) > 8:
                    dateStr = dateStr[-8:]

                a = datetime.datetime.strptime(dateStr, '%Y%m%d')
                # if '201708' in dateStr:
                #     continue
                dateStr = a.strftime('%Y-%m-%d')
                mouthStr = a.strftime('%Y-%m')
                print(dateStr)
                totalFile += 1
                logsCrashData.setdefault(dateStr, 0)
                salesInfoData.setdefault(dateStr, 0)
                mouthAndClient.setdefault(mouthStr, {})
                f = open(logFilePath, 'r', encoding='utf-8')
                startInFile = 0
                lineNo = 0
                dateDevStr = None
                accesskey = None
                for line in f.readlines():
                    if 'accesskey":"' in line:
                        aa = 'ipA16914F0-A856-4143-802F-A7EAC86FBBFD'
                        l1 = line.find('accesskey":"')
                        l1 = l1 + len('accesskey":"')
                        l2 = l1 + len(aa)
                        subStr = line[l1:l2]
                        if '123ABC' in subStr:
                            subStr = '123ABC'
                        accesskey = subStr
                        dateDevStr = dateStr + subStr
                        print(dateDevStr)

                        break

                if dateDevStr != None:
                    filesData.setdefault(dateDevStr, 0)
                    if filesData[dateDevStr] > 0:
                        print(dateDevStr)
                        print("have some dev and some day....")
                        global repeatCount
                        repeatCount = repeatCount + 1
                        continue
                    else:
                        filesData[dateDevStr] = 1
                if accesskey != None:
                    ipadData.setdefault(accesskey, 0)
                    if '2017-03-07' in dateStr:
                        global maxDayCount
                        newName = 'rlterm3log_%s_%d.txt' % (dateStr, maxDayCount)
                        shutil.copyfile(logFilePath, os.path.join(testPaths, newName))
                        maxDayCount += 1

                clientid = None
                client_detail_id = None
                f.seek(0)
                for line in f.readlines():
                    if '"clientid":' in line:
                        l = line.find('"clientid":')
                        clid = line[l + len('"clientid":'):l + len('"clientid":') + 4]
                        clid = clid.replace('"', '')
                        clid = clid.replace(',', '')
                        clientid = clid
                    if '"client_detail_id":' in line:
                        l = line.find('"client_detail_id":')
                        clid = line[l + len('"client_detail_id":'):l + len('"client_detail_id":') + 3]
                        clid = clid.replace('"', '')
                        clid = clid.replace(',', '')
                        client_detail_id = clid
                        print(clid)
                    if 'clientID=' in line:
                        l = line.find('clientID=')
                        clid = line[l+len('clientID='):l+len('clientID=')+3]
                        clid = clid.replace(' ','')
                        clid = clid.replace(',','')
                        clientid = clid
                    if 'clientDetailID=' in line:
                        l = line.find('clientDetailID=')
                        clid = line[l+len('clientDetailID='):l+len('clientDetailID=')+1]
                        clid = clid.replace(' ','')
                        clid = clid.replace(',','')
                        client_detail_id = clid


                    if client_detail_id != None and clientid != None:
                        break
                idsStr = None



                if client_detail_id != None and clientid != None:
                    idsStr = '%s-%s' % (clientid, client_detail_id)
                    print(idsStr)
                    cidsData.setdefault(idsStr, 0)

                f.seek(0)
                updateIpos = False
                for line in f.readlines():

                    if updateIposKeywords in line:
                        updateIpos = True

                    if crashkeywords in line:
                        startInFile += 1
                        if updateIpos:
                            print("update ipos ..........")
                            updateIpos = False
                        else:
                            if startInFile > 1 or lineNo > 15:
                                # logsCrashData[dateStr] = logsCrashData[dateStr] + 1
                                # if accesskey != None:
                                #     ipadData[accesskey] = ipadData[accesskey] + 1
                                if idsStr != None:
                                    print(cidsData)
                                    cidsData[idsStr] = cidsData[idsStr] + 1
                                    mouthAndClient[mouthStr].setdefault(idsStr, 0)
                                    mouthAndClient[mouthStr][idsStr] = mouthAndClient[mouthStr][idsStr] + 1

                    if saleskeywords in line:
                        salesInfoData[dateStr] = salesInfoData[dateStr] + 1
                    lineNo = lineNo + 1
                f.close()
                if totalFile > 500000:
                    break
            if totalFile > 500000:
                break


                # break
                # break
    print("一共有:" + str(totalFile) + "个文件" + "重复文件有 " + str(repeatCount) + "个")
    # print("一共有:" + str(totalCrashCount-totalFile) + "闪退")


def compare_client(x, y):
    xStr = x[0].replace('-', '')
    yStr = y[0].replace('-', '')
    return int(xStr) - int(yStr)


def analyseExcelData():
    df = pd.read_excel('test.xlsx','Sheet1')
    df.plot()
    plt.show()
    print(df.head())


def getExcelData():
    mArr = sorted(mouthAndClient.items(), key=lambda d: d[0])
    mIndex = []
    newData = []
    clientIndex = sorted(cidsData.keys())
    for m, v in mArr:
        nV = sorted(v.items(), key=lambda d: d[0])
        print(nV)
        mIndex.append(m)
        aa = {}
        aa[m] = nV
        newData.append(aa)

    print(newData)
    twoDData = np.zeros((len(mIndex),len(clientIndex)))

    i = 0
    for m in mIndex:
        j = 0
        for c in clientIndex:
            if m in mouthAndClient and c in mouthAndClient[m]:
                twoDData[i][j] = mouthAndClient[m][c]
            j = j + 1
        i = i + 1

    print(twoDData)

    twoDf = pd.DataFrame(twoDData,index=mIndex,columns=clientIndex)
    print(twoDf)
    writer = pd.ExcelWriter('test.xlsx')
    twoDf.to_excel(writer,'Sheet1')
    writer.save()
    # print(mArr)
    print(mIndex)
    print(clientIndex)

def analyse():


    monthData = {}
    monthSalesData = {}

    for k, v in logsCrashData.items():
        a = datetime.datetime.strptime(k, '%Y-%m-%d')
        monthStr = a.strftime('%Y-%m')
        monthData.setdefault(monthStr, 0)
        monthData[monthStr] = monthData[monthStr] + v

        monthSalesData.setdefault(monthStr, 0)
        monthSalesData[monthStr] = monthSalesData[monthStr] + salesInfoData[k]

    monthData = monthData
    monthDataFrame = pd.DataFrame()
    monthDataFrame["date"] = monthData.keys()
    monthDataFrame["crash"] = monthData.values()
    monthDataFrame['sales'] = monthSalesData.values()
    monthDataFrame = monthDataFrame.sort_values(['date'], ascending=[True])
    print(monthDataFrame)

    daySeries = pd.Series(logsCrashData, name='crash')

    print('mouth-----')
    monthDataFrame.describe()

    print('days-----')
    print(daySeries.sort_values().tail())
    print(daySeries.describe())

    monthIndexs = np.arange(len(monthData))
    salesCount = monthDataFrame['sales']
    crashCount = monthDataFrame['crash']
    print(monthDataFrame['crash'].sum())

    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # plt.grid(True)
    # N = len(monthIndexs)
    # width = 0.1
    # ax.set_ylabel('Times')
    # ax.set_xlabel('Month')
    # ax.set_xticks(monthIndexs + width)
    # ax.set_xticklabels(monthDataFrame['date'])
    # reg = np.polyfit(monthIndexs, crashCount, deg=2)
    # ry = np.polyval(reg, monthIndexs)
    #
    # p1 = plt.bar(monthIndexs, crashCount, width=width, color='red')
    #
    # # m,b = np.polyfit(monthIndexs,crashCount,1)
    #
    # pr = plt.plot(monthIndexs, ry, '-', label="Crash Count")
    #
    # psales = plt.plot(monthIndexs, salesCount, '--', label="Sales Count")
    #
    # for (m, n) in zip(monthIndexs, crashCount):
    #     print(m, n)
    #     # print("%i : %i" % m,n)
    #     count = n
    #     plt.text(m - 0.15, n + 10, '%d' % n)
    #
    # plt.legend()
    # plt.show()

    ipadFrame = pd.DataFrame()
    ipadFrame['ipad'] = cidsData.keys()
    ipadFrame['crash'] = cidsData.values()
    ipadFrame = ipadFrame.sort_values(['crash'], ascending=[False])
    print(ipadFrame)
    print(ipadFrame.describe())
    print(monthDataFrame['crash'].sum())

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    plt.grid(True)
    ipadN = len(ipadFrame['ipad'])
    print(ipadN)
    ipadIndex = np.arange(ipadN)
    ipadCrashCount = ipadFrame['crash']
    print(ipadIndex)
    print(ipadCrashCount)
    ax2.set_ylabel('Times')
    ax2.set_xlabel('client')
    ax2.set_xticklabels(ipadFrame['ipad'])
    p2 = plt.bar(ipadIndex, ipadCrashCount, width=0.1, color='red')
    plt.show()





    # fig2 = plt.figure()
    # ax2 = fig.add_subplot(111)
    # x = np.array([datetime.datetime.strptime(dateStr,'%Y-%m-%d') for dateStr in daySeries.index])
    # x = np.arange(len(x))
    # y = np.array(daySeries.values)
    # print('---------------')
    # print(y)
    # ax2.plot(x,y)
    #
    # m,b = np.polyfit(x,y,1)
    # plt.plot(x,m*x+b,'-')
    # plt.show()

    # fig2 = plt.figure()
    # ax2 = fig.add_subplot(212)
    # x = monthDataFrame['sales']
    # y = monthDataFrame['crash']
    # ax2.scatter(x,y)
    # plt.show()


if __name__ == '__main__':
    print("start...")
    #extractLogs()
    readLogs()
    getExcelData()
    analyseExcelData()
