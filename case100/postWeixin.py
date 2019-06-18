#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# python调用企业微信发送消息命令

# 发送消息命令
# python weixin.py ${人员} 主题 正文
# 例如：
# python3 weixin.py maYun a b
# ./weixin.py maYun n m
# 说明；当一个变量含有多个值或者含有空格、回车符号时，可以使用双引号。
#       当通知所有用户时可以把用户参数设置成"@all"

import requests
import sys
import os
import json
import logging

# 日志模块
# logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s, %(filename)s, %(levelname)s, %(message)s',
#                 datefmt = '%a, %d %b %Y %H:%M:%S',
#                 filename = os.path.join('/tmp','weixin.log'),
#                 filemode = 'a')

# 微信接口参数
# 根据自己申请的企业微信上接口参数调整；
corpid='ww706438937701feec'
appsecret='LN4kjDjuFCNgullXlHhEEjaVsXvlLhdoUf-1DGNIwZc'
agentid=1000005

# touser=sys.argv[1]
# subject=sys.argv[2]
# #toparty=‘3|4|5|6‘
# message=sys.argv[2] + "\n\n" +sys.argv[3]

touser='ChenChen'
subject='TestChen'
#toparty=‘3|4|5|6‘
message='test'

#获取accesstoken
token_url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + appsecret
req=requests.get(token_url)
accesstoken=req.json()['access_token']

#发送消息
msgsend_url='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + accesstoken



params={
        "touser": touser,
#        "toparty": toparty,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
                "content": message
        },
        "safe":0
}

req=requests.post(msgsend_url, data=json.dumps(params))

# 写日志
#  logging.info('sendto:' + touser + ';;subject:' + subject + ';;message:' + message)