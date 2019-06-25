
from common import sendMessage

message = '检查失败'
# Slack频道=【chen_test】，个人调试频道
slackQaUrl = "https://hooks.slack.com/services/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"

sendMessage.sendSlack(slackQaUrl,message)

# 多个接收者用‘|’分隔
touser = 'ChenChen'

sendMessage.sendWeixin(touser,message)