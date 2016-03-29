#!/usr/bin/python
#filename: searchengine.py
#input: onne
#output: none
#writer: mail:15933533880@163.com

from pysqlite2 import dbapi2 as sqlite
import urllib2
from BeautifulSoup import *
from urlparse import urljoin
import pdb


#create a not useful word list
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])
class crawler:
    """
    This is a crawler class.
    It contains the statement of some function
    """
    #initial crawler class
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)
    
    def __del__(self):
        self.con.close()

    def dbcommit(self):
        pass

    #get the id of entry or add it into db
    def getentryid(self, table, field, value, createnew=True):
        cur = self.con.execute(
                "select rowid from %s where %s = '%s'" % (table, field, value))
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute(
                    "insert into %s (%s) values ('%s')" % (table, field, valaue))
            return cur.lastrowid
        else:
            return res[0]

    #create indexs of all url
    def addtoindex(self, url, soup):
        pass

    #get text from HTML
    def gettextonly(only, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()
    #manage the separate words process
    def separatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s!='']

    #judge the index repeat
    def isindexed(self, url):
        u = self.con.execute(
                "select rowid from urllist where url='%s'" % url).fetchone()
        if u!=None:
            #the url is exist, and examine it if has been retrievaled 
            v = self.con.execute(
                    "select * from wordlocation where urlid = '%d'" % u[0] ).fetchone()
            if v!=None:
                return True
        return False

    #add a link
    def addlinkref(self, urlFrom, urlTo, linkText):
        pass

    def crawl(self, pages, depth=2):
        for i in range(depth):
            newspages = set()
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print "Could not open %s" % page
                    continue
                soup = BeautifulSoup(c.read())

    #create DB
    def createindextables(self):
        self.con.execute('create table urllist(url)') 
        self.con.execute('create table wordlist(word)') 
        self.con.execute('create table wordlocation(urlid, wordid, location)') 
        self.con.execute('create table link(fromid integer, toid integer)') 
        self.con.execute('create table linkwords(wordid, linkid)')
        self.con.execute('create index wordidx on wordlist(word)') 
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)') 
        self.con.execute('create index urltoidx on link(toid)') 
        self.con.execute('create index urlfromidx on link(fromid)') 
        self.dbcommit()


class searcher:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()
    
    def getmatchrows(self, q):
        #create query list
        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]

        #split word depend on space ' '
        words = q.split(' ')
        tablenumber=0

        #excute query list
        for word in words:
            wordrow = self.con.execute(
                    "select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow != None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    tablelist += ' ,'
                    clauselist += ' and '
                    clauselist += 'w%d.urlid=w%d.urlid and ' % (tablenumber-1, tablenumber)
                fieldlist += ' , w%d.location' % tablenumber
                tablelist += ' wordlocation w%d' % tablenumber
                clauselist += 'w%d.wordid=%d' % (tablenumber, wordid)
                tablenumber += 1

        #execute query command
        fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]

        return rows, wordids
    

    def geturlname(self, uid):
        return self.con.execute(
                "select url from urllist where rowid=%d" % uid).fetchone()[0]

    
    def getscoredlist(self, rows, wordids):
        totalscores = dict([(row[0], 0) for row in rows])

        #evaluate function
        #weights = [(1.0, self.frequencyscore(rows))]
        weights = [(1.0, self.locationscore(rows)), (1.5, self.frequencyscore(rows))]

        for (weight, scores) in weights:
            for url in totalscores:
                totalscores[url] += weight*scores[url]
        return totalscores

    def query(self, q):
        rows, wordids = self.getmatchrows(q)
        scores = self.getscoredlist(rows, wordids)
        rankedscores = sorted([(score, url) for (url, score) in scores.items()], reverse=1)
        for (score, urlid) in rankedscores[0:10]:
            print '%f\t%s' %  (score, self.geturlname(urlid))

    def normalizescores(self, scores, smallIsBetter=0):
        vsmall = 0.00001
        if smallIsBetter:
            minscore = min(scores.values())
            return dict([(u, float(minscore)/max(vsmall, l)) for (u,l) in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0:
                maxscore = vsmall
            return dict([(u, float(c)/maxscore) for (u,c) in scores.items()])

    def frequencyscore(self, rows):
        counts = dict([(row[0], 0) for row in rows])
        for row in rows:
            counts[row[0]] += 1
        return self.normalizescores(counts)

    def locationscore(self,rows):
        locations = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            loc = sum(row[1:])
            if loc < locations[row[0]]:
                locations[row[0]] = loc

        return self.normalizescores(locations,smallIsBetter=1)
