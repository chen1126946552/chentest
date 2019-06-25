import requests
import unittest


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        url = "https://reportv3.ptengine.jp/token.key"
        r = requests.get(url)
        cls.token = r.json()['key']


    def test_DC(self):
        '''DC一个接口'''
        url = "https://hquery.ptengine.jp/d"
        headers = {
            "Content - Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept":"application/json, text/javascript, */*; q=0.01"
        }

        body = {"dict":{"time":{"starttime":1561305600,"endtime":1561368151,"timezone":"+08:00"},"filter":"","range":{"rangetype":"site","sid":"678c8654","rangeparam":"678c8654"},"parameter":{"merge":{"paramlist":[]}},"item":{"token": self.token,"mainitem":"overview","subitem":"cvn","limit":100}}}
        print(body)
        r = requests.post(url,data=body, headers=headers)
        print(r.text)
        # 获取接口响应时间
        print(r.elapsed.microseconds/1000)
        #self.assertTrue(exp_login.exp_DC(r.text))


if __name__ == "__main__":
    unittest.main()
