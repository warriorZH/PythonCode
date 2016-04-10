#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: MMSEG.py
#description: use mmseg algorithm for paticiple in chinese language
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-3-5
#log:

import re
import numpy
import pdb
import sys

#********************-----------------********************#

#********************-----------------********************#
class MMSEG(object):
    '''
        realize mmseg algorithm in this class
        U can access mmseg algorithm in:
        english mode: http://technology.chtsai.org/mmseg/
        chinese mode: http://www.52nlp.cn/%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D%E5%85%A5%E9%97%A8%E4%B9%8B%E6%9C%80%E5%A4%A7%E5%8C%B9%E9%85%8D%E6%B3%95%E6%89%A9%E5%B1%951
    '''
    def __init__(self):
        #used in word list
        self.wordList = [] #storage word dictionary
        self.wordListLength = 0 #length of wordList
        self.wordElemIndex = 0
        #step1
        self.maxWordLength = 10
        self.participleList = [""]
        self.cacheParticipleList = [""]
        self.sentencePartWordList = [""]
        self.maxLengthRecordList = []
        self.cacheParticipleSamples = [[] for i in range(0,50)] #设置了一个较大buffer，待优化
        self.cacheParticipleSamplesCounter = 0
        #step 2
        self.maxAverageLengthRecordList = []
        #step3
        self.minVarianceValueRecordList = []
        #step4
        self.wordCountRecordList = []
        self.allWordCountDict = {}
        self.bestWordIndex = 0



    #-----------------********************-----------------#
    def getWordCountDict(self, fileDir):
        '''
            description: get the word count dictionary from fileDir
            input:
                fileDir: the path of file storage the word count dictionary
            output:
                none
        '''
        wordCountFile = open(fileDir,'r')
        oneLine = wordCountFile.readline()
        while(oneLine):
            rPattern = re.compile('''[ ]{5}''')
            oneLineList = rPattern.split(oneLine)
            self.allWordCountDict[oneLineList[0]] = int(oneLineList[1])
            oneLine = wordCountFile.readline()
        wordCountFile.close()


    #-----------------********************-----------------#
    def getwordsDict(self, fileDir):
        '''
            description: get the word dictionary : pku_training_words.utf8,
                        and construct a sorted dictionary
            input:
                fileDir :  the path of word dict file
            output:
                none
        '''
        wordfile = open(fileDir, 'r')
        try:
            all_word_lines = wordfile.read()
        except:
            print "open file error!!"
        finally:
            wordfile.close()

        self.wordList = all_word_lines.split('\n')
        self.wordList = sorted(self.wordList)
        self.wordListLength = len(self.wordList)


    #-----------------********************-----------------#
    def findElemInWordDict(self, wordElem, preElemindex = None):
        '''
            description: find wordElem in wordList use binary search,
                        and if "PreElemindex" is not None,
                        will search element behind "PreElemindex"
            input:
                wordElem: the word to be find
                preElemindex: the index of  previously find elememt
            output:
                True: find the wordElem
                False: not find the wordElem
        '''
        inpreElemindex = preElemindex
        wordListLeft = 0
        wordListRight = self.wordListLength-1
        wordListMid = int((wordListLeft+wordListRight)/2)
        if preElemindex == None:#
            while(wordListLeft<=wordListRight):#the binary search
                if (self.wordList[wordListMid] in wordElem) & (wordElem in self.wordList[wordListMid]):
                    self.wordElemIndex =  wordListMid
                    #print self.wordElemIndex
                    return True
                elif self.wordList[wordListMid]>wordElem:
                    wordListRight = wordListMid-1
                    wordListMid = int((wordListLeft+wordListRight)/2)
                else:
                    wordListLeft = wordListMid+1
                    wordListMid = int((wordListLeft+wordListRight)/2)
            #print "First NONE"
            return False
        else:
            self.wordElemIndex = preElemindex #search element behind "PreElemindex"
            while(self.wordElemIndex<=self.wordListLength):
                if self.wordList[preElemindex] in self.wordList[self.wordElemIndex]:
                    if (wordElem in self.wordList[self.wordElemIndex]) & (self.wordList[self.wordElemIndex] in wordElem):
                        #print self.wordElemIndex
                        return True
                    else:
                        self.wordElemIndex +=1
                else:
                    #print "Second NONE"
                    return False




    #-----------------********************-----------------#
    def MMSEGStep1MaxThreeLength(self, sentence, wordsTable):
        '''
            description: base on three continuous words ,
                        and select the max length of the sum of three words
            input:
                sentence: the sentence to be participle
                wordsTable: the reference word dictionary
            output:
                True : select the best participle
                False : not select the best participle ,need the next step
        '''
        #divide the sentence into single character
        rePattern = re.compile('''(?:[0-\x79]+|[\x80-\xff]{3}?)''')
        sentenceSingleWordList = rePattern.findall(sentence)
        word1Left = 0
        word1RightTemp = 0
        word1Right = word1Left
        word2Left = 0
        word2RightTemp = 0
        word2Right = word2Left
        word3Left = 0
        word3Right = word3Left
        word1Elem = ""
        word2Elem = ""
        word3Elem = ""
        cacheWord1Elem = ""
        cacheWord2Elem = ""
        cacheWord3Elem = ""
        FirstUnSpreadableFlag = True
        SecondUnSpreadableFlag = True
        self.cacheParticipleSamples = [[] for i in range(0,50)] #设置了一个较大buffer，待优化
        self.cacheParticipleSamplesCounter = 0
        self.participleList = []
        self.cacheParticipleList = []
        self.sentencePartWordList = []
        while(word1Right<len(sentenceSingleWordList)-1):
            #
            self.cacheParticipleSamples = [[] for i in range(0,50)]
            self.cacheParticipleSamplesCounter = 0
            #pdb.set_trace()
            if(self.findThreeElements(word1Left, word1Right, 0, sentenceSingleWordList)):
                word1Elem, word2Elem, word3Elem, word1Right, word2Right= self.findThreeElements(word1Left, word1Right, 0, sentenceSingleWordList)
            else:
                #print "input index error!"
                return None
            #print "start: "+word1Elem, word2Elem, word3Elem
            self.cacheParticipleSamples[self.cacheParticipleSamplesCounter].append(word1Elem)
            self.cacheParticipleSamples[self.cacheParticipleSamplesCounter].append(word2Elem)
            self.cacheParticipleSamples[self.cacheParticipleSamplesCounter].append(word3Elem)
            self.cacheParticipleSamplesCounter+=1
            word1Right = word1Right+1
            #pdb.set_trace()
            while((word2Right<=len(sentenceSingleWordList)-1)|(word2Right<=len(sentenceSingleWordList)-1)):
                #扩展第一个词
                if(self.findThreeElements(word1Left, word1Right, 1, sentenceSingleWordList)):
                    cacheWord1Elem, cacheWord2Elem, cacheWord3Elem, word1Right, word2RightTemp= self.findThreeElements(word1Left, word1Right, 1, sentenceSingleWordList)
                    if cacheWord1Elem == word1Elem:#扩展失败，跳出     #这里返回的word1Right是正确的word1Elem右边界，但是word2RightTemp有待确认的价值，
                        word2Right = word2Right #word1Elem扩展失败，word2Elem的右边界不更新                       #也就是word1Elem确实扩展了这个就用来更新word2Elem的右边界，
                        word2Left = word1Right+1                                                              #若word1Elem没有扩展，这个值就没有参考价值
                        FirstUnSpreadableFlag = True
                    else:#继续扩展
                        FirstUnSpreadableFlag = False
                        word2Right = word2RightTemp #word1Elem扩展成功，word2Elem的右边界更新
                        word2Left = word1Right+1
                        word1Elem = cacheWord1Elem
                        word2Elem = cacheWord2Elem
                        word3Elem = cacheWord3Elem
                        word1Left = word1Left
                        word1Right = word1Right+1
                    #print "first: "+word1Elem, word2Elem, word3Elem
                    if FirstUnSpreadableFlag == False:
                        self.cacheParticipleSamples[self.cacheParticipleSamplesCounter].append(word1Elem)
                        self.cacheParticipleSamples[self.cacheParticipleSamplesCounter].append(word2Elem)
                        self.cacheParticipleSamples[self.cacheParticipleSamplesCounter].append(word3Elem)
                        self.cacheParticipleSamplesCounter+=1
                #扩展第二个词
                word2Right = word2Right+1
                if(word2Right<len(sentenceSingleWordList)-1):
                    if(self.findThreeElements(word2Left, word2Right, 2, sentenceSingleWordList)):
                        cacheWord1Elem, cacheWord2Elem, cacheWord3Elem, word1RightTemp, word2Right= self.findThreeElements(word2Left, word2Right, 2, sentenceSingleWordList)
                        if cacheWord2Elem == word2Elem:                                 #这里返回的word2Right是正确的word2Elem右边界，但是word1RightTemp没有可参考性
                            SecondUnSpreadableFlag = True
                        else:
                            SecondUnSpreadableFlag = False
                            word2Elem = cacheWord2Elem
                            word3Elem = cacheWord3Elem
                        #print "second: "+word1Elem, cacheWord2Elem, word3Elem
                        if SecondUnSpreadableFlag == False:
                            self.cacheParticipleSamples[self.cacheParticipleSamplesCounter].append(word1Elem)
                            self.cacheParticipleSamples[self.cacheParticipleSamplesCounter].append(word2Elem)
                            self.cacheParticipleSamples[self.cacheParticipleSamplesCounter].append(word3Elem)
                            self.cacheParticipleSamplesCounter+=1
                if ((FirstUnSpreadableFlag & SecondUnSpreadableFlag) | (self.cacheParticipleSamplesCounter>48)):
                    break
            #get the most optimization wordElem
            self.getMaxLengthLists()
            if (len(self.maxLengthRecordList)>1):
                #print "the total length not only one!!#########################"
                self.MMSEGStep2MaxAverageLength()
                if(len(self.maxAverageLengthRecordList)>1):
                    #print "the average length not only one!!@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                    self.MMSEGStep3MinVariance()
                    if(len(self.minVarianceValueRecordList)>1):
                        #print "the variance length not only one!!$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                        self.MMSEGStep4MaxWordCount()
                        #if(len(self.wordCountRecordList)>0):
                        word1Elem = self.cacheParticipleSamples[self.bestWordIndex][0]
                        word2Elem = self.cacheParticipleSamples[self.bestWordIndex][1]
                        word3Elem = self.cacheParticipleSamples[self.bestWordIndex][2]
                        #else:
                        #    word1Elem = self.cacheParticipleSamples[self.minVarianceValueRecordList[0]][0]
                        #    word2Elem = self.cacheParticipleSamples[self.minVarianceValueRecordList[0]][1]
                        #    word3Elem = self.cacheParticipleSamples[self.minVarianceValueRecordList[0]][2]
                    else:
                        word1Elem = self.cacheParticipleSamples[self.minVarianceValueRecordList[0]][0]
                        word2Elem = self.cacheParticipleSamples[self.minVarianceValueRecordList[0]][1]
                        word3Elem = self.cacheParticipleSamples[self.minVarianceValueRecordList[0]][2]
                else:
                    word1Elem = self.cacheParticipleSamples[self.maxAverageLengthRecordList[0]][0]
                    word2Elem = self.cacheParticipleSamples[self.maxAverageLengthRecordList[0]][1]
                    word3Elem = self.cacheParticipleSamples[self.maxAverageLengthRecordList[0]][2]
            else:
                word1Elem = self.cacheParticipleSamples[self.maxLengthRecordList[0]][0]
                word2Elem = self.cacheParticipleSamples[self.maxLengthRecordList[0]][1]
                word3Elem = self.cacheParticipleSamples[self.maxLengthRecordList[0]][2]
            self.sentencePartWordList.append(word1Elem)
            #print "end: "+word1Elem, word2Elem, word3Elem
            #updata the word1Left index
            word1ElemSingleWordList = rePattern.findall(word1Elem)
            word1Left = word1Left+len(word1ElemSingleWordList)
            word1Right = word1Left
        self.sentencePartWordList.append(word2Elem)
        self.sentencePartWordList.append(word3Elem)


    #-----------------********************-----------------#
    def findThreeElements(self ,startLeft, startRight, spreadFlag,sentenceSingleWordList):
        '''
            description: get three word terms base "startLeft"/"startRight"/"spreadFlag" from sentenceSingleWordList
            input:
                startLeft: left side of search start
                startRight:right side of search start
                spreadFlag:
                    0:the first time to search
                    1:to spread the word1Elem
                    2:to spread the word2Elem
                sentenceSingleWordList: signal word list of the sentence to be participle
            output:
                word1Elem, word2Elem, word3Elem, word1Right, word2Right
                None: input index error
        '''
        word1Elem = ""
        word2Elem = ""
        word3Elem = ""
        tempElem = ""
        word1Left = 0
        word1Right = word1Left
        word2Left = 0
        word2Right = word2Left
        word3Left = 0
        word3Right = word3Left
        sentenceSingleWordList = sentenceSingleWordList
        #
        if spreadFlag == 0:
            #search the first element use Minimum Matching
            word1Left = startLeft
            word1Right = startRight
            cacheRightIndex = word1Right
            if((word1Left>=len(sentenceSingleWordList))|(word1Left>word1Right)):
                return None
            for i in range(word1Left, word1Right+1):  #get the left element
                word1Elem = word1Elem + sentenceSingleWordList[i]
            tempElem = word1Elem
            while(self.findElemInWordDict(tempElem) == False):
                if((word1Right-word1Left+1 < self.maxWordLength) & (word1Right < len(sentenceSingleWordList)-1)):
                    word1Right = word1Right+1
                    tempElem = tempElem + sentenceSingleWordList[word1Right]
                else:
                    word1Right = cacheRightIndex
                    tempElem = word1Elem #如果找不到和这个字相关的词，就默认为单字词
                    break
            word1Elem = tempElem
            if word1Right >= len(sentenceSingleWordList)-1:
                word2Elem = ""
                word3Elem = ""
                #updata the word2Left
                word2Left = word1Right+1
                word2Right = word2Left
                #print word1Elem, word2Elem, word3Elem
                return word1Elem, word2Elem, word3Elem, word1Right, word2Right

            #search the Second element use Minimum Matching
            word2Left = word1Right+1
            word2Right = word2Left
            cacheRightIndex = word2Right
            for i in range(word2Left, word2Right+1):  #get the left element
                word2Elem = word2Elem + sentenceSingleWordList[i]
            tempElem = word2Elem
            while(self.findElemInWordDict(tempElem) == False):
                if((word2Right-word2Left+1 < self.maxWordLength) & (word2Right < len(sentenceSingleWordList)-1)):
                    word2Right = word2Right+1
                    tempElem = tempElem + sentenceSingleWordList[word2Right]
                else:
                    word2Right = cacheRightIndex
                    tempElem = word2Elem #如果找不到和这个字相关的词，就默认为单字词
                    break
            word2Elem = tempElem
            if word2Right >= len(sentenceSingleWordList)-1:
                word3Elem = ""
                #print word1Elem, word2Elem, word3Elem
                return word1Elem, word2Elem, word3Elem, word1Right, word2Right
        elif spreadFlag == 1:
            #spread the first element use Minimum Matching
            word1Left = startLeft
            word1Right = startRight
            cacheRightIndex = word1Right
            if((word1Left>=len(sentenceSingleWordList))|(word1Left>=word1Right)):
                return None
            for i in range(word1Left, word1Right):  #get the left element
                word1Elem = word1Elem + sentenceSingleWordList[i]
            if word1Right>=len(sentenceSingleWordList):#访问溢出
                return None
            tempElem = word1Elem+sentenceSingleWordList[word1Right]
            while(self.findElemInWordDict(tempElem) == False):
                if((word1Right-word1Left+1 < self.maxWordLength) & (word1Right < len(sentenceSingleWordList)-1)):
                    word1Right = word1Right+1
                    tempElem = tempElem + sentenceSingleWordList[word1Right]
                else:
                    word1Right = cacheRightIndex-1
                    tempElem = word1Elem #如果找不到和这个字相关的词，就默认为单字词
                    break
            #if(self.findElemInWordDict(tempElem) == True):
            #    print tempElem
            word1Elem = tempElem
            if word1Right >= len(sentenceSingleWordList)-1:
                word2Elem = ""
                word3Elem = ""
                #updata the word2Left for extern second
                word2Left = word1Right+1
                word2Right = word2Left
                #print word1Elem, word2Elem, word3Elem
                return word1Elem, word2Elem, word3Elem, word1Right, word2Right
            if(cacheRightIndex<=word1Right): #如果第一个词扩展成功，就需要对第二个词作更新，仍是最小匹配原则，否则第二个词不改动
                #search the Second element use Minimum Matching
                word2Left = word1Right+1
                word2Right = word2Left
                for i in range(word2Left, word2Right+1):  #get the left element
                    word2Elem = word2Elem + sentenceSingleWordList[i]
                tempElem = word2Elem
                while(self.findElemInWordDict(tempElem) == False):
                    if((word2Right-word2Left+1 < self.maxWordLength) & (word2Right < len(sentenceSingleWordList)-1)):
                        word2Right = word2Right+1
                        tempElem = tempElem + sentenceSingleWordList[word2Right]
                    else:
                        word2Right = word2Left
                        tempElem = word2Elem #如果找不到和这个字相关的词，就默认为单字词
                        break
                word2Elem = tempElem
                if word2Right >= len(sentenceSingleWordList)-1:
                    word3Elem = ""
                    #print word1Elem, word2Elem, word3Elem
                    return word1Elem, word2Elem, word3Elem, word1Right, word2Right
        elif spreadFlag == 2:
            #spread the Second element use Minimum Matching

            word2Left = startLeft
            word2Right = startRight
            cacheRightIndex = word2Right
            if((word2Left>=len(sentenceSingleWordList))|(word2Left>=word2Right)):#输入参数错误
                return None
            for i in range(word2Left, word2Right):
                word2Elem = word2Elem + sentenceSingleWordList[i]
            if word2Right>=len(sentenceSingleWordList):#访问溢出
                return None
            tempElem = word2Elem + sentenceSingleWordList[word2Right]
            while(self.findElemInWordDict(tempElem) == False):
                if((word2Right-word2Left+1 < self.maxWordLength) & (word2Right < len(sentenceSingleWordList)-1)):
                    word2Right = word2Right+1
                    tempElem = tempElem + sentenceSingleWordList[word2Right]
                else:
                    word2Right = cacheRightIndex-1
                    tempElem = word2Elem #如果找不到和这个字相关的词，就默认为单字词
                    break
            word2Elem = tempElem
            if word2Right >= len(sentenceSingleWordList)-1:
                word3Elem = ""
                #print word1Elem, word2Elem, word3Elem
                return word1Elem, word2Elem, word3Elem, word1Right, word2Right
        #search the third elememt use Maximum Matching
        word3Left = word2Right+1
        word3Right = word3Left
        if(len(sentenceSingleWordList)-word3Left > self.maxWordLength):
            word3Elem=sentenceSingleWordList[word3Left]
            tempElem = ""
            for i in range(word3Left,word3Left+self.maxWordLength):
                tempElem = tempElem + sentenceSingleWordList[i]
                if self.findElemInWordDict(tempElem):
                    word3Elem = tempElem
        else:
            word3Elem=sentenceSingleWordList[word3Left]
            tempElem = ""
            for i in range(word3Left,len(sentenceSingleWordList)):
                tempElem = tempElem + sentenceSingleWordList[i]
                if self.findElemInWordDict(tempElem):
                    word3Elem = tempElem


        ##while(!self.findElemInWordDict(word3Elem)):
        ##    if(word3Right - word3Left + 1 < self.maxWordLength)
        ##        word3Right = word3Right+1
        ##        word3Elem = word3Elem + sentenceSingleWordList[word3Right]
        ##    else:
        ##        word3Right = word3Left
        ##        word3Elem = sentenceSingleWordList[word3Left]
        ##        break
        #print word1Elem, word2Elem, word3Elem
        return word1Elem, word2Elem, word3Elem, word1Right, word2Right

    #-----------------********************-----------------#
    def getMaxLengthLists(self):
        '''
            description:get the lists of the max length of three words
            input:
                cacheParticipleSamples:record of the all three words Samples
            output:
                None
        '''
        i=0
        j=0
        lengthTemp = 0
        listTemp = []
        self.maxLengthRecordList = []
        lengthRecord={}
        i=0
        while(self.cacheParticipleSamples[i]):
        #for i in range(0,len(self.cacheParticipleSamples)):
            lengthTemp = len(self.cacheParticipleSamples[i][0]) + \
                        len(self.cacheParticipleSamples[i][1]) + \
                        len(self.cacheParticipleSamples[i][2])
            #print self.cacheParticipleSamples[i]
            lengthRecord[i] = lengthTemp
            i+=1
            if i>48:
                break
        listTemp = sorted(lengthRecord.items(), key=lambda d: d[1], reverse=True)
        for j in range(0,i):
            if listTemp[0][1] == listTemp[j][1]:
                self.maxLengthRecordList.append(listTemp[j][0])
            else:
                break



    #-----------------********************-----------------#
    def MMSEGStep2MaxAverageLength(self):
        '''
            description: select the max average length of the max length elements in cacheParticipleSamples
            input:
                None
            output:
                None
        '''
        i=0
        j=0
        m=0
        lengthTemp = 0
        averageLength = 0
        elementNumber = 0
        averageRecordDict = {}
        listTemp = [] #用来存储排序过后的以(index, averageLength)为单位的序列
        self.maxAverageLengthRecordList = []
        if(len(self.maxLengthRecordList)>1):
            for i in range(0,len(self.maxLengthRecordList)):
                elementNumber = 0
                lengthTemp = 0
                for m in range(0,3):
                    if(len(self.cacheParticipleSamples[i][m])>0):
                        lengthTemp += len(self.cacheParticipleSamples[i][m])
                        elementNumber += 1
                #print self.cacheParticipleSamples[i]
                averageLength = int(100*lengthTemp/elementNumber)
                averageRecordDict[self.maxLengthRecordList[i]] = averageLength
                #print "总长：", lengthTemp , " 个数：", elementNumber, " 平均长：", averageLength
                                        #所在 cacheParticipleSamples位置  #所在位置的平均词长
            listTemp = sorted(averageRecordDict.items(), key=lambda d: d[1], reverse=True)
            #print listTemp
            for j in range(0, len(self.maxLengthRecordList)):
                if listTemp[0][1] == listTemp[j][1]: #判断平均词长是否相等
                    self.maxAverageLengthRecordList.append(listTemp[j][0]) #若相等，把所在 cacheParticipleSamples位置加入到list中
                else:
                    break

    #-----------------********************-----------------#
    def MMSEGStep3MinVariance(self):
        '''
            description: select the min variance of the max average length elements in cacheParticipleSamples
            input:
                none
            output:
                none
        '''
        i=0
        j=0
        m=0
        varianceRecord = 0
        lengthListTemp = []
        varianceRecordDict = {}
        wordCountTemp = 0
        wordCountRecordDict = {}
        wordCountDivisevarianceDict = {}
        wordCountDivisevarianceList = []
        self.minVarianceValueRecordList = []
        self.bestWordIndex = 0
        if(len(self.maxAverageLengthRecordList)>1):
            for i in range(0,len(self.maxAverageLengthRecordList)):
                elementNumber = 0
                lengthListTemp = []
                for m in range(0,3):
                    if(len(self.cacheParticipleSamples[i][m])>0):
                        lengthListTemp.append(len(self.cacheParticipleSamples[i][m]))
                        elementNumber += 1

                varianceRecord = numpy.var(lengthListTemp)
                varianceRecordDict[self.maxAverageLengthRecordList[i]] = varianceRecord
                #print " 个数：", elementNumber, " 均方：", varianceRecord
            listTemp = sorted(varianceRecordDict.items(), key=lambda d: d[1])

            #for j in range(0, len(self.maxAverageLengthRecordList)):
            #    wordCountDivisevarianceDict[listTemp[j][0]] = wordCountRecordDict[listTemp[j][0]]/listTemp[j][1]
            #    print "均方："  + str(listTemp[j][1]) + "  词频：" + str(wordCountRecordDict[listTemp[j][0]]) + " 参数值:" + str(wordCountDivisevarianceDict[listTemp[j][0]]) + "\n"
            #wordCountDivisevarianceList = sorted(wordCountDivisevarianceDict.items(), key=lambda d:d[1], reverse=True)
            #self.bestWordIndex = wordCountDivisevarianceList[0][0]
            for j in range(0, len(self.maxAverageLengthRecordList)):
                if listTemp[0][1] == listTemp[j][1]: #判断均方差是否相等
                    self.minVarianceValueRecordList.append(listTemp[j][0]) #若相等，把所在 cacheParticipleSamples位置加入到list中
                else:
                    break

    #-----------------********************-----------------#
    def MMSEGStep4MaxWordCount(self):
        '''
            description: get the top sum of word count in the max average length items
            input:
                None
            output:
                None
        '''
        wordCountTemp=0
        wordCountRecordDict={}
        wordCountRecordList=[]
        self.wordCountRecordList = []
        if(len(self.minVarianceValueRecordList)>1):
            for i in range(0,len(self.minVarianceValueRecordList)):
                wordCountTemp=0
                for m in range(0,3):
                    if(self.allWordCountDict.has_key(self.cacheParticipleSamples[i][m])):
                        if(len(self.cacheParticipleSamples[i][m])>3):
                            wordCountTemp += self.allWordCountDict[self.cacheParticipleSamples[i][m]]
                wordCountRecordDict[self.minVarianceValueRecordList[i]] = wordCountTemp
            self.wordCountRecordList = sorted(wordCountRecordDict.items(), key=lambda d:d[1], reverse=True)
            self.bestWordIndex = self.wordCountRecordList[0][0]
            #print self.bestWordIndex



if __name__ == "__main__":
    if len(sys.argv) == 4:
        wordfilepath = sys.argv[1]
        storageResultpath = sys.argv[2]
        getPartDatapath = sys.argv[3]
        lineCounter = 0
        unvisualCharPattern = re.compile('''( +|\s+)''')
        getDataFile = open(getPartDatapath, 'r')
        getDataFileCopy = open(getPartDatapath+".copy",'w')
        for onelineSource in getDataFile.readlines():
            listCopy = unvisualCharPattern.findall(onelineSource)
            if len(listCopy[0]) == len(onelineSource):
                pass
            else:
                getDataFileCopy.write(onelineSource)
        getDataFile.close()
        getDataFileCopy.close()
        getDataFile = open(getPartDatapath+".copy",'r')
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
            print "mmseg manage %d lines" % lineCounter
        storDataFile.close()
        getDataFile.close()
    elif  (len(sys.argv)>0) & (sys.argv[1] == "help"):
        print "mmseg test command help:"
        print "1.the test data source is in utf8 form"
        print "2.command example:python MMSEG.py  test_word_path test_source_data_path result_path"
    else:
        print "arguments error!!"
        print "2.command example:python MMSEG.py  test_word_path test_source_data_path result_path"

#wordfilepath = "/home/warrior/gitDir/PythonCode/MyParticiple/dataSource/gold/pku_training_words.utf8"
#storageResultpath = "/home/warrior/gitDir/PythonCode/MyParticiple/mmseg_result.utf8"
#getPartDatapath = "/home/warrior/gitDir/PythonCode/MyParticiple/dataSource/testing/pku_test.utf8"

#测试findElemInWordDict功能
#wordfilepath = "/home/warrior/gitDir/PythonCode/MyParticiple/dataSource/gold/pku_training_words.utf8"
#mmseg = MMSEG()
#mmseg.getwordsDict(wordfilepath)
#wordelem1 = "执"
#mmseg.findElemInWordDict(wordelem1)
#print mmseg.wordElemIndex
#for i in range(mmseg.wordElemIndex,mmseg.wordElemIndex+40):
#    print("%d: %s\n" % (i, mmseg.wordList[i]))
