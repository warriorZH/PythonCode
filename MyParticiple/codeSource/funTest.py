#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: funTest.py
#description: test code
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-3-5
#log:

from MMSEG import *
import os
import commands

#lineCounter = 0
#wordfilepath = "/home/warrior/gitDir/PythonCode/MyParticiple/dataSource/gold/pku_training_words.utf8"
#storageResultpath = "/home/warrior/gitDir/PythonCode/MyParticiple/mmseg_result.utf8"
#getPartDatapath = "/home/warrior/gitDir/PythonCode/MyParticiple/dataSource/testing/pku_test.utf8"
#getDataFile = open(getPartDatapath, 'r')
#storDataFile = open(storageResultpath, 'w')
#mmseg = MMSEG()
#mmseg.getwordsDict(wordfilepath)

#wordelem2 = getDataFile.readline()
#mmseg.MMSEGStep1MaxThreeLength(wordelem2, mmseg.wordList)
#while(wordelem2):
#    for i in mmseg.sentencePartWordList:
#        storDataFile.write(i+"  ")
#    storDataFile.write("\n")
#    wordelem2 = getDataFile.readline()
#    mmseg.MMSEGStep1MaxThreeLength(wordelem2, mmseg.wordList)
#    lineCounter+=1
#    print "manage %d lines" % lineCounter
#storDataFile.close()
#getDataFile.close()

status = ""
result = ""
status, result = commands.getstatusoutput("python testcode.py")
print result
