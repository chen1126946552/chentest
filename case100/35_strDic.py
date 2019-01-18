# -*- coding: UTF-8 -*-

import json

with open("json1.csv", "rt") as in_file:
	text1 = in_file.read()

# 将字符串转成字典
user_dict = json.loads(text1)

widgetid = user_dict['data']['widgetId']
print(widgetid)

dataList = user_dict['data']['data']

for i in dataList:
	print(i['metricsName'])