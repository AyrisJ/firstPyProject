# coding=utf-8

import time

if __name__=='__main__':
    t1 = time.time()
    time.sleep(5)
    t2 = time.time()
    print t2 - t1
    print __name__
    print time.__name__

