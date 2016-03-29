#! /usr/bin/env python
# -*- coding: utf-8 -*-

#filename: weibocookie.py
#description:
#   login in to the sina weibo use cookie
#writer: warrior mail:15933533880@163.com

#import package
import sys
import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib
import rsa
import binascii







class weibocookie:
   # def __init__(self,url,headers):
   #     self.url = url
   #     self.headers = headers

    def getpagecont(self, filename):
        headers = {'cookie':'U_TRS1=00000040.62b56e48.55e1a8a9.c3c1aa76; UOR=www.baidu.com,blog.sina.com.cn,; vjuids=7c934d7b1.14f797ad747.0.43cb4b38; SINAGLOBAL=202.206.212.64_1440852137.604519; SGUID=1440852138460_11190771; sso_info=v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLKNo4yxjKOAuI2DjLeJp5WpmYO0so2jjLGMo4C4jYOMtw==; ULV=1448863118114:7:6:2:221.192.236.70_1448851618.109722:1448805644093; vjlast=1448847683.1448863119.10; lxlrtst=1448859205_o; lxlrttp=1448859205; tgc=TGT-MjYzMTIwODQzNw==-1449060828-xd-6E425903BE824BBE988E3A56D4320D00; SUS=SID-2631208437-1449060828-XD-xknum-11ff7d432ba6d220ec3ebfe063302e60; SUE=es%3D5d012fccd6281c2823079679f81a9c75%26ev%3Dv1%26es2%3D47698a496fc53f6b4b8da4d63790040c%26rs0%3DxU3UgeaRI%252Bb5xj7BfwVGufspoMgK%252FGxUm0ti2Ahx766DzMmVCHRcGxIFNTfaR2d06fQcawRRboS1%252BXA%252F9hwaTDsR6I78attAfzsJ3WcYYyPSgwlFx4UpXhoKo13YuRSFVt9OC3isXOHN3AH%252F7ZATLJuNhrl57%252B7Ck9neyiTgvc4%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1449060828%26et%3D1449147228%26d%3D40c3%26i%3D2e60%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D25%26st%3D0%26lt%3D7%26uid%3D2631208437%26user%3D0owarrioro0.%252A%252A%26ag%3D9%26name%3D0owarrioro0%2540sina.com%26nick%3D%25E7%2594%25A8%25E6%2588%25B72631208437%26sex%3D%26ps%3D0%26email%3D0owarrioro0%2540sina.com%26dob%3D%26ln%3D%26os%3D%26fmp%3D%26lcp%3D; SUB=_2A257WpmMDeRxGeRI6FMT8CbIyDuIHXVYEYxErDV_PUNbvtAPLVGlkW8XJ2RRKO_CdUdK6KO9QDIpiX8wUA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFW0sbnBz3W8AYO-kcqOSK9; ALC=ac%3D25%26bt%3D1449060828%26cv%3D5.0%26et%3D1480596828%26uid%3D2631208437%26vf%3D0%26vs%3D0%26vt%3D0%26es%3Dde66246f44162634dc2b5ee98285083e; ALF=1480596828; LT=1449060828; U_TRS2=00000040.71b61984.565eea2c.4a6181bd'}
        url = 'http://login.sina.com.cn/member/app.php?entry=sso&act=my'
        req = urllib2.Request(url, headers = headers)
        try:
            r = urllib2.urlopen(req)
            text = r.read()
            f = open(filename, 'w')
            f.write(text)
            f.close()
            print "get page success!"
            return 1
        except:
            print "get page error!"
            return -1


    def gethomepagecont(self, filename):
        headers = {'cookie':'SINAGLOBAL=9786038745660.334.1440906972437; wvr=6; un=0owarrioro0@sina.com; SUS=SID-2631208437-1449062859-GZ-jnzwc-c18a732a632a36b52a950445d06f2e60; SUE=es%3D0991b4394620c9ee87d60c475ff933c4%26ev%3Dv1%26es2%3D40862a498c7824c3f1a6e053d204d553%26rs0%3DBiOj0IQIAURtZe7xRKKSgJ3tQ6Qg3nH9If7oimP2l3xTQ94xKPhNFJcPgHXvYPpwL7hnIAn7%252BPopEqQw3qxY3rTqMt%252BDOl3FTWGLhwv4iiQ7w%252BGlnzZa018fwELo8e0IC6GD2h2e9IPamDlBkyb%252B9KiRFqnFahI41KEaC1yZSzI%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1449062859%26et%3D1449149259%26d%3Dc909%26i%3D2e60%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D25%26st%3D0%26uid%3D2631208437%26name%3D0owarrioro0%2540sina.com%26nick%3D%25E7%2594%25A8%25E6%2588%25B72631208437%26fmp%3D%26lcp%3D; SUB=_2A257WoGbDeRxGeRI6FMT8CbIyDuIHXVYEfRTrDV8PUNbvtBeLRH1kW8KwiqybdCO4kMlXL5sACQBGPOP8w..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFW0sbnBz3W8AYO-kcqOSK95JpX5KMt; SUHB=010HZV7P_WpcKK; ALF=1480598859; SSOLoginState=1449062859; _s_tentry=login.sina.com.cn; Apache=1144701824523.5085.1449062871863; UOR=bbs.miercn.com,widget.weibo.com,login.sina.com.cn; ULV=1449062871882:9:2:4:1144701824523.5085.1449062871863:1449062694837'}
        url = 'http://weibo.com/u/2631208437/home?wvr=5&lf=reg'
        req = urllib2.Request(url, headers = headers)
        try:
            r = urllib2.urlopen(req)
            text = r.read()
            f = open(filename, 'w')
            f.write(text)
            f.close()
            print "get page success!"
            return 1
        except:
            print "get page error!"
            return -1




