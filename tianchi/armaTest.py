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
s_dta = [304,275,291,3993,5769,2740,1676,1448,1563,1578,3111,3232,2063,1436,1370,1515,1595,2808,2507,2400,2144,2136,2305,1724,3464,5462,4223,2895,3124,3408,3302,2234,1949,2239,2490,2221,2105,1970,2463,1937,1831,1370,1618,1546,1441,1544,1309,1233,1182,1412,1069,874,848,950,740,936,861,1038,1027,845,976,1112,1155,831,1053,828,869,976,882,964,1013,604,810,702,792,692,812,867,799,866,717,851,789,727,893,1127,847,787,799,802,717,868,1068,950,702,792,787,672,685,697,838,634,829,778,743,728,755,1305,936,800,937,735,590,816,828,652,631,710,689,649,836,747,568,551,772,688,758,607,749,837,669,654,784,728,600,753,786,708,570,616,742,717,844,633,511,395,744,458,436,656,787,572,500,632,724,702,641,607,641,531,503,566,868,710,725,908,852,732,618,1169,887,700,502,798,455,634,459,510,588,607,484,423,386]
dta = pd.Series(s_dta[60:123])
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2061', '2123'))
# dta = dta.diff(1)
plt.plot(dta.index,dta.values)
plt.show()
# #
# fig = plt.figure(figsize=(12,8))
# ax1 = fig.add_subplot(211)
# fig = sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=40, ax=ax1)
# ax2 = fig.add_subplot(212)
# fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)
# fig.show()x, unbiased=False, nlags=40, qstat=False, fft=False, alpha=None

p = sm.tsa.acf(dta, nlags=20)
print(p)
p = sm.tsa.pacf(dta, nlags=20)
print(p)


# arma_mod20 = sm.tsa.ARMA(dta, (2,2)).fit()
# # print(arma_mod20.params)

arma_mod30 = sm.tsa.ARMA(dta, (0, 1)).fit(disp=-1, trend="c", solver='powell', method="css")
print(arma_mod30.summary())
# # print(arma_mod30.params)
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
# # print(stats.normaltest(resid-1))
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
steps = 20

pre_result = _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=dta, exog=None, method='ols', start=len(dta))
# print "#################################"
print(pre_result)
plt.plot(s_dta[123:143])
plt.plot(pre_result,'red')
plt.show()