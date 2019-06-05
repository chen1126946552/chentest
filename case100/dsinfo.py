# -*- coding: UTF-8 -*-

# 链接测试的mysql库, 针对表进行查询和修改
import pymysql.cursors

# 连接数据库
connect = pymysql.Connect(
    host='192.168.1.2',
    port=3306,
    user='ptone',
    passwd='ptone',
    db='ptone_test_9999',
    charset='utf8'
)

# 获取游标
cursor = connect.cursor()


# 查询数据
sql = "SELECT name,config FROM ptone_ds_info WHERE code = '%s' "
data = ('googleanalysis',)
cursor.execute(sql % data)
for row in cursor.fetchall():
#    print("Name:%s\tconfig:%s" % row)
    print(row[0])
    print(row[1])
print('共查找出', cursor.rowcount, '条数据')


# 关闭连接
cursor.close()
connect.close()