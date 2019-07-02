# -*- coding: utf-8 -*-

import requests
import unittest
import exp_login

class TestLogin(unittest.TestCase):
    '''登录'''
    def test_login(self):

        url = "https://reportv3.ptengine.jp/ptmindservice/user/login"
        userName = 'chen.chen@ptmind.com'
        password = '817c29a6a86fd8dc7f8f0f995b78358e'

        headers = {
            "Content - Type": "application / json",
            "Referer":"https://report.ptengine.jp/login.html"
        }

        body = {
            "rememberPass": True,
            "userName": userName,
            "password": password
        }
        r = requests.post(url,data=body, headers=headers)
        print(r.text)
        # 获取接口响应时间
        print(r.elapsed.microseconds/1000)
        self.assertTrue(exp_login.exp_login(r.text))

if __name__ == "__main__":
    unittest.main()
