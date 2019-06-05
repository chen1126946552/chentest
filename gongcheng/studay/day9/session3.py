import requests


s = requests.session()

# 添加cookies

cooks = {
    "csrftoken" : "efz6HsoEb3aeV4Dg8bhAeGyKm0jM98Q7AIBvOEvjKiVBiiUaCTMQuGHLPlWpzBKT",
    "sessionid" : "b6odhwwxazo994qmc9wmxmscogo9v1wk"
}

# 工具不匹配，自己写
c = requests.cookies.RequestsCookieJar()
c.set("csrftoken", cooks["csrftoken"])
c.set("sessionid", cooks["sessionid"])

s.cookies.update(c)

print(s.cookies)

url = 'http://47.104.190.48:8000/login_test/'

r = s.get(url)

print(r.text)