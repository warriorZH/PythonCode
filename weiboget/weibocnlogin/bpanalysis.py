import sys
import os
import time
import urllib2
from bs4 import *

fd = open('homepage', 'r')
html_doc = fd.read()
fd.close()
soup = BeautifulSoup(html_doc,'lxml')
bp_fd = open('homepage_bp', 'w')
text = soup.title
print text
bp_fd.write(str(soup))
bp_fd.close()
print soup.title
