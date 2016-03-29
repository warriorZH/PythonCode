#!/usr/bin/python
# -*- coding: <encoding name> -*-
#filename: crawler.py
#input:
#output:
#writer: warrior 15933533880@163.com

import urllib2
import pdb
import os
import re
import string
class crawlertest:
    """ 
    this is a crawler test demo
    """
    def __init__(self):
        url = ''


    def __del__(self):
        pass

    def getContFromUrl(self, url):
        try:
            contentfile = urllib2.urlopen(url)
        except:
            print "Can not open the url %s",url
        #allCont = contentfile.read() 
        for i in range(200):
            lineCont = contentfile.readline()
            #print allCont
            gettitle = re.compile('(?<=<title>).+')
            urltitle = gettitle.findall(lineCont)
            if urltitle:
                urltitle = urltitle[0][:-9]
                print lineCont
                print urltitle
            else:
                pass
                #print 'None'
        contentfile = urllib2.urlopen(url)
        httpcodefile = open('httpcodefile', 'w')
        temp = contentfile.read()
        print temp
        httpcodefile.write(contentfile.read())
        httpcodefile.close()

