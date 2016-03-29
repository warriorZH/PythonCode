#!/bin/python
#filename: generatefeedvector.py
#input: none
#output: none
#writer: warrior
#mail: 15933533880

import feedparser
import re

def getwordcounts(url):
    #analysis RSS feed
    d = feedparser.parse(url)
    wc = {}
#   print d
    #ergodic all article in circulate
    for e in d.entries:
        if 'summary' in e: summary = e.summary
        else: summary = e.description

        #extract sord list
        words = getwords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
   # return d.feed.title,wc
    return getattr(d.feed, 'title', 'Unknown title'), wc


def getwords(html):
    #remove all html sign
    txt = re.compile(r'<[^>]+>>').sub('',html)

    #use the character but not letter to resolution word
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    #turn to lower case
    return [word.lower() for word in words if word!='']


apcount = {}
wordcounts = {}
feedlist = [line for line in file('feedlist.txt')]
for feedurl in feedlist:
    title,wc = getwordcounts(feedurl)
    wordcounts[title] = wc
    for word,count in wordcounts.items():
        apcount.setdefault(word,0)
        if count > 0:
            apcount[word] += 1


wordlist = []
for w,bc in apcount.items():
    frac = float(bc)/len(feedlist)
    if frac>0.1 and frac<0.5 : 
        wordlist.append(w)

out = file('blogdata.txt', 'w')
out.write('Blog')
for word in wordlist:
    out.write('\t%s', word)
out.write('\n')
for blog,wc in wordcounts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t%d' % wc[word])
        else:
            out.write('\t0')
        out.write('\n')
out.close()
