#! /usr/bin/env python
# -*- coding: utf-8 -*-

#filename: weiboLogin.py
#description:
#   login in to the sina weibo
#writer: warrior mail:15933533880@163.com

#import package
import weiboLogin
import urllib
import urllib2
import time

filename = 'account'
WBLogin = weiboLogin.weiboLogin()
if WBLogin.login(filename) == 1:
    print 'Login success!'
else:
    print 'Login error!'
    exit()
