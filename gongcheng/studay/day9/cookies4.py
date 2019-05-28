
import requests

import re

url = "http://47.104.190.48:8000/register/"

r = requests.get(url)

print(r.cookies) # 返回cookies

print(r.text)

# re 知道前面和后面，取中间值
token = re.findall('name="csrfmiddlewaretoken" value="(.+?)"',r.text)
print(token[0])

body = {
    "csrfmiddlewaretoken":token[0],
    "username":"t12",
    "password":"123456",
    "email":"111",
}

# 注册之前，先删除

r2 = requests.post(url, data=body, cookies=cookies)
print(r2.text)