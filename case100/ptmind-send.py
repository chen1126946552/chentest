# -*- coding: utf-8 -*-
import datetime
import time
import os
import requests

qa_host = "http://qatest.ptmind.com/"
qa_path = "/logs/102jenkins/"
qa_file = "TestReport_"
subject = 'ptengine interface result'

jpfile_name = '/data/www/qa/logs/102jenkins/Jenkins-102.txt'
jpfile_error_name = 'a.csv'
DIR = './'
file_object_error = open(jpfile_error_name, 'r')


# 获取路径下最新文件
# def compare(x, y):
#     stat_x = os.stat(DIR + "/" + x)
#     stat_y = os.stat(DIR + "/" + y)
#     if stat_x.st_ctime < stat_y.st_ctime:
#         return -1
#     elif stat_x.st_ctime > stat_y.st_ctime:
#         return 1
#     else:
#         return 0
#
items = os.listdir(DIR)
items.sort(key=lambda fn: os.path.getmtime(os.path.join(DIR, fn)))
print(items[-1])
a = items[len(items) - 1]
now_date = a[-21:-5]

msg = qa_host + qa_path + qa_file + now_date + '.html'

towho = '<!here|here>'

# Slack频道=【ptengine_develop】，ptengine开发群
slackQaUrl = "https://hooks.slack.com/services/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ddddddd"

failmsg = '测试报告详情参考：'

try:
    jpdata = file_object_error.read()
finally:
    file_object_error.close()
print(items[len(items) - 1])
print(len(jpdata))

if len(jpdata) > 100:
    fileObjectWrite = open('sampleList.txt', 'a')
    fileObjectWrite.write(msg + '  \n')
    fileObjectWrite.close()
else:
    fileObjectWrite = open('sampleList.txt', 'w')
    fileObjectWrite.write('')
    fileObjectWrite.close()

fileObject = open('sampleList.txt', 'r')

lines = fileObject.readlines()
print(len(lines))

for line in lines:  # 依次读取每行
    line = line.strip()  # 去掉每行头尾空白
    print("读取的数据为: %s" % (line))

print(lines)

slacktext = '{0}\n{1} Jenkins_中国区_172.20.101.102_页面访问失败1，速速检查：\n{2}\n{3}'.format(towho, now_date, failmsg, lines)
# 这里的信息，显示在slack中

if len(lines) > 0:
    try:
        requests.post(slackQaUrl, json={'text': slacktext})
        # requests.post(slackQaUrl, json = {'text': lines})

        print("send message success")
        fileObject.close()
        fileObjectWrite = open('sampleList.txt', 'w')
        fileObjectWrite.write('')
        fileObjectWrite.close()
    except:
        print("Error: send message fail")
        fileObject.close()
else:
    fileObject.close()
quit()