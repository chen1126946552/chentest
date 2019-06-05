# -*- coding: UTF-8 -*-
# 正则表达式

import re

test = '用户输入的字符串'
if re.match(r'正则表达式',test):
    print('ok')
else:
    print('failed')

# Read a file
with open("json.csv", "rt") as in_file:
    text = in_file.read()

print(text)
widgetId = re.findall(r'\"widgetId\":\".*?\"', text)
print(widgetId)

panelId = re.findall(r'\"panelId\":\".*?\"', text)
print(panelId)

categories = re.findall(r'\"categories\":\[.*?\]', text)
print(categories)

metricsNameList = re.findall(r'\"metricsName\":\".*?\"', text)
print(metricsNameList)

dimensionsList = re.findall(r'\"dimensions\":\".*?\"', text)
print(dimensionsList)

dateRangeList = re.findall(r'\"dateRange\":\[.*?\]', text)
print(dateRangeList)

rowsList = re.findall(r'\"rows\":\[.*?\]', text)
print(rowsList)

metricsTotalsMapValue = re.findall(r'\"metricsTotalsMap\":\{\"value\":.*?(?=,)\}\"', text)
print(metricsTotalsMapValue)
