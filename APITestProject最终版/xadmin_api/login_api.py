import requests
import re
from requests_toolbelt import MultipartEncoder
from lxml import etree
import pymysql

url = "http://47.104.190.48:8000/login/"

s = requests.session()

def login(s, user="test", psw="test"):
    '''登录'''
    r = s.get(url)
    # re 知道前面和后面，取中间值
    waretoken = ""
    try:
        token = re.findall('name="csrfmiddlewaretokenxx" value="(.+?)"', r.text)
        print("获取到登录页面token:%s" % token[0])
        waretoken = token[0]
    except:
        print("获取页面token失败")
        waretoken = ""

    body = {
        "csrfmiddlewaretoken": waretoken,
        "username": user,
        "password": psw
    }
    r2 = s.post(url, data=body)
    if "登录成功" in r2.text:
        print("登录成功！")
    else:
        print("登录失败，检查账号密码！")
    return r2.text

def is_login_sucess(t):
    result = False       # 立 flag
    if "登录成功" in t:
        result = True
    return result

if __name__ == "__main__":
    r = login(s)
    res = is_login_sucess(r)
    print(res)
