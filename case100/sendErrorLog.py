# -*- coding: utf-8 -*-
import datetime
import time
import os
import sys
import re
import urllib2
import json
import requests

reload(sys)
sys.setdefaultencoding('utf8')

# -----HTML报告：发布路径及报告头-------
# -----域名：调试过程使用-----------
# qa_host="http://192.168.3.22:8088/"
# -----域名：正式上线使用----------
qa_host = "http://qatest.ptmind.com/"
# qa_host="http://172.19.8.100:8088/"
qa_path = "DD/Online/JP/CL/Core/"
qa_file = "TestReport_CL_Core_"

# -----自动化执行结果路径信息-------------------
jpfile_name = '/data/www/qa/logs/DD/Online/JP/CL/Core/dd_interface.txt'
jpfile_error_name = '/data/www/qa/logs/DD/Online/JP/CL/Core/errlog/dd_interface_errlog.txt'
DIR = '/data/www/qa/DD/Online/JP/CL/Core/'
file_object_error = open(jpfile_error_name, 'r')


# -----HTML报告：获取路径下最新文件---------
# stat.st_ctime（i节点最后更改时间）
# 函数compare实现按时间[升序]排序
# os.listdir按文件存取时间顺序列出目录
def compare(x, y):
    stat_x = os.stat(DIR + "/" + x)
    stat_y = os.stat(DIR + "/" + y)
    if stat_x.st_ctime < stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime > stat_y.st_ctime:
        return 1
    else:
        return 0


items = os.listdir(DIR)
items.sort(compare)

# -----HTML报告：从最新的文件中截取时间内容，倒数第6-22个字符----------
a = items[len(items) - 1]
print a
now_date = a[-21:-5]

# -----HTML报告：拼写HTML报告的发布路径---------
report_html = qa_host + qa_path + qa_file + now_date + '.html'
print report_html

# -----Slack通知范围------------------
# towho = '<!here|here>'
towho = 'here'

# -----Slack发布频道设置---------------
# Slack频道=【chen_test】，个人调试频道
# slackQaUrl = "https://hooks.slack.com/services/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"
# Slack频道=【datadeck_develop】，Datadeck开发群
# slackQaUrl = "https://hooks.slack.com/services/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"
# Slack频道=【dd_autotest_online】，线上环境长期观测的自动化项目群
slackQaUrl = "https://hooks.slack.com/services/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"
# Slack频道=【dd_autotest_offline】，Staging环境长期观测的自动化项目群
# slackQaUrl = "https://hooks.slack.com/services/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"

# -----Slack发布消息的描述信息-------------
failmsg = '测试报告详情参考：'

# -----执行结果记录：sampleList.txt--------
# -----读取dd_interface_errlog.txt文件，计算文件字符数量---------
try:
    jpdata = file_object_error.read()
finally:
    file_object_error.close()
print len(jpdata)
# -----当文件字符数量＞100个，则存在异常信息，将报告名称写入sampleList.txt文件---------
# -----当文件字符数量≤100个，则执行结果无异常，清空sampleList.txt文件--------
if len(jpdata) > 100:
    fileObjectWrite = open('sampleList.txt', 'a')
    fileObjectWrite.write(report_html + '  \n')
    fileObjectWrite.close()
else:
    fileObjectWrite = open('sampleList.txt', 'w')
    fileObjectWrite.write('')
    fileObjectWrite.close()

# -----读取文件内容-------
fileObject = open('sampleList.txt', 'r')

# -----读取文件内容行数-------
lines = fileObject.readlines()
print len(lines)
# -----内容行收尾去空格-------
for line in lines:  # 依次读取每行
    line = line.strip()  # 去掉每行头尾空白
    print "读取的数据为: %s" % (line)
# -----打印内容行内容---------
print lines

# -----Slack发布范围、内容详情----------
slacktext = '{0}\n{1} AT_DD_Online_JP_CL_Core_检查失败：\n{2}\n{3}'.format(towho, now_date, failmsg, lines)

# -----Slack通知发布机制：连续N次错误，发送Slack通知--------
# -----当Slack通知发布成功后，清空sampleList.txt文件--------
# -----当Slack通知发布失败后，打印发送信息失败--------------
if len(lines) > 0:
    try:
        requests.post(slackQaUrl, json={'text': slacktext})
        # requests.post(slackQaUrl, json = {'text': lines})
        print "send message success"
        fileObject.close()
        fileObjectWrite = open('sampleList.txt', 'w')
        fileObjectWrite.write('')
        fileObjectWrite.close()
    except smtplib.SMTPException:
        print "Error: send message fail"
        fileObject.close()
else:
    fileObject.close()
quit()
