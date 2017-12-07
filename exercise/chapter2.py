# coding=utf-8

# 操作符练习
print("-" * 20 + "操作符练习" + "-" * 20)
print -2 * 4 + 3 ** 2
print not 6.2 < 6

# 变量练习
print("-" * 20 + "变量练习" + "-" * 20)
counter = 0
miles = 1000.0
name = 'Bob'
counter = counter + 1
kilometers = 1.609 * miles
print '%f miles is the same as %f km' % (miles, kilometers)

print("-" * 20 + "数字练习" + "-" * 20)
print(6.23 + 1.5j)

# 字符串练习
print("-" * 20 + "字符串练习" + "-" * 20)
pystr = "python"
iscool = "is cool!"
print pystr[0]
print pystr[2:5]
print iscool[:2]
print iscool[3:]
print iscool[-1]  # -1表示最后一个字符
print pystr + iscool
print pystr + ' ' + iscool
print pystr * 2
print '-' * 20
print 'python \nis cool'  # 使用换行符

# 列表和数组练习
# 列表练习
print("-" * 20 + "列表和数组练习" + "-" * 20)
aList = [1, 2, 3, 4]
print aList
print aList[0]
print aList[1:]
print aList[:2]
aList[1] = 8
print aList

# 元组练习
aTuple = ("robots", 77, 93, "try")
print aTuple
print aTuple[1]
print aTuple[1:]
print aTuple[:2]
# aTuple[1]=5   不支持赋值
print aTuple

# 字典练习
print("-" * 20 + "字典练习" + "-" * 20)
aDict = {'host': 'earth'}
print aDict
aDict['port'] = 80
print aDict

print aDict['host']
print aDict.keys()
for key in aDict.keys():
    print key, aDict[key]

# for循环和range内建函数
print("-" * 20 + "循环和内建函数" + "-" * 20)
for eachNum in range(3):
    print eachNum
for c in "abc":
    print c

foo = "abc"
for i in range(len(foo)):
    print foo[i], '(%d)' % i

squared = [x ** 2 for x in range(4)]
print squared

sqdEvents = [x ** 2 for x in range(8) if not x % 2]
print sqdEvents

# 读写文件
print("-" * 20 + "读写文件操作" + "-" * 20)
fobj = open("/Users/yangjie/tmp/python", 'r')
for eachLine in fobj:
    print eachLine,
fobj.close()
print

# 异常处理
print("-" * 20 + "异常处理" + "-" * 20)

# try:
#     filename=raw_input('Enter file name:')
#     fobj=open(filename,'r')
#     for eachLine in fobj:
#         print eachLine,
#     fobj.close()
# except IOError,e:
#     print 'file open error',e

# 函数处理
print("-" * 20 + "函数处理" + "-" * 20)


def addMe2Me(x):
    print("apply + operation to argument:")
    return x + x


print addMe2Me(4.5)
print addMe2Me(8)
print addMe2Me('python')
print addMe2Me([1, 2, 3])

# 类定义
print("-" * 20 + "类定义" + "-" * 20)


class FooClass(object):
    """my very first class :FooClass"""
    version = 1

    def __init__(self, nm='Jone Doe'):
        """constructor"""
        self.name = nm
        print 'Created a class instance for ', nm

    def showname(self):
        """display instance attribute and class name"""
        print 'your name is ', self.name
        print 'my name is ', self.__class__.__name__

    def showver(self):
        """show class static attribute"""
        print self.version

    def addMe2Me(x):
        return x + x


fool = FooClass()
fool.showname()
fool.showver()

fool2=FooClass("yangjie")
fool2.showname()
fool2.showver()


#模块概念
import sys
sys.stdout.write("Hello World!")
print sys.platform
print sys.version

print type(111)
print dir(foo)

