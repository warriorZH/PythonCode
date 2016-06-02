#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: using_pq_pre.py
#description: use the already known p/q value to predict
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-5-31
#log:
import os
import re
import sys
import math
import statsmodels.api as sm
from statsmodels.tsa.arima_model import _arma_predict_out_of_sample
import pandas as pd


def predict(pq_file, train_file):
    if os.path.isfile(pq_file):
        pq_fd = open(pq_file, 'r')
    else:
        print "pq_file error"
    if os.path.isfile(train_file):
        train_fd = open(train_file, 'r')
    else:
        print "train_file error"
    pq_cont = pq_fd.readlines()
    train_cont = train_fd.readlines()
    pq_fd.close()
    train_fd.close()
    play_data = []
    artist_id = []
    score = []
    for index in range(1, len(train_cont), 4):
        play_data.append(train_cont[index])
        # print train_cont[index]
        artist_id.append(train_cont[index - 1][:-2])
    print len(play_data)
    oneline_list = []
    artist_pq = {}
    for item in pq_cont:
        oneline_list = item.split(',')
        print oneline_list
        artist_pq[oneline_list[0]] = [int(oneline_list[1]), int(oneline_list[2][:-1])]
    arma_model = []
    pre_data = []
    for one_id, one_train_data in zip(artist_id, play_data):
        p = artist_pq[one_id][0]
        q = artist_pq[one_id][1]
        list_data = one_train_data.split(',')
        for i in range(0, len(list_data), 1):
            list_data[i] = int(list_data[i])
        dta = pd.Series(list_data[105:183])
        dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2046', '2123'))
        try:
            one_model = sm.tsa.ARMA(dta, (p, q)).fit(disp=-1, trend="c", solver='powell', method="css")
            arma_model.append(one_model)
            # get what you need for predicting one-step ahead
            params = one_model.params
            residuals = one_model.resid
            p = one_model.k_ar
            q = one_model.k_ma
            k_exog = one_model.k_exog
            k_trend = one_model.k_trend
            steps = 60

            pre_result = _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=dta,
                                                     exog=None, method='ols', start=len(dta))
            pre_data.append(pre_result)
            one_score = Calculate_score(list_data[123:123 + steps], pre_result)
            # print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:%d" % one_score
            if one_score < -100:
                one_score = 0
            score.append(one_score)
        except:
            q = q - p
            try:
                one_model = sm.tsa.ARMA(dta, (p, q)).fit(disp=-1, trend="c", solver='powell', method="css")
                arma_model.append(one_model)
                # get what you need for predicting one-step ahead
                params = one_model.params
                residuals = one_model.resid
                p = one_model.k_ar
                q = one_model.k_ma
                k_exog = one_model.k_exog
                k_trend = one_model.k_trend
                steps = 60

                pre_result = _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=dta,
                                                         exog=None, method='ols', start=len(dta))
                pre_data.append(pre_result)
                one_score = Calculate_score(list_data[123:123 + steps], pre_result)
                # if one_score < 0:
                #     one_score = -1
                # print "###########################:%d" % one_score
                score.append(one_score)
            except:
                q = q + p
                p = 0
                try:
                    one_model = sm.tsa.ARMA(dta, (p, q)).fit(disp=-1, trend="c", solver='powell', method="css")
                    arma_model.append(one_model)
                    # get what you need for predicting one-step ahead
                    params = one_model.params
                    residuals = one_model.resid
                    p = one_model.k_ar
                    q = one_model.k_ma
                    k_exog = one_model.k_exog
                    k_trend = one_model.k_trend
                    steps = 60

                    pre_result = _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog,
                                                             endog=dta,
                                                             exog=None, method='ols', start=len(dta))
                    pre_data.append(pre_result)
                    one_score = Calculate_score(list_data[123:123 + steps], pre_result)
                    # if one_score < 0:
                    #     one_score = -1
                    # print "#################################################################################:%d" % one_score
                    score.append(one_score)
                except:
                    pre_result = list_data[123:123 + steps]
                    p = 0
                    q = 0
                    pre_data.append(pre_result)
                    one_score = Calculate_score(list_data[123:123 + steps], pre_result)
                    # if one_score < 0:
                    #     one_score = -1
                    # print "#################################################################################:%d" % one_score
                    score.append(one_score)
                    arma_model.append([])
                    pre_data.append([])
                    score.append(0)
                    print list_data
                    print one_id

    result_data_fd = open("./new_mars_tianchi_artist_plays_predict.csv", 'w')

    date_list = []
    for iter in range(20150901, 20150931):
        date_list.append(iter)
    for iter in range(20151001, 20151031):
        date_list.append(iter)

    for item, art_id in zip(pre_data, artist_id):
        output = ""
        for iter, one_date in zip(item, date_list):
            output = "%s,%s,%s\n" % (art_id, str(int(iter)), one_date)
            result_data_fd.write(output)
    result_data_fd.close()
    print sum(score)


def Calculate_score(real_list, pre_list):
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
        return one_score
    else:
        print "input data error"
        return False


if __name__ == "__main__":
    if len(sys.argv) == 3:
        predict(sys.argv[1], sys.argv[2])
    else:
        print "input form: 'python using_pq_pre.py pq_file train_file'"