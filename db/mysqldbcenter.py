import MySQLdb

conn = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='root',
    db='develop'
    )


def getConn():
    return conn


def closeConn():
    conn.close()


def insertRow(sql, param):
    try:
        cur = conn.cursor()
        cur.execute(sql, param)
        conn.commit()
    except Exception as e:
        print e
    finally:
        cur.close
        conn.close
