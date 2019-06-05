import requests

url =  "http://47.104.190.48:8000/change/"

r = requests.get(url)

print(r.status_code) #最后一次URL的状态码
print(r.headers)
print(r.url)

all = r.history # 获取所有重定向的地址 list Response对象

for i in all:
    print(i)  # Response 对象

print (all[0].status_code)
print (all[0].headers)
print (all[0].url)

