#encoding=utf-8
#2.1
# var1=raw_input("type your name:")
# print var1

print "yangjie2"

var2="yangjie3"
var3=123456
print '%s，%d' %(var2,var3)

#! /usr/bin/env python
print 1+2*4

#2.3
num1=5.0
num2=2
print num1*num2,num1/num2,num1%num2,num1**num2

#2.4
# numstr=raw_input("num str:")
# print type(numstr)
# numstr=int(numstr)
# print type(numstr)

#2.5
list1=[0,1,2,3,4,5,6,7,8,9,10]
for item in list1:
    print item,
print
for item in range(11):
    print item,
print

#2.6
# isnum=raw_input("type a num:")
# isnum=int(isnum)
isnum=101
if isnum>0:
    print ">0"
elif isnum==0:
    print "=0"
else:
    print "<0"

#2.7
# str=raw_input("type a str:")
str111="abcdefg"
strleng=len(str111)
index=0
while index<strleng:
    print str111[index],
    index=index+1
print
for index in range(strleng):
    print str111[index],
print

#2.8
list2=[1,2,3,4,5]
arr2=(1,1,1,1,1,1,1)
index=0
sum2=0
# list2=raw_input("type a list:")
for index in range(len(list2)):
    sum2=sum2+list2[index]
print sum2

index=0
sum3=0
# arr2=raw_input("type a arr:")
while index<len(arr2):
    sum3=sum3+arr2[index]
    index=index+1
print sum3

sum4=0
while 1!=1:
    tempNum=raw_input("type a num:")
    if tempNum!="break":
        tempNum=int(tempNum)
        sum4=sum4+tempNum
    else:
        print sum4
        break
        # flag="break"

#2.9
list3=[3,2,3,4,5]
sum5=0
for index in range(len(list3)):
    sum5=sum5+list3[index]

print float(sum5)/len(list3)  #转换成浮点数计算，不然精度会丢失
print sum5/len(list3)

#2.10
while 1!=1:
    tempNum=raw_input("please input a number:")
    tempNum=int(tempNum)
    if 1<=tempNum<=100:
        print "success"
        break
    else:
        print "error,please input again"

# 2.11
while 1!=1:
    print "1. 取五个数的和"
    print "2. 取五个数的平均值"
    print "3. 退出"
    choice=raw_input("请输入你的选择：")
    choice=int(choice)
    if choice==1:
        sumTemp=0
        for index in range(5):
            tempNum=raw_input("输入第%d个数:" % (index+1))
            tempNum=int(tempNum)
            sumTemp=sumTemp+tempNum
        sumTemp=str(sumTemp)
        print "五个数的总和为:"+sumTemp
    elif choice==2:
        sumTemp = 0
        for index in range(5):
            tempNum = raw_input("输入第%d个数:" % (index + 1))
            tempNum = int(tempNum)
            sumTemp = sumTemp + tempNum
        print "五个数的平均值为:",float(sumTemp)/5
    else:
        break;


#2.12
print dir()
print dir
print type(dir)
print dir.__doc__

import sys
print dir()
print dir(sys)
print sys.version,sys.platform


ch1=2
ch2=3
ch3=1
if ch1>ch3:
    (ch1, ch3) = (ch3, ch1)
print ch1,ch2,ch3
if ch2>ch3:
    (ch2, ch3) = (ch3, ch2)
print ch1,ch2,ch3
if ch1>ch2:
    (ch1, ch2) = (ch2, ch1)
print ch1,ch2,ch3

