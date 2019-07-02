# -*- coding: utf-8 -*-

import requests
import json

def sendSlack(slackQaUrl,message):

    towho = '<!here|here>'
    slacktext =  '{0}\n{1}\n'.format(towho,message)
    requests.post(slackQaUrl, json = {'text': slacktext})
    print ("send message success")

def sendWeixin(touser,message):
    corpid = 'ww706438937701feec'
    appsecret = 'LN4kjDjuFCNgullXlHhEEjaVsXvlLhdoUf-1DGNIwZc'
    agentid = 1000005

    # 获取accesstoken
    token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + appsecret
    req = requests.get(token_url)
    accesstoken = req.json()['access_token']

    # 发送消息地址
    msgsend_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + accesstoken

    # 部门列表参数toparty 标签ID totag
    params = {
        "touser": touser,
        # "toparty": toparty,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": message
        },
        "safe": 0
    }
    requests.post(msgsend_url, data=json.dumps(params))