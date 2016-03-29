#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: testExample.py
#description: test example for this project
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-3-9
#log:

from codeSource.MMSEG import *
from codeSource.crfppTrain import *
from codeSource.crfppTest import *
from codeSource.mmsegAndCRF import *
import os
import sys

'''
    测试脚本针对本分词模型，CRF训练已经完成，因此可以直接使用CRF——MODEL测试数据，MMSEG也可直接使用，最后综合两种算法结果的特点，得到最终结果。
'''
if __name__ == "__main__":
    if len(sys.argv)==2:
        crf_train_flag = False
        currentDIR = os.getcwd()
        outputStatue = ""
        if crf_train_flag :
            #CRF 训练
            sourcePath = currentDIR+"/dataSource/training/pku_training.utf8"
            resultpath = currentDIR+"/crfMidFiles/train_form_result.utf8"
            templatePath = currentDIR+"/codeSource/template"
            crf_model_name = "crf_model"
            crftrain = crfppTrain()
            crftrain.getTrainData(sourcePath,resultpath)
            print "get traing data complete!!"
            print "start training!!"
            crftrain.excuteCRFTrain(templatePath, resultpath, crf_model_name)
            print "training complete!!"
        else:
            testsourcePath = sys.argv[1]
            print "   start"
            print "    ||"
            print "   _||_"
            print "   \  /"
            print "    \/"
            #第一步，通过MMSEG实现基于词典和词频信息等的分词
            outputStatue = ""
            lineCounter = 0
            wordfilepath = currentDIR+"/dataSource/gold/pku_training_words.utf8"
            storageResultpath = currentDIR+"/tmp/mmseg_result.utf8"

            unvisualCharPattern = re.compile('''\s+''')
            getDataFile = open(testsourcePath, 'r')
            getDataFileCopy = open(testsourcePath+".copy",'w')
            for onelineSource in getDataFile.readlines():
                listCopy = unvisualCharPattern.findall(onelineSource)
                if len(listCopy[0]) == len(onelineSource):
                    pass
                else:
                    getDataFileCopy.write(onelineSource)
            getDataFile.close()
            getDataFileCopy.close()
            getDataFile = open(testsourcePath+".copy",'r')
            storDataFile = open(storageResultpath, 'w')
            mmseg = MMSEG()
            mmseg.getwordsDict(wordfilepath)
            wordelem2 = getDataFile.readline()
            mmseg.MMSEGStep1MaxThreeLength(wordelem2, mmseg.wordList)
            while(wordelem2):
                for i in mmseg.sentencePartWordList:
                    storDataFile.write(i+"  ")
                storDataFile.write("\n")
                wordelem2 = getDataFile.readline()
                mmseg.MMSEGStep1MaxThreeLength(wordelem2, mmseg.wordList)
                lineCounter+=1
                print "mmseg manage %d lines\r" % lineCounter ,
            print "mmseg  manage  complete\r"
            print "    ||"
            print "   _||_"
            print "   \  /"
            print "    \/"
            storDataFile.close()
            getDataFile.close()


            #第二步， 通过crf_model实现基于统计信息的分词
            testformPath = currentDIR+"/crfMidFiles/crfform.utf8"
            crftagPath = currentDIR+"/crfMidFiles/crftag.utf8"
            testResultPath = currentDIR+"/tmp/crf_result.utf8"
            crfpp = crfppTest()
            crfpp.FormateTestData(testsourcePath,testformPath)
            crfpp.manageTestData(testformPath, crftagPath)
            crfpp.FormateTagData(crftagPath,testResultPath)
            print "CRF manage complete!!"
            print "    ||"
            print "   _||_"
            print "   \  /"
            print "    \/"


            #第三步，综合考虑两种分词结果的特点，最优化分词结果
            optmize = mmsegAndCRF()
            MMSEGResultPath = currentDIR+"/tmp//mmseg_result.utf8"
            CRFResultPath = currentDIR+"/tmp/crf_result.utf8"
            optResultPath = currentDIR+"/tmp/optimize_result.utf8"
            optmize.optimizeCRFAndMMSEG(MMSEGResultPath, CRFResultPath, optResultPath)
            print "    ||"
            print "   _||_"
            print "   \  /"
            print "    \/"
            print "   end"
    else:
        print "argv error!!"
        print "please input test_source_data_path"
        print "forexample: python testExample.py /home/../MyParticiple/dataSource/testing/pku_test.utf8"
