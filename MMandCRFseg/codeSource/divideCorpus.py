#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: divideCorpus.py
#description: divide corpus into 5 part
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-4-8
#log:

import os
import sys
import commands


if __name__ == "__main__":
    if len(sys.argv)==3:
        fd = open(sys.argv[1],'r')
        file_cont = fd.readlines()
        fd.close()
        all_line_num = len(file_cont)
        part_line_num = int(all_line_num/5)

        for i in range(0,5):
            fd = open(sys.argv[2]+"_part%d.utf8"%i, 'w')
            for one_line in file_cont[i*part_line_num:(i+1)*part_line_num]:
                fd.write(one_line)
            fd.close
        print part_line_num
