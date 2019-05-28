import unittest
import requests
from xadmin_api.login_cls_api import TestXadmin
import ddt
from common.read_excel import ExcelUtil
import os

cur = os.path.dirname(os.path.realpath(__file__))
excelPath = os.path.join(cur, "test.xlsx")
print("test.xlsx文件地址：%s"%excelPath)

data = ExcelUtil(excelPath=excelPath, sheetName="Sheet1")
dates = data.dict_data()
print(dates)


# dates = [
#     {"user": "test", "psw": "test", "exp": True},
#     {"user": "test111", "psw": "11", "exp": False},
#     {"user": "test222", "psw": "22", "exp": False},
#     {"user": "test", "psw": "test", "exp": True},
# ]

@ddt.ddt
class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        cls.x = TestXadmin(cls.s)

    @classmethod
    def tearDownClass(cls):
        cls.s.close()

    def setUp(self):
        pass
        # self.s = requests.session()
        # self.x = TestXadmin(self.s)

    def tearDown(self):
        self.s.cookies.clear()   # 清空cookies
    #     # self.s.close()

    @ddt.data(*dates)
    def test_login_01(self, xxx):
        '''登录数据： test test '''
        print("测试数据：%s" % str(xxx))
        user = xxx["user"]
        psw = xxx["psw"]
        exp = bool(xxx["exp"])           # 0 1
        print("期望结果：%s"%exp)
        t = self.x.login(user, psw )      # 登录
        res = self.x.is_login_sucess(t)   # 获取实际结果
        print("实际结果：%s"%res)
        self.assertEqual(res, exp)

if __name__ == '__main__':
    unittest.main()