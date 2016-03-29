#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: crfppTest.py
#description: use crf++ algorithm tool to optimize the mmseg result
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-3-8
#log:


import commands
import re
import pdb
import os

#********************-----------------********************#

#********************-----------------********************#
class crfppTest(object):
    '''
        use use crf++ algorithm tool to optimize the mmseg result, this class is for using model to test data
        tool get:https://drive.google.com/folderview?id=0B4y35FiV1wh7fngteFhHQUN2Y1B5eUJBNHZUemJYQV9VWlBUb3JlX0xBdWVZTWtSbVBneU0&usp=drive_web#list
    '''
    def __init__(self):
        pass


    #-----------------********************-----------------#
    def FormateTestData(self, testSourceDataPath, testFormDataPath):
        '''
            description: manage the test source data into the CRF++ need form
            input:
                testSourceDataPath
                testFormDataPath
            output:
                none
        '''

        testSourceDataFile = open(testSourceDataPath,'r')
        testFormDataFile = open(testFormDataPath,'w')

        rePattern = re.compile('''(?:[0-\x79]+|[\x80-\xff]{3}?)''')
        #onelineSource = testSourceDataFile.readline()
        #while(onelineSource):
        for onelineSource in testSourceDataFile.readlines():
            SourceList = rePattern.findall(onelineSource)
            for item in SourceList:
                testFormDataFile.write(item+"\n")
            testFormDataFile.write("\n") #空行分割每一行
            #onelineSource = testSourceDataFile.readline()

        testSourceDataFile.close()
        testFormDataFile.close()


    #-----------------********************-----------------#
    def manageTestData(self, testFormDataPath, CRFTagDataPath, modelName="crf_model"):
        '''
            description: run the crf test action and save the middle result
            input:
                testFormDataPath
                CRFTagDataPath
            output:
                none
        '''

        #testFormDataFile = open(testFormDataPath,'r')
        #CRFResultDataFile = open(CRFResultDataPath,'w')
        resultStatue = ""
        resultOutput = ""
        command = "crf_test -m " + modelName + " " + testFormDataPath +" > "+ CRFTagDataPath
        resultStatue,resultOutput = commands.getstatusoutput(command)
        print resultOutput




    #-----------------********************-----------------#
    def FormateTagData(self, CRFTagDataPath, CRFResultDataPath):
        '''
            description: formate tag data into participle data
            input:
                CRFTagDataPath
                CRFResultDataPath
            output:
                none
        '''

        CRFTagDataFile = open(CRFTagDataPath,'r')
        CRFResultDataFile = open(CRFResultDataPath, 'w')
        rePattern = re.compile('''\s+''')
        tempWords = ""
        TagList = []
        #formTagSwitch = {
        #    "S": CRFResultDataFile.write(TagList[0]+"  "),
        #    "B": tempWords = TagList[0],
        #    "M": tempWords += TagList[0],
        #    "E": CRFResultDataFile.write(tempWords+TagList[0]+"  ")
        #}
        #print "#####################################################"
        #pdb.set_trace()
        #onelineCRFTagData = CRFTagDataFile.readline()
        #print "online"+onelineCRFTagData
        #onelineCRFTagData = CRFTagDataFile.readline()
        #print "online"+onelineCRFTagData
        #while(onelineCRFTagData):
        for onelineCRFTagData in CRFTagDataFile.readlines():
            if(onelineCRFTagData == "\n"):
                CRFResultDataFile.write("\n")
                #print "hello!!"
            else:
                #print "world!!"
                TagList = rePattern.split(onelineCRFTagData)
                #print TagList
                if(len(TagList) > 1):
                    if(TagList[1] == "S"):
                        #print TagList[0]
                        CRFResultDataFile.write(TagList[0]+"  ")
                    elif(TagList[1] == "B"):
                        tempWords = ""
                        tempWords = TagList[0]
                    elif(TagList[1] == "M"):
                        tempWords += TagList[0]
                    elif(TagList[1] == "E"):
                        tempWords += TagList[0]
                        CRFResultDataFile.write(tempWords+"  ")

            #onelineCRFTagData = CRFTagDataFile.readline()
        CRFTagDataFile.close()
        CRFResultDataFile.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        testsourcePath = sys.argv[1]
        os.mkdir("tmp")
        testformPath = os.getcwd()+"/tmp/crfform.utf8"
        crftagPath = os.getcwd()+"/tmp/crftag.utf8"
        testResultPath = sys.argv[2]

        #testsourcePath = "/home/warrior/gitDir/PythonCode/MyParticiple/dataSource/testing/pku_test.utf8"
        #testformPath = "/home/warrior/gitDir/PythonCode/MyParticiple/crfMidFiles/crfform.utf8"
        #crftagPath = "/home/warrior/gitDir/PythonCode/MyParticiple/crfMidFiles/crftag.utf8"
        #testResultPath = "/home/warrior/gitDir/PythonCode/MyParticiple/resultFiles/crf_result.utf8"
        crfpp = crfppTest()
        print "start test!!"
        crfpp.FormateTestData(testsourcePath,testformPath)
        crfpp.manageTestData(testformPath, crftagPath)
        crfpp.FormateTagData(crftagPath,testResultPath)
        print "test complete!!"
    elif (len(sys.argv)>0) & (sys.argv[1] == "help"):
        print "crf test command help:"
        print "1.the test data source is in utf8 form"
        print "2.command example:python crfppTest.py  test_source_data_path result_path"
    else:
        print "arguments error!!"
        print "command example:python crfppTest.py  test_source_data_path result_path"
