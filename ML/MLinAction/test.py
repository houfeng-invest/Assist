import ML.MLinAction.kNN as kNN
group , labels = kNN.createDataSet()
print(group)

kNN.classify0([0,0],group,labels,3)

#datingDataMat,datingLabels = kNN.file2matrix('./data/datingTestSet2.txt')

kNN.drawDatingData()