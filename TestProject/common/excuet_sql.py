# -*- coding: utf-8 -*-

import pymysql


def engage_sid_sql():
    # 打开数据库连接
    db = pymysql.connect(host='ptconftestdb.ptfuture.cn',
                         port=23306,
                         user='ptmind',
                         passwd='ptmind2012',
                         db='ptmind_common')

    # 使用 cursor() 方法创建一个游标对象cur
    cur = db.cursor()

    sql = 'select DISTINCT sid from pt_engage_base WHERE `status`=1 and deleted=0;'
    # 使用 execute()  方法执行 SQL 查询
    cur.execute(sql)
    r = []
    for i in cur.fetchall():
        s = {'sid':i[0]}
        r.append(s)
    return r

    # 一定要提交
    db.commit()
    db.close()

if __name__ == "__main__":
    print(engage_sid_sql())