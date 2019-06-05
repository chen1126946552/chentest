import requests

url =  "http://47.104.190.48:8000/change/"

# 不允许重定向
r = requests.get(url, allow_redirects=False)

print(r.status_code)