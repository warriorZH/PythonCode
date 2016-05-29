#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: test.py
#description: test code for tianchi data mining
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-5-16
#log:

# import pandas as pd
#
# data = pd.read_csv('/home/warrior/Desktop/tianchiData/mars_tianchi_songs.csv')
# print data.head(8)
# print '\n Data Types:'
# print data.dtypes

#
# aa = range(0,21,4)
# print aa[3:]


# output = "aa"
# output = "%s%s%s" % (output, str(13), ",")
# print output

#
# date_list = []
# for iter in range(20150901, 20150931):
#     date_list.append(iter)
# for iter in range(20151001, 20151031):
#     date_list.append(iter)
#
# print date_list


# aa = '6bb4c3bbdb6f5a96d643320c6b6005f5\r\n'
# bb = aa[:-2]#.split('\r\n')[0]
# print bb

aa = [1,2,3]
bb = [4,5,6]
cc = [7,8,9]
for a,b,c in zip(aa,bb,cc):
    print a,b,c