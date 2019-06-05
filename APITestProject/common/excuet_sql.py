import pymysql

# 数据准备
# DELETE from hello_teacher WHERE teacher_name = 'test0002';
def delete_sql(sql_delete):
    # 打开数据库连接
    db = pymysql.connect(host='47.104.190.48',
                         port=3306,
                         user='root',
                         passwd='root',
                         db='django')

    # 使用 cursor() 方法创建一个游标对象cur
    cur = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cur.execute(sql_delete)

    # 一定要提交
    db.commit()
    db.close()