# coding=utf8

import pymysql
from DBUtils.PooledDB import PooledDB

dbinfo = {
    'host': '127.0.0.1',
    'username': 'root',
    'passwd': 'root',
    'dbname': 'develop'
}


# 获取数据库链接
def getconn():
    pool = PooledDB(
        pymysql,
        2,
        host=dbinfo['host'],
        user=dbinfo['username'],
        passwd=dbinfo['passwd'],
        db=dbinfo['dbname'])
    conn = pool.connection()
    return conn


# 获取返回字典值的游标
def getdictcur():
    conn = getconn()
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return cur


# 获取常用游标
def getcommoncur():
    conn = getconn()
    cur = conn.cursor()
    return cur


def insertRow(sql, param):
    conn = getconn()
    cur = conn.cursor()
    try:
        cur.execute(sql, param)
        conn.commit()
    except Exception, e:
        print e
    finally:
        cur.close()
        conn.close()


# 查询单个结果,使用常用游标
def getone(sql, param):
    try:
        cur = getcommoncur()
        cur.execute(sql, param)
        ret = cur.fetchone()
        return ret[0]
    except Exception as e:
        print e


# 查询单条结果
def getrow(sql, param):
    try:
        cur = getdictcur()
        cur.execute(sql, param)
        ret = cur.fetchall()
        return ret[0]
    except Exception as e:
        print e


# 查询所有结果集
def getall(sql, param):
    cur = getdictcur()
    cur.execute(sql, param)
    ret = cur.fetchall()
    return ret


# 连接数据库测试
def conndb1(sql, dbinfo, param):
    db = pymysql.connect(dbinfo['host'], dbinfo['username'], dbinfo['passwd'],
                         dbinfo['dbname'])
    cur = db.cursor()
    cur.execute(sql, param)
    data = cur.fetchone()
    print data[0]
    cur.close()
    db.close()


# 连接数据库测试2---使用连接池
def conndb2(sql, dbinfo, param):
    pool = PooledDB(
        pymysql,
        2,
        host=dbinfo['host'],
        user=dbinfo['username'],
        passwd=dbinfo['passwd'],
        db=dbinfo['dbname'])
    conn = pool.connection()
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql, param)
    result = cur.fetchall()
    cur.close()
    conn.close()
    print result
    print result[1]
    print result[1]['user_name']


# 下面是正文可执行代码

if __name__ == '__main__':
    sql = '''
        insert into user_phone_call_6m(dial_cnt_6m,call_cnt_6m,peer_num) values(%s,%s,%s)
    '''
    insertRow(sql, (11, 22, "13622986989",))
