from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import selenium
import sys
import os
import time
import urllib2


sel = selenium.webdriver.Chrome()
loginurl = 'http://login.weibo.cn/login/'
#open the login in page
sel.get(loginurl)
time.sleep(2)
#sign in the username
try:
    sel.find_element_by_xpath("//form[@method='post']/div[1]/input[1]").send_keys('15933533880')
    print 'user success!'
except:
    print 'user error!'
time.sleep(1)
#sign in the pasword
try:
    sel.find_element_by_xpath("//form[@method='post']/div[1]/input[2]").send_keys('675979')
    print 'pw success!'
except:
    print 'pw error!'
time.sleep(1)
#click to login
try:
    sel.find_element_by_xpath("//form[@method='post']/div[1]/input[8]").click()
    print 'click success!'
except:
    print 'click error!'
time.sleep(1)
curpage_url =  sel.current_url
print curpage_url
while(curpage_url == loginurl):
    #print 'please input the verify code:'
    #verifycode = sys.stdin.readline()
    #sel.find_element_by_xpath("//div[@id='pl_login_form']/div/div[2]/div[3]/div[1]/input").send_keys(verifycode)
    try:
        sel.find_element_by_xpath("//form[@method='post']/div[1]/input[8]").click()
        print 'click success!'
    except:
         print 'click error!'
    time.sleep(1)
    curpage_url = sel.current_url
print '***out the while'
#get the session cookie
for wer in sel.get_cookies():
    for asd in wer:
        print asd
print '####################################'
cookie = [item["name"] + "=" + item["value"] for item in sel.get_cookies()]
print cookie
print '#####################################'
cookiestr = ';'.join(item for item in cookie)
print cookiestr

print '%%%using the urllib2 !!'
homeurl = sel.current_url
print 'homeurl: %s' % homeurl
headers = {'cookie':cookiestr}
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.130 Chrome/43.0.2357.130 Safari/537.36'
req = urllib2.Request(homeurl)
req.add_header('Referer', homeurl)
req.add_header('User-Agent', user_agent)
req.add_header('cookie', cookiestr)
try:
    response = urllib2.urlopen(req)
    text = response.read()
    fd = open('homepage', 'w')
    fd.write(text)
    fd.close()
    print '###get home page html success!!'
except:
    print '### get home page html error!!'
#try:
#    sel.find_element_by_xpath("//div[@class='W_person_info']/div[2]/ul/li[2]/a").click()
#    print 'click success!'
#except:
#    print 'click error!'
#time.sleep(3)
#followerpage = sel.current_url
#print '@@@follower page url: %s' % followerpage

