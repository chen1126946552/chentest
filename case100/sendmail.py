# -*- coding: utf-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText

file_name='./jmeter.log'

file_object = open(file_name,'r')

try:
     data = file_object.read( )
finally:
     file_object.close()

if len(data)>0:
    server = smtplib.SMTP('smtp.163.com', '25')
    server.login('datatest30', '123456P')
    msg = MIMEText('测试报告详情参考：\n[http://172.20.101.102:8088/PTOnline/InterfaceUsability/CN/TestReport_2018-07-10_19_08.html]', 'plain', 'utf-8')
    msg['From'] = 'datatest30@163.com <datatest30@163.com>'
    msg['Subject'] = Header(u'Ptengine_接口可用性_中国区_AUTO_检查失败1', 'utf8').encode()
    msg['To'] = 'datatest30@163.com <datatest30@163.com>'
    server.sendmail('datatest30@163.com', ['datatest30@163.com'], msg.as_string())
    server.quit()
else:
    quit()
