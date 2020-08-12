# -*- coding: utf-8 -*-

import requests
import json

def send_weixin(touser,message):
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

def send_teams(message,report_url):
    headers = {
        "Content-Type": "application/json;"
    }
    # ptx_alter群
    url = "https://outlook.office.com/webhook/367a0699-7953-4b43-8719-0ea03c166e03@b509a3c5-f909-4062-983b-bf02a7aee6a3/IncomingWebhook/2a9e4d9b95604253ba55dd9c658586f7/b6613acf-d3fd-4807-80ec-2450c3e5fd7f"
    body = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": "This is the summary property",
        "themeColor": "0075FF",
        "sections": [{
            "startGroup": True,
            "title": "**PtengineX Alert**",
            "facts": [{
                "name": "Details:",
                "value": message + report_url},
                {
                    "name": "Link:",
                    "value": [report_url](report_url)
                }]}]}
    r = requests.post(url, data=json.dumps(body), headers=headers);
    print(r.text)