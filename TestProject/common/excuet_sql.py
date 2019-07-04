# -*- coding: utf-8 -*-

import pymysql
import config.config


def engage_sid_sql():
    # 打开数据库连接
    db = pymysql.connect(host=config.config.HOST,
                         port=config.config.PORT,
                         user=config.config.USER,
                         passwd=config.config.PASSWD,
                         db='ptmind_common')

    # 使用 cursor() 方法创建一个游标对象cur
    cur = db.cursor()

    sql = 'select DISTINCT pt_engage_base.sid from pt_engage_base INNER JOIN ref_site_status ON ref_site_status.sid = pt_engage_base.sid WHERE pt_engage_base.`status`=1 and pt_engage_base.deleted=0 and ref_site_status.`status`=1;'

    # 使用 execute()  方法执行 SQL 查询
    cur.execute(sql)
    r = []
    for i in cur.fetchall():
        s = {'sid':i[0]}
        r.append(s)

    # 一定要提交
    db.commit()
    db.close()

    return r

# 将数据插入数据库中
def engage_data_sql(filename, tablename):
    # 打开数据库连接
    db = pymysql.connect(host='139.220.242.36',
                         port=23306,
                         user='qa_auto',
                         passwd='qa_auto',
                         db='qa_auto_ptengine',
                         charset='utf8',
                         local_infile=1)
    # 使用 cursor() 方法创建一个游标对象cur
    sql = "load data local infile '{0}' into table {1} fields terminated by ',' lines terminated by '#'" .format(filename, tablename)
    print(sql)
    cur = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cur.execute(sql)

    # 一定要提交
    db.commit()
    db.close()

if __name__ == "__main__":
#    print(engage_sid_sql())
    engage_data_sql("event.csv","inter_elapsed_time")
