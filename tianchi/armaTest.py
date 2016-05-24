#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: arimatest.py
#description: test code for arma model
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-5-21
#log:

from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.tsa.arima_model import _arma_predict_out_of_sample

from statsmodels.graphics.api import qqplot




# print(sm.datasets.sunspots.NOTE)
s_dta = [216,211,213,187,208,231,239,291,173,253,317,235,196,271,221,252,181,222,218,247,272,233,215,264,205,282,213,271,258,228,222,256,361,282,253,300,239,261,281,257,286,276,387,281,300,323,332,343,315,318,263,329,291,352,335,357,390,328,246,232,281,354,353,332,300,282,222,350,252,316,303,234,264,377,307,412,336,368,353,407,407,350,419,480,378,427,410,339,295,312,338,415,323,285,320,373,358,328,441,441,359,306,338,312,353,312,319,353,396,341,359,427,389,522,372,467,407,511,514,427,385,498,527,495,418,392,537,465,422,422,439,503,363,352,469,411,422,487,389,299,360,503,439,490,315,487,603,606,366,556,463,405,408,429,358,477,418,370,334,376,317,304,348,326,305,353,425,355,372,374,351,356,359,301,276,321,407,379,406,439,411,417,319]
dta = pd.Series(s_dta[:153])
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001', '2153'))
dta = dta.diff(1)
# # del dta["YEAR"]
plt.plot(dta.index,dta.values)
# print(dta.values)
plt.show()
#
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)
fig.show()

# arma_mod20 = sm.tsa.ARMA(dta, (2,2)).fit()
# # print(arma_mod20.params)

arma_mod30 = sm.tsa.ARMA(dta, (3, 3)).fit(trend="c", method="css-mle")
# print(arma_mod30.params)



#
# # print(arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic)
# # print(arma_mod30.aic, arma_mod30.bic, arma_mod30.hqic)
# #
# # print(sm.stats.durbin_watson(arma_mod30.resid.values))
# # print(sm.stats.durbin_watson(arma_mod20.resid.values))
#
# fig = plt.figure(figsize=(12,8))
# ax = fig.add_subplot(111)
# ax = arma_mod30.resid.plot(ax=ax);
# # fig.show()
#
# resid = arma_mod30.resid
# # print(stats.normaltest(resid))
# fig = plt.figure(figsize=(12,8))
# ax = fig.add_subplot(111)
# fig = qqplot(resid, line='q', ax=ax, fit=True)
# # fig.show()
#
# fig = plt.figure(figsize=(12,8))
# ax1 = fig.add_subplot(211)
# fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
# ax2 = fig.add_subplot(212)
# fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)
#
#
#
# r,q,p = sm.tsa.acf(resid.values.squeeze(), qstat=True)
# data = np.c_[range(1,41), r[1:], q, p]
# table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
# # print(table.set_index('lag'))
#
# predict_sunspots = arma_mod20.forecast(30, alpha=.1)
# # print(predict_sunspots)
#
# # fig, ax = plt.subplots(figsize=(12, 8))
# # ax = dta.ix['2001':].plot(ax=ax)
# # fig = arma_mod30.plot_predict(83, 203, alpha=.1, exog=s_dta[80:183], dynamic=False, ax=ax, plot_insample=True)
# # fig.show()

# get what you need for predicting one-step ahead
params = arma_mod30.params
residuals = arma_mod30.resid
p = arma_mod30.k_ar
q = arma_mod30.k_ma
k_exog = arma_mod30.k_exog
k_trend = arma_mod30.k_trend
steps = 30

pre_result = _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=dta, exog=None, start=len(dta))
# print "#################################"
print(pre_result)
plt.plot(s_dta[153:183])
plt.plot(pre_result)
plt.show()