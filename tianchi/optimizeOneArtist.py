#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: optimizeOne.py
#description: optimize one specified artist pre-score
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-5-31
#log:

import os
import sys
import math
import statsmodels.api as sm
from statsmodels.tsa.arima_model import _arma_predict_out_of_sample
import pandas as pd
import matplotlib.pyplot as plt

class optimizeOne(object):
    """
    :description optimize one specified artist pre-score
    """
    def __init__(self):
        self.pre_result = []
        self.test_data = []

    def optPredictedValue(self, train_data):
        """
        :description calculate a optimized predicted value
        :param train_data: model train data
        :return:
        """
        self.test_data = train_data[123:183]
        dta = pd.Series(train_data[:123])
        dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001', '2123'))
        # dta = dta.diff(1)
        # plt.plot(dta.index, dta.values)
        # plt.show()

        p = sm.tsa.acf(dta, nlags=20)
        print(p)
        p = sm.tsa.pacf(dta, nlags=20)
        print(p)

        arma_mod = sm.tsa.ARMA(dta, (15, 5)).fit(disp=-1, trend="c", solver='powell', method="css")
        # print(arma_mod.summary())

        # get what you need for predicting one-step ahead
        params = arma_mod.params
        residuals = arma_mod.resid
        p = arma_mod.k_ar
        q = arma_mod.k_ma
        k_exog = arma_mod.k_exog
        k_trend = arma_mod.k_trend
        steps = 60

        self.pre_result = _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=dta, exog=None,
                                                 method='ols', start=len(dta))
        # print "#################################"
        print(self.pre_result)

        # result_data_fd = open("./oprResult.txt", 'w+')
        # date_list = []
        # for iter in range(20150901, 20150931):
        #     date_list.append(iter)
        # for iter in range(20151001, 20151031):
        #     date_list.append(iter)
        #
        # item = self.pre_result
        # art_id = ""
        # output = ""
        # for iter, one_date in zip(item, date_list):
        #     output = "%s,%s,%s\n" % (art_id, str(int(iter)), one_date)
        #     result_data_fd.write(output)
        # result_data_fd.close()

        plt.plot(range(183), train_data)
        plt.plot(range(123,183), self.pre_result, 'red')
        plt.show()

    def Calculate_score(self, real_list, pre_list):
        """
        :description calculate score of predict data base on the rule on
                https://tianchi.shuju.aliyun.com/competition/information.htm?spm=0.0.0.0.nEciiw&raceId=231531&_lang=zh_CN
        :param real_list: test collection data
        :param pre_list: prediction data
        :return:
            one_score: score of one artist
            False: get score error
        """
        if len(real_list) == len(pre_list):
            sum_val = 0.0
            for S, T in zip(pre_list, real_list):
                sum_val += math.pow((S - T - 1) / (1 + T), 2)
            ceta = math.sqrt(sum_val / len(real_list))
            fai = math.sqrt(sum(real_list))
            one_score = (1 - ceta) * fai

            if one_score < -100:
                print real_list
                print pre_list
                print "#####################################################################################################"
                print ceta
                print fai
            print one_score
        else:
            print "input data error"
            return False

if __name__ == "__main__":
    optOne = optimizeOne()
    train_data = [216,211,213,187,208,231,239,291,173,253,317,235,196,271,221,252,181,222,218,247,272,233,215,264,205,282,213,271,258,228,222,256,361,282,253,300,239,261,281,257,286,276,387,281,300,323,332,343,315,318,263,329,291,352,335,357,390,328,246,232,281,354,353,332,300,282,222,350,252,316,303,234,264,377,307,412,336,368,353,407,407,350,419,480,378,427,410,339,295,312,338,415,323,285,320,373,358,328,441,441,359,306,338,312,353,312,319,353,396,341,359,427,389,522,372,467,407,511,514,427,385,498,527,495,418,392,537,465,422,422,439,503,363,352,469,411,422,487,389,299,360,503,439,490,315,487,603,606,366,556,463,405,408,429,358,477,418,370,334,376,317,304,348,326,305,353,425,355,372,374,351,356,359,301,276,321,407,379,406,439,411,417,319]
    optOne.optPredictedValue(train_data)
    optOne.Calculate_score(optOne.test_data, optOne.pre_result)
