#!/usr/bin/env python

'makeTestFile.py -- create text file'

import os
ls=os.linesep

fname=raw_input("Enter write filename:")
while True:
    if os.path.exists(fname):
        print "ERROR: '%s' is already exist " % fname
        fname = raw_input("Enter filename:")
    else:
        break

all=[]
print "\nEnter lines ('.' by itself to quit).\n"

while True:
    entry=raw_input(">")
    if entry=='.':
        break
    else:
        all.append(entry)

fobj=open(fname,"w")
fobj.writelines(['%s%s' %(x,ls) for x in all])
fobj.close()
print 'DONE!'


fname=raw_input("Enter read filename:")
print

try:
    fobj=open(fname,"r")
except IOError,e:
    print "file open error",e
else:
    for eachline in fobj:
        print eachline,
    fobj.close()

