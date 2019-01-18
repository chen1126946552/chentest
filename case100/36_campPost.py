# -*- coding: UTF-8 -*-
# 从widgetID_List.csv文件中获取widget列表，将widget返回的数据摘取，并存入文件中

import requests
import json

host = 'http://192.168.2.15:7090'
userEmail = 'datatest35@163.com'
userPassword = 'e10adc3949ba59abbe56e057f20f883e'
uid = '3413'
filename = 'ParamVaule_v2.csv'
filenameWidget = 'widgetID_List.csv'

header = {'accept': 'application/json, text/plain, */*',
          'accept-encoding': 'gzip, deflate, br',
          'accept-language': 'en_US',
          'content-type': 'application/json;charset=UTF-8',
          'Timezone': 'Asia/Shanghai',
          'User-Agent': 'Apache-HttpClient/4.5.6 (Java/1.8.0_181)',
          'UID': uid}


# 发送登录请求，获取sid
def getsid(host, userEmail, userPassword, header):
    url = host + "/api/v2/users/signin?community=false"
    para = {"userEmail": userEmail, "userPassword": userPassword, "rememberMe": True}

    r = requests.post(url, data=json.dumps(para), headers=header)

    # 响应的json数据转换为可被python识别的数据类型
    json_r = r.json()
    # 获取sid
    return json_r['data']['sid']


# 从文件中获取widgetid的list
def getwidget(filenameWidget):
    with open(filenameWidget, "rt") as in_file:
        text = in_file.read()
    return text.split('\n')


# 获取widget的Setting数据
def getdata(host, header, widgetid):
    url2 = host + "/api/v1/widgets/" + widgetid
    para2 = {}

    r2 = requests.get(url2, params=para2, headers=header)
    # 响应的json数据转换为可被python识别的数据类型
    return r2.json()


# 获取widget数据接口
def getpost(host, uid, sid, json_r2):
    url3 = host + "/api/v1/widgets/data/preview?isEtl=false"
    para3 = json_r2['data']
    header = {'accept': 'application/json, text/plain, */*',
              'accept-encoding': 'gzip, deflate, br',
              'accept-language': 'en_US',
              'content-type': 'application/json;charset=UTF-8',
              'Timezone': 'Asia/Shanghai',
              'User-Agent': 'Apache-HttpClient/4.5.6 (Java/1.8.0_181)',
              'UID': uid,
              'Token': sid}

    r3 = requests.post(url3, data=json.dumps(para3), headers=header)
    return r3.json()


# 将获取的值，写入文件中
def writefile(json_r3, filename):
    list1 = []
    widgetid = json_r3['data']['widgetId']
    # 将获取到的值，添加到list中
    list1.append(widgetid)

    dataList = json_r3['data']['data']
    metricsNamelist = []
    for i in dataList:
        metricsNamelist.append(i['metricsName'])

    list1.append(metricsNamelist)

    # 将list,用###分隔写入文件中
    with open(filename, "a+") as out_file:
        out_file.write('\n')
        for i in list1:
            out_file.write(str(i))
            out_file.write('###')


if __name__ == '__main__':
    sid = getsid(host, userEmail, userPassword, header)
    widgetlist = getwidget(filenameWidget)
    for i in widgetlist:
        print(i)
        json_r2 = getdata(host, header, i)
        json_r3 = getpost(host, uid, sid, json_r2)
        writefile(json_r3, filename)
