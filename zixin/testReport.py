# coding=utf8

import urllib2

fileUrl = "http://localhost:10001/CreditInfo/BasicPersonInfor/1/1/100/440881199307254155/2018-06-01/0"
response = urllib2.urlopen(fileUrl, timeout=300)
print response

