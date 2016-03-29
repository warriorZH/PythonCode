#!/usr/bin/python
#FileName: OpFile.py

import sys
f = open('somefile.txt', 'w')
f.write('Hello, ')
f.write('World!!\n')
f.write('I am ')
f.write('working in BeiJing!!\n')
f.write('Hello, ')
f.write('World!!\n')
f.close()

f = open('somefile.txt', 'r')
content = f.readline()
print content
content = f.readline(2)
print content
content = f.read(4)
print content
content = f.read()
print content
