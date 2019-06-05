import requests
import re

s = requests.Session()  # 代码里面的浏览器

print(s.headers)
print(s.cookies)


url = "http://47.104.190.48:8000/register/"
r1 = s.get(url)

print(s.cookies)


token = re.findall('name="csrfmiddlewaretoken" value="(.+?)"',r1.text)
print(token[0])

body = {
    "csrfmiddlewaretoken":token[0],
    "username":"t12",
    "password":"123456",
    "email":"111",
}


r2 = s.post(url, data=body)
print(r2.text)