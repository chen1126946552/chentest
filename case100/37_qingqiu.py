# -*- coding: UTF-8 -*-

# 登录请求，获取widget数据接口

import requests
import json

sid = ''
url = "http://192.168.2.15:7090/api/v2/users/signin?community=false"
para = {"userEmail":"datatest35@163.com","userPassword":"e10adc3949ba59abbe56e057f20f883e","rememberMe":True}
header ={'accept': 'application/json, text/plain, */*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en_US',
'content-type': 'application/json;charset=UTF-8',
'Timezone':'Asia/Shanghai',
'User-Agent': 'Apache-HttpClient/4.5.6 (Java/1.8.0_181)',
'UID':'3413',
'Token':sid}

r = requests.post(url,data=json.dumps(para),headers=header)

print('post请求获取的响应结果json类型',r.text)
print("post请求获取响应状态码",r.status_code)
print("post请求获取响应头",r.headers)

# 响应的json数据转换为可被python识别的数据类型
json_r = r.json()
print(json_r)

sid = json_r['data']['sid']
print(sid)

print('登录成功，获取sid')

widgetid = '569c59d9-2712-42da-9909-a995897b792d'
url2 = "http://192.168.2.15:7090/api/v1/widgets/"+ widgetid
para2 = {}
header2 ={'accept': 'application/json, text/plain, */*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en_US',
'content-type': 'application/json;charset=UTF-8',
'Timezone':'Asia/Shanghai',
'User-Agent': 'Apache-HttpClient/4.5.6 (Java/1.8.0_181)',
'UID':'3413',
'Token':sid}

getr = requests.get(url2,params=para2,headers= header2)

print('get请求获取的响应结果json类型',getr.text)
print("get请求获取响应状态码",getr.status_code)

# 响应的json数据转换为可被python识别的数据类型
json_r2 = getr.json()

print('发送取数请求....')

url3 = "http://192.168.2.15:7090/api/v1/widgets/data/preview?isEtl=false"
para3 = json_r2['data']
postr = requests.post(url3,data=json.dumps(para3),headers=header2)
print('post请求获取的响应结果json类型',postr.text)
print("post请求获取响应状态码",postr.status_code)
