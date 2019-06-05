import requests
import unittest

class TestWeather(unittest.TestCase):

    def setUp(self):
        self.url = 'http://47.104.190.48:8000/weather_json/'
        self.s = requests.session()

    def tearDown(self):
        self.s.close()

    def test_01(self):
        par = {
            'time':'2019-04-05',
            'city':'上海'
        }
        r = self.s.get(self.url, params=par)
        print(r.text)
