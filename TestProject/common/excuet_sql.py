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

# 将数据插入数据库中
def engage_data_sql(filename):
    # 打开数据库连接
    db = pymysql.connect(host='139.220.242.36',
                         port=23306,
                         user='qa_auto',
                         passwd='qa_auto',
                         db='qa_auto_ptengine',
                         charset='utf8',
                         local_infile = 1)
    # 使用 cursor() 方法创建一个游标对象cur
    sql = "load data local infile '{0}' into table inter_elapsed_time fields terminated by ',' lines terminated by '#'" .format(filename)
    print(sql)
    cur = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cur.execute(sql)

    # 一定要提交
    db.commit()
    db.close()

if __name__ == "__main__":
#    print(engage_sid_sql())
    engage_data_sql("dc.csv")
