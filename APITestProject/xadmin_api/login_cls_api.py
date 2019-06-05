import requests
import re

# self 自己 本身  this

class TestXadmin():
    def __init__(self, s):
        # 构建函数
        self.s = s

    def login(self, user, psw):
        # 1.准备死数据
        url = "http://47.104.190.48:8000/login/"
        # s = requests.session()
        # 2.获取需要的动态数据
        r = self.s.get(url)
        # re 知道前面和后面，取中间值
        token = re.findall('name="csrfmiddlewaretoken" value="(.+?)"', r.text)
        print(token[0])

        # 3.发请求的body
        body = {
            "csrfmiddlewaretoken": token[0],
            "username": user,
            "password": psw
        }

        # 4.发请求
        r2 = self.s.post(url, data=body)
        return r2.text  # 返回的html页面

    def is_login_sucess(self, t):
        if "登录成功" in t:
            print("log日志-----登录成功！-------")
            return True
        else:
            print("log日志-----登录失败，检查账号密码！---")
            return False

if __name__ == '__main__':
    s = requests.session()
    x = TestXadmin(s)   # 实例化
    t = x.login(user="test", psw="test")
    res = x.is_login_sucess(t)
    print(res)




