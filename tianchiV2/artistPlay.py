#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: artistPlay.py
#description: fit the artist play data use LST algorithm
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-5-25
#log:


import numpy as np  #惯例
import scipy as sp  #惯例
#这里就是我们要使用的最小二乘的函数
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

m = 7  #多项式的次数

realdata = [141,152,178,161,135,159,137,132,117,141,124,169,196,131,125,153,149,170,135,163,119,155,133,116,121,162,139,146,112,112,138,149,135,164,168,129,168,207,230,163,171,160,152,161,163,180,176,160,199,121,151,156,208,205,214,183,189,177,200,143,139,146,140,169,194,145,159,145,171,195,165,129,157,161,133,173,166,142,140,117,136,136,138,117,134,125,173,160,138,139,128,114,126,137,154,152,154,146,136,121,148,178,142,177,184,121,210,193,267,161,152,146,121,134,193,146,132,167,119,124,150,142,163,156,198,130,112,145,138,138,173,196,161,145,145,155,141,162,147,115,106,166,119,142,157,128,142,118,146,143,126,159,125,104,85,146,133,139,122,118,111,97,127,148,158,170,115,120,105,122,176,127,127,132,171,136,136,95,102,121,126,131,183]
y = realdata[:123]
x = range(1, 124, 1)

def fake_func(p, x):
    f = np.poly1d(p) #多项式分布的函数
    return f(x)


# #残差函数
# def residuals(p, y, x):
#     return y - fake_func(p, x)

def residuals(p, y, x):
    ret = y - fake_func(p, x)
    ret = np.append(ret, np.sqrt(0.0001)*np.dot(p,p)) #将lambda^(1/2)p加在了返回的array的后面
    return ret

#先随机产生一组多项式分布的参数
p0 = np.random.randn(m)

#fitting
plsq = leastsq(residuals, p0, args=(y, x))

index_x = 21
print(plsq[0])

plt.plot(range(1, index_x, 1), realdata[113:133], label='real_value')
plt.plot(range(1, index_x, 1), fake_func(plsq[0], range(1, 134, 1))[113:133], label='fit_value')
plt.show()