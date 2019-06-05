# -*- coding: UTF-8 -*-
# 从widgetID_List.csv文件中获取widget列表，将widget返回的数据摘取，并存入文件中

import requests
import json
import logging

host = 'https://middlev2.datadeck.com/api/slack/v1/widgets/'
filenameWidget = 'widgetID_List1.csv'
path = './middlev2/'


# 从文件中获取widgetid的list
def getwidget(filenameWidget):
    with open(filenameWidget, "rt") as in_file:
        text = in_file.read()
    return text.strip().split('\n') # 去掉字符串前后空格换行，并按照换行符区分返回list


# 获取widget的数据
def getdata(host, uid, widgetid):

    header = {'token': 'bm90aWZpY2F0aW9uX3N1cGVyX3Rva2Vu',
              'UserID': uid}
    url2 = host + widgetid
    para2 = {}
    r2 = requests.get(url2, params=para2, headers=header)
    # 响应的json数据转换为可被python识别的数据类型
    return r2.json()

# 将获取的值，写入文件中
def writefile(json_r):
    list1 = []

    widgetid = json_r['data']['data']['widgetId']
    filename = widgetid +'.csv'

    dataList = json_r['data']['data']['data']

    # 将获取的值，添加到list
    for i in dataList:
        #list1.append(i['rows'])
        for j in i['rows']:
            list2 = []
            for k in j:
                if(type(k) == float):
                    list2.append(int(k))
                else:
                    list2.append(k)
            list1.append(list2)

    # 将list,写入文件中
    fl = open(path + filename, "w+")
    for i in list1:
        fl.write(str(i))
        fl.write('\n')
    fl.close()


if __name__ == '__main__':
    widgetlist = getwidget(filenameWidget)
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    for i in widgetlist:
        logging.info('start')
        widgetUidList = i.split(',')
        logging.info('getdata start')
        json_r = getdata(host, widgetUidList[1], widgetUidList[0])
        logging.info('getdata end')
        logging.info('write start')
        writefile(json_r)
        logging.info('end')
