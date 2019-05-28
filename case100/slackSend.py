# -*- coding: utf-8 -*-

import requests



#-----Slack通知范围------------------
towho = '<!here|here>'
#towho = 'here'

#-----Slack发布频道设置---------------
# Slack频道=【chen_test】，个人调试频道
# 可以从URL中获取https://api.slack.com/apps/ABR6DVA85/install-on-team
slackQaUrl = "https://hooks.slack.com/services/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"
# Slack频道=【datadeck_develop】，Datadeck开发群
# slackQaUrl = "https://hooks.slack.com/services/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"
# Slack频道=【dd_autotest_online】，线上环境长期观测的自动化项目群
#slackQaUrl = "https://hooks.slack.com/services/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"
# Slack频道=【dd_autotest_offline】，Staging环境长期观测的自动化项目群
#slackQaUrl = "https://hooks.slack.com/services/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"


#-----Slack发布范围、内容详情----------
slacktext =  '{0}\n检查失败：\n'.format(towho)


requests.post(slackQaUrl, json = {'text': slacktext})
print ("send message success")
