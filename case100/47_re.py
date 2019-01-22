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

m = re.match(r'\"metricsName\":\".*?\"', text)
print(m)