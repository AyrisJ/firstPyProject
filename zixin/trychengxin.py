# coding=utf-8


"""
@Version : 1.0
@Time    : 2016/8/25 13:56
@Author  : fanzhen
@Contact : fanzhen@nonobank.com
@Site    : www.hellofanfan.com
@File    : trychengxin.py
@Software: PyCharm
"""

import urllib2


import sys

sys.setrecursionlimit(1000)


def collect(i):
    if i == 0:
        exit()
    t = i
    global f
    while 1:
        try:
            n = t/300+1
            name = '/Users/yangjie/Repo_data/zixin/Q10152900H0900201804100'+n.__str__()+'1.txt'

            f = open(name, 'a+')
            print name + ' is open!'

            fileUrl = "http://www.nonobank.com/CreditInfo/BasicPersonInfor/1/" + t.__str__() + "/100/0/2018-06-01/0"

            print fileUrl + " is inuse."

            response = urllib2.urlopen(fileUrl, timeout=300)

            # sleep(5)
            r = response.read()
            # f.write(r)
            f.write(r.decode('utf-8', 'ignore').encode('gbk', 'ignore'))
            f.close()
            print fileUrl + " was ok!"

            t = t + 1
            if r == "":
                f.close()
                break
            if t == 4000:
                f.close()
                break
        except Exception, e:
            print Exception, ":", e
            print t
            collect(t)
    f.close()

    return 0


collect(1)


