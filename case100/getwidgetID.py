# -*- coding: UTF-8 -*-
# 链接mysql库,获取widgetid和uid

import pymysql.cursors
import sys

filename = 'widgetID_List1.csv'
spaceid = (sys.argv[1],)

# 连接数据库
connect = pymysql.Connect(
    host='initdb.datadeck.com',
    port=13327,
    user='Ptddreadonly',
    passwd='$)JKRnK5Xb',
    db='datadeck',
    charset='utf8'
)

# 获取游标
cursor = connect.cursor()

# 查询数据
sql = "SELECT widget_id,uid FROM v_ptone_widget_info_ex WHERE space_id = '%s' and widget_status=1 and  ds_id=12 and is_demo=0"
cursor.execute(sql % spaceid)

fl = open(filename, "w+")

for row in cursor.fetchall():
    print("%s,%s" % row)
    # 将list,写入文件中
    fl.writelines("%s,%s" % row)
    fl.write('\n')

fl.close()

print('共查找出', cursor.rowcount, '条数据')

# 关闭连接
cursor.close()
connect.close()