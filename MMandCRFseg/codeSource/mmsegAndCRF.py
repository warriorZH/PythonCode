#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: mmsegAndCRF.py
#description: considerinng both MMSEG and CRF to reach the optimization
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-3-9
#log:


import re

class mmsegAndCRF(object):
    '''
        比较了，MMSEG CRF各自的特点，取出两种结果中相同的作为最终结果，不相同的分词结果，就选择不同词片段中平均词长比较长的作为结果
    '''
    def __init__(self):
        pass

    def optimizeCRFAndMMSEG(self, MMSEGResultPath, CRFResultPath, optResultPath):
        '''
            description: considering both MMSEG and CRF, view their result alone can know that the longest word is reasonable at most situation
            input:
                MMSEGResultPath
                CRFResultPath
            output:
                none
        '''
        onelineMMSEG = ""
        oneLineCRF = ""
        listMMSEG = []
        listCRF = []
        midListMMSEG = []
        midListCRF = []
        midFlag = False
        optmizeList = []
        indexMMSEG = 0
        indexCRF = 0
        wordCountMMSEG = 0
        wordCountCRF = 0
        lineCount = 0

        MMSEGResultFile = open(MMSEGResultPath,'r')
        CRFResultFile = open(CRFResultPath,'r')
        optResultFile = open(optResultPath,'w')

        rePattern = re.compile('''[ ]+''')
        onelineMMSEG = MMSEGResultFile.readline()
        oneLineCRF = CRFResultFile.readline()
        #print len(oneLineCRF)
        #print len(onelineMMSEG)
        while((len(onelineMMSEG)>0) & (len(oneLineCRF)>0)):
            lineCount+=1
            listMMSEG = rePattern.split(onelineMMSEG)
            listCRF = rePattern.split(oneLineCRF)
            midListMMSEG = []
            midListCRF = []
            midFlag = False
            optmizeList = []
            indexMMSEG = 0
            indexCRF = 0
            wordCountMMSEG = 0
            wordCountCRF = 0
            if(len(listCRF)>len(listMMSEG)):
                maxLength = len(listCRF)
            else:
                maxLength = len(listMMSEG)
            while((indexCRF<len(listCRF)) & (indexMMSEG<len(listMMSEG))):
                if(listMMSEG[indexMMSEG]==listCRF[indexCRF]):
                    if(midFlag == True):
                        if(len(midListCRF)<=len(midListMMSEG)):
                            optmizeList = optmizeList+midListCRF
                            midListCRF = [] #reset
                            midListMMSEG = []
                            wordCountCRF = 0
                            wordCountMMSEG = 0
                        else:
                            optmizeList = optmizeList+midListMMSEG
                            midListMMSEG = [] #reset
                            midListCRF = []
                            wordCountCRF = 0
                            wordCountMMSEG = 0
                    optmizeList.append(listCRF[indexCRF])
                    wordCountCRF += len(listCRF[indexCRF])
                    indexCRF += 1
                    wordCountMMSEG += len(listMMSEG[indexMMSEG])
                    indexMMSEG += 1
                    midFlag = False #消除误差
                else:
                    if(midFlag == True): #非第一次产生误差
                        if(wordCountMMSEG > wordCountCRF):
                            wordCountCRF += len(listCRF[indexCRF])
                            midListCRF.append(listCRF[indexCRF])
                            indexCRF += 1
                        elif(wordCountMMSEG < wordCountCRF):
                            wordCountMMSEG += len(listMMSEG[indexMMSEG])
                            midListMMSEG.append(listMMSEG[indexMMSEG])
                            indexMMSEG += 1
                        else:
                            wordCountCRF += len(listCRF[indexCRF])
                            midListCRF.append(listCRF[indexCRF])
                            indexCRF += 1
                            wordCountMMSEG += len(listMMSEG[indexMMSEG])
                            midListMMSEG.append(listMMSEG[indexMMSEG])
                            indexMMSEG += 1
                    else:
                        midFlag = True #第一次产生误差
                        wordCountCRF += len(listCRF[indexCRF])
                        midListCRF.append(listCRF[indexCRF])
                        indexCRF += 1
                        wordCountMMSEG += len(listMMSEG[indexMMSEG])
                        midListMMSEG.append(listMMSEG[indexMMSEG])
                        indexMMSEG += 1
            if(indexCRF<indexMMSEG):
                for i in range(indexCRF,len(listCRF)):
                    optmizeList.append(listCRF[i])
            else:
                for i in range(indexMMSEG,len(listMMSEG)):
                    optmizeList.append(listMMSEG[i])
            print "optimize manage %d lines\r" % lineCount,
            #print optmizeList
            for i in range(0,len(optmizeList)-1):
                optResultFile.write(optmizeList[i]+"  ")
            optResultFile.write(optmizeList[i+1])
            onelineMMSEG = MMSEGResultFile.readline()
            oneLineCRF = CRFResultFile.readline()
        while(len(onelineMMSEG)>0):
            optResultFile.write(onelineMMSEG)
            onelineMMSEG = MMSEGResultFile.readline()
        while(len(oneLineCRF)>0):
            optResultFile.write(oneLineCRF)
            oneLineCRF = CRFResultFile.readline()
        print "optimize  manage  complete\r"
        optResultFile.close()
        MMSEGResultFile.close()
        CRFResultFile.close()




if __name__ == "__main__":
    if len(sys.argv) == 4:
        MMSEGResultPath = sys.argv[1]
        CRFResultPath = sys.argv[2]
        optResultPath = sys.argv[3]
        optimizeCRFAndMMSEG(MMSEGResultPath, CRFResultPath, optResultPath)
    elif  (len(sys.argv)>0) & (sys.argv[1] == "help"):
        print "mmsegAndCRF test command help:"
        print "1.the data source is in utf8 form"
        print "2.command example:python mmsegAndCRF.py  mmseg_result_path crf_result_path optimize_result_path"
    else:
        print "arguments error!!"
        print "2.command example:python mmsegAndCRF.py  mmseg_result_path crf_result_path optimize_result_path"



#MMSEGResultPath = "/home/warrior/gitDir/PythonCode/MyParticiple/resultFiles/mmseg_result.utf8"
#CRFResultPath = "/home/warrior/gitDir/PythonCode/MyParticiple/resultFiles/crf_result.utf8"
#optResultPath = "/home/warrior/gitDir/PythonCode/MyParticiple/resultFiles/optimize_result.utf8"
#optimizeCRFAndMMSEG(MMSEGResultPath, CRFResultPath, optResultPath)
