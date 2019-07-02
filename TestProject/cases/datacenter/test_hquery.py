# -*- coding: utf-8 -*-

import unittest
import ddt
from common.read_excel import ExcelUtil
import os
from common.inter import getToken
from common.inter import getDC
import datetime
import time
import config.config


cur = os.path.dirname(os.path.realpath(__file__))
excelPath = os.path.join(cur, "datacenter.xlsx")
print("datacenter.xlsx文件地址：%s"%excelPath)

data = ExcelUtil(excelPath=excelPath, sheetName="Sheet1")
dates = data.dict_data()
print(dates)

@ddt.ddt
class TestDC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.token = getToken(config.config.TOKEN_URL)
        # 处理日期
        today = datetime.date.today()
        cls.today_time = int(time.mktime(today.timetuple()))

        today_7 = datetime.date.today() + datetime.timedelta(-7)
        cls.today_7_time = int(time.mktime(today_7.timetuple()))

    @ddt.data(*dates)
    def test_hquery(self, data):
        '''DC接口'''
        print(data['name'])
        print("测试数据：%s" % str(data))
        s = getDC(config.config.DC_URL, data['name'], config.config.SID, self.today_7_time, self.today_time, self.token, data['mainitem'], data['subitem'])

        exp = 'timestamp'
        self.assertIn(exp, s[1])


if __name__ == "__main__":
    unittest.main()
