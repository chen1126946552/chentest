# -*- coding: utf-8 -*-
import datetime
import time
import os
import sys
import re
import json
import requests


# -----Slack通知范围------------------
towho = '<!here|here>'

# -----Slack发布频道设置---------------
# Slack频道=【chen_test】，个人调试频道
slackQaUrl = "https://hooks.slack.com/services/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"
# OnealertUrl对应的报警内容
OnealertUrl = "http://api.onealert.com/alert/api/event?app=680ca4a6-bfb4-9e46-cf3b-1d2de68209b4&eventType=trigger&alarmName=中国区Ptengine&eventId=21946514-9eb2-4078-813f-a8420baf0dab-7&alarmContent=测试消息,请忽略&priority=3"



# -----Slack发布消息的描述信息-------------
failmsg = '测试报告详情参考：'


# -----Slack发布范围、内容详情----------
slacktext = '{0}\n AT_DD_Online_JP_CL_Core_检查失败：\n{1}'.format(towho, failmsg)

requests.post(slackQaUrl, json={'text': slacktext})
requests.post(OnealertUrl)

