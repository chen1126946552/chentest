# -*- coding: UTF-8 -*-
# 读取json文件，并摘取响应内容

import json

filename = "json.csv"

# 从文件中获取
def getwidget(filename):
    with open(filename, "rt") as in_file:
        text = in_file.read()
    return text

# 提取值
def writefile(json_r):
    a = json.loads(json_r)
    b = a['data']['items']
    for i in b:
        print(i['value'],end=',')

if __name__ == '__main__':
    text = getwidget(filename)
    writefile(text)