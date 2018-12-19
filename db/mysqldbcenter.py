import MySQLdb

conn = MySQLdb.connect(
    host='localhost', user='root', passwd='root', db='develop')


def getConn():
    return conn


def closeConn():
    conn.close()


def insertRow(sql, param):
    try:
        # conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='develop')
        cur = conn.cursor()
        cur.execute(sql, param)
        conn.commit()
    except Exception as e:
        print e
    finally:
        cur.close
        # conn.close


def getAll(sql, param):
    try:
        conn = MySQLdb.connect(
            host='localhost', user='root', passwd='root', db='develop')
        conn.set_character_set('utf8')
        cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute(sql, param)
        result = cur.fetchall()
        return result
    except Exception as e:
        print e
    finally:
        cur.close()
        conn.close()


def getOne(sql, param):
    try:
        conn = MySQLdb.connect(
            host='localhost', user='root', passwd='root', db='develop')
        cur = conn.cursor()
        cur.execute(sql, param)
        result = cur.fetchone()
        if result is None:
            return result
        return result[0]
    except Exception as e:
        print e
    finally:
        cur.close()
        conn.close()


def delall(sql, param):
    try:
        cur = conn.cursor()
        delnum = cur.execute(sql, param)
        conn.commit()
        return delnum
    except Exception as e:
        print e
    finally:
        pass
