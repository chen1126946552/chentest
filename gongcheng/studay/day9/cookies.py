
import requests

import re

url = "http://47.104.190.48:8000/login/"

r = requests.get(url)

print(r.cookies) # 返回cookies

print(r.text)

# re 知道前面和后面，取中间值
token = re.findall('name="csrfmiddlewaretoken" value="(.+?)"',r.text)
print(token[0])

body = {
    "csrfmiddlewaretoken":token[0],
    "username":"test111",
    "password":"123456"
}

r2 = requests.post(url, data = body, cookies = r.cookies)
print(r2.text)

# 断言
assert '登录成功' in r2.text