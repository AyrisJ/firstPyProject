# coding=utf8

#使用Threading模块创建线程

import threading
import time


existFlag=0


class MyThread(threading.Thread):
    def __init__(self,threadID,threadName,delay):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.threadName=threadName
        self.delay=delay

    def run(self):
        print "Starting "+self.threadName
        print_time(self.threadName,self.delay,5)
        print "Exiting "+self.threadName


def print_time(threadname,delay,counter):
    while counter:
        if existFlag:
            threading.Thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadname,time.ctime(time.time()))
        counter-=1


thread1=MyThread(1,"thread-1",1)
thread2=MyThread(2,"thread-2",2)

thread1.start()
thread2.start()

print "Exiting Main Thread"





