#/usr/bin/env python

def displayNumType(num):
    print num," is",
    if isinstance(num,(int,long,float,complex)):
        print ' a number of type :',type(num).__name__
    else:
        print 'not a number at all!'
displayNumType(-69)
displayNumType(999999999999L)
displayNumType(98.6)
displayNumType(-5.2+1.9j)
displayNumType('xxx')

import types
def displayNumType2(num):
    print num,'is',
    if type(num)==types.IntType:
        print "a integer"
    elif type(num) is types.LongType:
        print "a Long"
    elif type(num)==type(0.0):
        print "a float"
    elif type(num)==type(0+0j):
        print "a complex"
    else:
        print "not a number at all"
print
displayNumType2(-69)
displayNumType2(999999999999L)
displayNumType2(98.6)
displayNumType2(-5.2+1.9j)
displayNumType2('xxx')