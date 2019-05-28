import json
import requests

a = '{"aa":111, "b":True}'  # str
b = '{"aa":111, "b":true}'  # str json

c = json.loads(b)
print(c)

# a怎么转字段 eval: 把字符串当成代码去识别

d = eval(a)
print(d)
print(type(d))

url = "http://httpbin.org/post"

body = {
    "uo": "hello world",
    "xx": "aaaa"
}

r = requests.post(url, json = body)
print(r.text)

# 第二种发送方式
r2 = requests.post(url, data=json.dumps(body))
print(r2.text)
