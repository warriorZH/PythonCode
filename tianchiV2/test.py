#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: test.py
#description: test code for project
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-5-25
#log:


import numpy as np  #惯例
import scipy as sp  #惯例
from scipy.optimize import leastsq #这里就是我们要使用的最小二乘的函数
import matplotlib.pyplot as plt

# aa = range(1,124,1)
# print(aa)

aa = [1,2,3]
bb = [1,2,3]
cc = []
cc = np.dot(aa, bb)
print (cc)