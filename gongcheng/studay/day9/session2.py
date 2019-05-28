import requests

import re

s = requests.session()

url = "http://47.104.190.48:8000/login/"

r = s.get(url)

# re 知道前面和后面，取中间值
token = re.findall('name="csrfmiddlewaretoken" value="(.+?)"',r.text)
print(token[0])

body = {
    "csrfmiddlewaretoken":token[0],
    "username":"test111",
    "password":"123456"
}

r2 = s.post(url, data = body)

print(dict(s.cookies))

# 断言
assert '登录成功' in r2.text

# 登录之后
url3 = "http://47.104.190.48:8000/change"

r3 = s.get(url3)
print(r3.text)