#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: datashow.py
#description: show data in figure
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-5-17
#log:

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5, 0.1)
y = np.sin(x)
plt.plot(x, y)
plt.show()