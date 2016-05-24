#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: test.py
#description: test code for tianchi data mining
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-5-16
#log:

import pandas as pd

data = pd.read_csv('/home/warrior/Desktop/tianchiData/mars_tianchi_songs.csv')
print data.head(8)
print '\n Data Types:'
print data.dtypes