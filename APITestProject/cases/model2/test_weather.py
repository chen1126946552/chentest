import requests
import unittest

class TestWeather(unittest.TestCase):
    '''天气接口'''
    def test_01(self):
        '''成功案例：time=2019-04-05, city=上海'''
        url = "http://47.104.190.48:8000/weather_json/"
        par = {
            "time": "2019-04-05",
            "city": "上海"
        }
        r = requests.get(url, params=par)
        print(r.text)    # 确认是不是json
        reason = r.json()['reason']
        print(reason)   # 实际结果
        exp = "success"  # 期望结果
        # assert reason==exp
        self.assertTrue(reason==exp)  # 断言

    def test_02(self):
        '''失败案例：time=2019-04-, city=上海'''
        url = "http://47.104.190.48:8000/weather_json/"
        par = {
            "time": "2019-04-",
            "city": "上海"
        }
        r = requests.get(url, params=par)
        print(r.text)    # 确认是不是json
        reason = r.json()['reason']
        print(reason)   # 实际结果
        exp = "时间格式不对"  # 期望结果
        self.assertTrue(exp in reason)

if __name__ == '__main__':
    unittest.main()


