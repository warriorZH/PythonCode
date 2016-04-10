#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: createTrainCorpus.py
#description: create train corpus by segment result / dictionary / last corpus
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-4-9
#log:


import sys
import commands
import re


if __name__ == "__main__":
    if len(sys.argv) == 5:
        fd_last_corpus = open(sys.argv[1], 'w')
        fd_result = open(sys.argv[2], 'r')
        fd_dictionary = open(sys.argv[3], 'r')
        fd_cur_corpus = open(sys.argv[4],'r')

        last_corpus = fd_cur_corpus.readlines()
        result = fd_result.readlines()
        dictionary = fd_dictionary.readlines()

        #close
        fd_result.close()
        fd_dictionary.close()
        fd_cur_corpus.close()
        #set pattern
        pattern = re.compile('\s+')

        last_corpus_list = []
        result_list = []
        dictionary_list = []
        cur_corpus_list = []
        for oneline in last_corpus:
            for one_word in pattern.split(oneline):
                last_corpus_list.append(one_word)
        for oneline in dictionary:
            for one_word in pattern.split(oneline):
                dictionary_list.append(one_word)

        fd_cur_corpus = open(sys.argv[4],'w')
        for oneline in last_corpus:
            fd_cur_corpus.write(oneline)
        for oneline in result:
            oneline_add = ""
            for one_word in pattern.split(oneline):
                if one_word in dictionary_list:
                    if one_word not in last_corpus_list:
                        oneline_add = oneline_add+"  "+one_word
            if len(oneline_add)>0:
                fd_cur_corpus.write(oneline_add+"\n")
                print oneline_add+"\n"
        fd_cur_corpus.close()

        fd_cur_corpus = open(sys.argv[4],'r')
        cur_corpus = fd_cur_corpus.readlines()
        for oneline in cur_corpus:
            for one_word in pattern.split(oneline):
                cur_corpus_list.append(one_word)
        print len(cur_corpus_list)
        print len(last_corpus_list)
        #更新上次训练语料
        for oneline in last_corpus:
            fd_last_corpus.write(oneline)
        fd_last_corpus.close()
