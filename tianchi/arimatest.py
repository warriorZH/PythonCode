#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: arimatest.py
#description: test data in arima
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-5-17
#log:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima_model import *


s_dta=[216,211,213,187,208,231,239,291,173,253,317,235,196,271,221,252,181,222,218,247,272,233,215,264,205,282,213,271,258,228,222,256,361,282,253,300,239,261,281,257,286,276,387,281,300,323,332,343,315,318,263,329,291,352,335,357,390,328,246,232,281,354,353,332,300,282,222,350,252,316,303,234,264,377,307,412,336,368,353,407,407,350,419,480,378,427,410,339,295,312,338,415,323,285,320,373,358,328,441,441,359,306,338,312,353,312,319,353,396,341,359,427,389,522,372,467,407,511,514,427,385,498,527,495,418,392,537,465,422,422,439,503,363,352,469,411,422,487,389,299,360,503,439,490,315,487,603,606,366,556,463,405,408,429,358,477,418,370,334,376,317,304,348,326,305,353,425,355,372,374,351,356,359,301,276,321,407,379,406,439,411,417,319]

print len(s_dta)
dta = pd.Series(s_dta[:123])
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001','2123'))
# plt.plot(dta)
# plt.show()

# fig = plt.figure()
# ax1= fig.add_subplot(311)
# diff1 = dta.diff(1)
# diff1.plot(ax=ax1)
# fig.show()

dta= dta.diff(1)#我们已经知道要使用一阶差分的时间序列，之前判断差分的程序可以注释掉
fig = plt.figure()
ax1=fig.add_subplot(221)
fig = sm.graphics.tsa.plot_acf(dta, lags=40, ax=ax1)
ax2 = fig.add_subplot(222)
fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)
# fig.show()


model = ARIMA(dta, order=(2,1,2))
result_AR = model.fit()
pre_data = result_AR.predict('2074','2183',dynamic=False)
print pre_data.values

# fig.show()

ax3 = fig.add_subplot(223)
dta.plot(ax=ax3)
result_AR.fittedvalues.plot(ax=ax3,color='red')

# # fig.show()
# ax4 = fig.add_subplot(224)
# temp = pd.Series(s_dta[73:])
# temp.index = pd.Index(sm.tsa.datetools.dates_from_range('2074','2183'))
# temp.plot(ax=ax4)
# pre_result = pd.Series(pre_data.values)
# pre_result.index = pd.Index(sm.tsa.datetools.dates_from_range('2074','2183'))
# pre_result.plot(ax=ax4,color='red')
# fig.show()

