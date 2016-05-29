#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: score.py
#description: calculate score of predict data
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-5-29
#log:

import math

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
            sum_val += math.pow((S - T)/T, 2)
        ceta = math.sqrt(sum_val/len(real_list))
        fai = math.sqrt(sum(real_list))
        one_score = (1 - ceta)*fai
        return one_score
    else:
        print "input data error"
        return False

