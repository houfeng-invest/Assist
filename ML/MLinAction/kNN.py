import numpy as np
import operator
import matplotlib.pyplot as plt
from os import  listdir

def createDataSet():
    group = np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels


def classify0(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inX,(dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    print(sqDiffMat)
    sqDistances = sqDiffMat.sum(axis=1)
    print(sqDistances)
    distances = sqDistances**0.5
    print(distances)
    sortedDistIndicies = distances.argsort()
    print(sortedDistIndicies)
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] =classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    print(sortedClassCount)
    return sortedClassCount[0][0]


def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = np.zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = np.zeros(np.shape(dataSet))
    # print(np.shape(dataSet))
    # print(normDataSet)
    m = dataSet.shape[0]
    normDataSet = dataSet - np.tile(minVals,(m,1))
    # print(np.tile(minVals,(m,1)))
    normDataSet = normDataSet / np.tile(ranges,(m,1))
    print(normDataSet)
    return normDataSet,ranges,minVals

def img2vector(filename):
    returnVect = np.zeros((1,1024))
    print(returnVect)
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(lineStr[j])
    print(returnVect)
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('./data/digits/trainingDigits')
    m = len(trainingFileList)
    trainingMat = np.zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split("_")[0])
        hwLabels.append(classNumStr)





def main():
    # group,labels = createDataSet()
    # print(group)
    # print(group.shape)
    # classify0([0,0],group,labels,3)
    # datingDataMat ,datingLabels = file2matrix('./data/datingTestSet2.txt')
    # print(datingDataMat)
    # print(datingLabels)
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0*np.array(datingLabels),15.0*np.array(datingLabels))
    # plt.show()

    # autoNorm(datingDataMat)

    testVector = img2vector('./data/digits/testDigits/0_13.txt')

if __name__ == "__main__":
    main()