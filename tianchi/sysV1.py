#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: sysV1.py
#description: pre-system version-1 using arma model
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-5-29
#log:

import os
import sys
import math
import statsmodels.api as sm
from statsmodels.tsa.arima_model import _arma_predict_out_of_sample
import pandas as pd
# from tianchi import score

class sysV1(object):
    """
    :description pre-system version-1 using arma model
    """
    def __init__(self):
        self.play_data = []
        self.artist_id = []
        self.train_data = []
        self.test_data = []
        self.arma_model = []
        self.ar_p_value = []
        self.ma_q_value = []
        self.pre_data = []
        self.score = []

    def getData(self, inputPath):
        """
        :description get artist play data
        :param inputPath: artist play data file path
        :return:
        False: get data fail
        True: get data success
        """
        if os.path.isfile(inputPath):
            input_fd = open(inputPath, 'r')
            input_cont = input_fd.readlines()
            print len(input_cont)
            for index in range(1, len(input_cont), 4):
                self.play_data.append(input_cont[index])
                self.artist_id.append(input_cont[index-1][:-2])
            print len(self.play_data)
        else:
            print "input path error!!"
    def get_cut_off_value(self, p_q_list):
        """
        :description get p/q cut off value base on p/q list
        :param p_q_list: p/q list
        :return:
        value: the cut off value
        """
        index_count = 0
        for item in p_q_list:
            if item > 0.2:
                index_count += 1
            else:
                return index_count
        return 1





    def model_fit_pred(self, num):
        """
        :description fit model and predict num days data
        :return:
        False: predict fail
        True: predict success
        """
        # divide train data and test data
        artist_pq_value_fd = open('./artist_pq_value.txt', 'w')
        for item, artist_id in zip(self.play_data, self.artist_id):
            list_data = item.split(',')
            for i in range(0, len(list_data), 1):
                list_data[i] = int(list_data[i])

            self.train_data.append(list_data[45:123])
            self.test_data.append(list_data[123:])
            dta = pd.Series(list_data[105:183])
            dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2046', '2123'))
            p = self.get_cut_off_value(sm.tsa.acf(dta, nlags=10))
            q = self.get_cut_off_value(sm.tsa.pacf(dta, nlags=10))
            try:
                one_model = sm.tsa.ARMA(dta, (p, q)).fit(disp=-1, trend="c", solver='powell', method="css")
                self.arma_model.append(one_model)
                self.ar_p_value.append(p)
                self.ma_q_value.append(q)
                # get what you need for predicting one-step ahead
                params = one_model.params
                residuals = one_model.resid
                p = one_model.k_ar
                q = one_model.k_ma
                k_exog = one_model.k_exog
                k_trend = one_model.k_trend
                steps = int(num)

                pre_result = _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=dta, exog=None, method='ols', start=len(dta))
                self.pre_data.append(pre_result)
                one_score = self.Calculate_score(list_data[123:123+steps], pre_result)
                # print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:%d" % one_score
                if one_score < -100:
                    one_score = 0
                self.score.append(one_score)
            except:
                q = q - p
                try:
                    one_model = sm.tsa.ARMA(dta, (p, q)).fit(disp=-1, trend="c", solver='powell', method="css")
                    self.arma_model.append(one_model)
                    self.ar_p_value.append(p)
                    self.ma_q_value.append(q)
                    # get what you need for predicting one-step ahead
                    params = one_model.params
                    residuals = one_model.resid
                    p = one_model.k_ar
                    q = one_model.k_ma
                    k_exog = one_model.k_exog
                    k_trend = one_model.k_trend
                    steps = int(num)

                    pre_result = _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=dta,
                                                             exog=None, method='ols', start=len(dta))
                    self.pre_data.append(pre_result)
                    one_score = self.Calculate_score(list_data[123:123 + steps], pre_result)
                    # if one_score < 0:
                    #     one_score = -1
                    # print "###########################:%d" % one_score
                    self.score.append(one_score)
                except:
                    q = q + p
                    p = 0
                    try:
                        one_model = sm.tsa.ARMA(dta, (p, q)).fit(disp=-1, trend="c", solver='powell', method="css")
                        self.arma_model.append(one_model)
                        self.ar_p_value.append(p)
                        self.ma_q_value.append(q)
                        # get what you need for predicting one-step ahead
                        params = one_model.params
                        residuals = one_model.resid
                        p = one_model.k_ar
                        q = one_model.k_ma
                        k_exog = one_model.k_exog
                        k_trend = one_model.k_trend
                        steps = int(num)

                        pre_result = _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog,
                                                                 endog=dta,
                                                                 exog=None, method='ols', start=len(dta))
                        self.pre_data.append(pre_result)
                        one_score = self.Calculate_score(list_data[123:123 + steps], pre_result)
                        # if one_score < 0:
                        #     one_score = -1
                        # print "#################################################################################:%d" % one_score
                        self.score.append(one_score)
                    except:
                        pre_result = list_data[123:123 + steps]
                        p = 0
                        q = 0
                        self.ar_p_value.append(p)
                        self.ma_q_value.append(q)
                        self.pre_data.append(pre_result)
                        one_score = self.Calculate_score(list_data[123:123 + steps], pre_result)
                        # if one_score < 0:
                        #     one_score = -1
                        # print "#################################################################################:%d" % one_score
                        self.score.append(one_score)
                        self.arma_model.append([])
                        self.pre_data.append([])
                        self.score.append(0)
                        print list_data
                        print artist_id
            output = "%s,%d,%d\n" % (artist_id, p, q)
            artist_pq_value_fd.write(output)
        artist_pq_value_fd.close()


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
                # S = abs(S)
                # T = abs(T)
                sum_val += math.pow((S - T-1) / (1+T), 2)
            ceta = math.sqrt(sum_val / len(real_list))
            fai = math.sqrt(sum(real_list))
            one_score = (1 - ceta) * fai

            if one_score < -100:
                print real_list
                print pre_list
                print "#####################################################################################################"
                print ceta
                print fai
            return one_score
        else:
            print "input data error"
            return False

if __name__ == "__main__":
    if len(sys.argv) == 3:
        process = sysV1()
        process.getData(sys.argv[1])
        process.model_fit_pred(sys.argv[2])
        print process.score
        # for iter in range(len(process.score)):
        #     print "%d   %f" % (iter+1, process.score[iter])
        # print process.ar_p_value[6]
        # print process.ma_q_value[6]
        # process.score[6] = 0
        # print sum(process.score)
        result_data_fd = open("./mars_tianchi_artist_plays_predict.csv", 'w')


        date_list = []
        for iter in range(20150901, 20150931):
            date_list.append(iter)
        for iter in range(20151001, 20151031):
            date_list.append(iter)

        for item, art_id in zip(process.pre_data, process.artist_id):
            output = ""
            for iter, one_date in zip(item, date_list):
                output = "%s,%s,%s\n" % (art_id, str(int(iter)), one_date)
                result_data_fd.write(output)
        result_data_fd.close()
        # print process.artist_id
    else:
        print "input form 'python sysV1.py path_aritst_play predict_number'"