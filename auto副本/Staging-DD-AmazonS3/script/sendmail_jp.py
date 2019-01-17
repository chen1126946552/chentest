# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import datetime
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import time
import os
import sys
import requests
reload(sys)
sys.setdefaultencoding('utf8')

qa_host="http://172.19.8.191:8088/"
qa_path="datadeck_DataSource/AmazonS3/"
qa_file="DATADECK_JP_TestReport_"
subject = 'datadeck interface result'

jpfile_name='/data/www/qa/logs/datadeck_DataSource/AmazonS3/jp_datadeck_interface.txt'
jpfile_error_name='/data/www/qa/logs/datadeck_DataSource/AmazonS3/errlog/jp_datadeck_interface_errlog.txt'
DIR='/data/www/qa/datadeck_DataSource/AmazonS3/'
file_object_error = open(jpfile_error_name,'r')

#获取路径下最新文件
def compare(x, y):
    stat_x = os.stat(DIR +  "/" + x)
    stat_y = os.stat(DIR +  "/" + y)
    if stat_x.st_ctime < stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime > stat_y.st_ctime:
        return 1
    else:
        return 0
items = os.listdir(DIR)
items.sort(compare)	

a = items[len(items) - 1]
now_date = a[-21:-5]
#msg="JP_DATADECK_interface_check result detail:  "+qa_host+qa_path+qa_file+now_date+'.html'
msg=qa_host+qa_path+qa_file+now_date+'.html'
#towho = '<!here|here>'
towho = 'here'
#slackQaUrl = "https://hooks.slack.com/services/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"
slackQaUrl = "https://hooks.slack.com/services/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"
failmsg = '测试报告详情参考：'
#slacktext =  '{0}\n{1} DataDeck日本区接口可用性测试失败：\nzhen.qin\n{2}\n{3}'.format(towho, now_date, failmsg, msg)

try:
     jpdata = file_object_error.read()
finally:
     file_object_error.close()
print items[len(items) - 1]
print len(jpdata)

if len(jpdata)>100:
	fileObjectWrite = open('sampleList_jp.txt', 'a')
	fileObjectWrite.write(msg+'  \n')
	fileObjectWrite.close()
else:
	fileObjectWrite = open('sampleList_jp.txt', 'w')
	fileObjectWrite.write('')
	fileObjectWrite.close()
		
fileObject = open('sampleList_jp.txt', 'r') 

#print fileObject.read()
lines = fileObject.readlines()
print len(lines)

for line in lines:                          #依次读取每行  
	line = line.strip() #去掉每行头尾空白 
	print "读取的数据为: %s" %(line)	
	
print lines

slacktext =  '{0}\n{1} 日本区DDv2_DS_Amazon S3_AUTO_检查失败：\nzhen.qin\n{2}\n{3}'.format(towho, now_date, failmsg, lines)

if len(lines)>0:
	try:
		requests.post(slackQaUrl, json = {'text': slacktext})
		#requests.post(slackQaUrl, json = {'text': lines})

		print "send message success"
		fileObject.close()
		fileObjectWrite = open('sampleList_jp.txt', 'w')
		fileObjectWrite.write('')
		fileObjectWrite.close()
	except smtplib.SMTPException:
		print "Error: send message fail"
		fileObject.close()
else:
	fileObject.close()
quit()