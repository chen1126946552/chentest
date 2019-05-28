# -*- coding: UTF-8 -*-

# 链接mysql库, 针对表进行增删改查


import pymysql.cursors
import random

# 连接数据库
connect = pymysql.Connect(
    host='192.168.1.2',
    port=3306,
    user='ptone',
    passwd='ptone',
    db='ao_test',
    charset='utf8'
)

# 获取游标
cursor = connect.cursor()
j = 1
for i in range(0,110000):
    s1 = str(j) + "test"
    sql = "INSERT INTO data10 (id, num1, num2, string1) VALUES ( '%d', '%d','%d','%s')"
    data = (i, random.randint(j*1000,j*10000), random.randint(j*100,j*1000), s1)
    cursor.execute(sql %data)
    connect.commit()
    if i % 10200 == 0:
        j += 1

cursor.close()
connect.close()