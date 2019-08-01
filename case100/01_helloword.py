# -*- coding: UTF-8 -*-
import time
import datetime
import os

# 输出helloworld

print("Hello World")

s1 = 'Hello World'
print(s1)

s2 = "World"
print("Hello",s2)

s3 = "...."
print("Hello %s World %d" %(s3,20))
print("hello %s" %s3)
s2 = '''Hello 'World '''

print(s2)
print(s2.replace("'", ""))

if(os.path.exists("a.txt")):
    os.remove("a.txt")

print(datetime.datetime.now().hour)



today = datetime.date.today()
today_time = int(time.mktime(today.timetuple()))

today_7 = datetime.date.today() + datetime.timedelta(-7)
today_7_time = int(time.mktime(today_7.timetuple()))
print(today)
print(today_time)
print(today_7)
print(today_7_time)
print(int(time.time()*1000))
print(time.time())
print(datetime.datetime.now())
month = datetime.datetime.today().strftime('%m')
print(month)

month = datetime.datetime.now().strftime('%m')
url = 'http://172.20.11.30:9200' + '/pte-checklist-vip-2019' + month + '/doc/'
print(url)