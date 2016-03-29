#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: statisticalWordCount.py
#description: statistic word count of pku_training.utf8
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-3-6
#log:


import re
import collections


trainDataPath = "/home/warrior/gitDir/PythonCode/MyParticiple/dataSource/training/pku_training.utf8"
staticalResultPath = "/home/warrior/gitDir/PythonCode/MyParticiple/codeSource/staticalResult.utf8"
trainDataFile = open(trainDataPath,'r')
staticalResultFile = open(staticalResultPath,'w')
trainData = trainDataFile.read()
rPattern = re.compile('''\s+''')
trainDataList = rPattern.split(trainData)
trainDataDictList = collections.Counter(trainDataList)
trainDataDictSortedList = sorted(trainDataDictList.items(), key=lambda d:d[1], reverse=True)
for item in trainDataDictSortedList:
    staticalResultFile.write(item[0])
    staticalResultFile.write("     ") #中间空5个空格
    staticalResultFile.write(str(item[1]))
    staticalResultFile.write('\n')

trainDataFile.close()
staticalResultFile.close()
print "run over!!"
