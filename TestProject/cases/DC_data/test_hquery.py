import unittest
import requests
import ddt
from common.read_excel import ExcelUtil
import os


cur = os.path.dirname(os.path.realpath(__file__))
excelPath = os.path.join(cur, "test.xlsx")
print("test.xlsx文件地址：%s"%excelPath)

data = ExcelUtil(excelPath=excelPath, sheetName="Sheet1")
dates = data.dict_data()
print(dates)

@ddt.ddt
class TestDC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()

    @classmethod
    def tearDownClass(cls):
        cls.s.close()

    def setUp(self):
        pass

    def tearDown(self):
        self.s.cookies.clear()   # 清空cookies

    @ddt.data(*dates)
    def test_hquery(self, xxx):
        '''DC接口'''
        print("测试数据：%s" % str(xxx))
        url = "https://hquery.ptengine.jp/d"

        headers = {
            "Content - Type": "application / json",
            "Referer":"https://report.ptengine.jp/login.html"
        }

        body = {
            "rememberPass": True,
            "userName": xxx["user"],
            "password": xxx["psw"]
        }
        r = requests.post(url,data=body, headers=headers)
        print(r.text)
        # 获取接口响应时间
        print(r.elapsed.microseconds/1000)
        self.assertTrue(exp_DC.test(r.text))

if __name__ == "__main__":
    unittest.main()
