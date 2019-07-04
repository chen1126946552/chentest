# -*- coding: utf-8 -*-

import unittest
import ddt
import datetime
import config.config
import os
from common.excuet_sql import engage_sid_sql
from common.excuet_sql import engage_data_sql
from common.inter import getEvent
import time

dates = engage_sid_sql()
print(dates)

filename = "engage.csv"

@ddt.ddt
class TestEngage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 处理日期
        cls.today = datetime.date.today()
        cls.fo = open(filename, "a+")
        cls.engageviews = 0

    @classmethod
    def tearDownClass(cls):
        cls.fo.close()
        engage_data_sql(filename, 'pt_engage')
        if (os.path.exists(filename)):
            os.remove(filename)

    @ddt.data(*dates)
    def test_engage(self, data):
        '''engage请求接口'''
        print(data['sid'])

        s = getEvent(config.config.EVENT_RUL, data['sid'], self.today, self.today, 'hit::pt:engageId,hit::pt:engageName', 'pt:engageView,pt:engageCTR,pt:engageCloseRate,pt:perExit,pt:conversions,pt:conversionRate')
        print(s[0]) # 返回status code
        print(s[1]) # 返回内容
        print(s[2]) # 响应时间s
        d = eval(s[1])
        rows = d['rows']
        if len(rows) == 0:
            self.fo.write("{0},0,'',0,0,0,0,0,0#".format(data['sid']))
        else:
            for i in rows:
                self.fo.write("{0},{1},{2},{3},{4},{5},{6},{7},{8}#".format(data['sid'], i[0], i[1].replace("'", ""), i[2], i[3], i[4], i[5], i[6], i[7]))


if __name__ == '__main__':
    unittest.main()