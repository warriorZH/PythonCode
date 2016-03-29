#! /usr/bin/env python
# -*- coding: utf-8 -*-

#filename: getcookie.py
#description:
#   
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

class gethtml(object):
    '''get the request 
        with specify url and cookie
    '''
    def __init__(self, url, cookie, filename):
        self.cookie = cookie
        self.url = url
        self.filename = filename


    def getpagecont(self, filename):
        url ='http://login.sina.com.cn/member/my.php?entry=sso'
        headers = {'cookie':'ac%3D25%26bt%3D1449197540%26cv%3D5.0%26et%3D1480733540%26uid%3D2631208437%26vf%3D0%26vs%3D0%26vt%3D0%26es%3De51beb95c808b02eb7c0d47a07d1cea1'}
        cj = cookielib.FileCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #urllib2.install_opener(opener)

        #headers = {'cookie':cookie}
        req = urllib2.Request(url, headers = headers)
        try:
            r = opener.open(req)
            text = r.read()
            f = open(filename, 'w')
            f.write(text)
            f.close()
            print 'get page success!'
        except:
            print 'get page error!'
        if cj:
            print 'get cookie success!'
            print cj
            cj.save('cookiefile')
        else:
            print 'get cookie error!'

































