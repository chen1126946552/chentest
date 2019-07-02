# -*- coding: utf-8 -*-

import unittest
import ddt
from common.excuet_sql import engage_sid_sql
import datetime
from common.inter import getEvent

dates = engage_sid_sql()
print(dates)


@ddt.ddt
class TestEngage(unittest.TestCase):

    @ddt.data(*dates)
    def test_engage(self, data):
        '''engage请求接口'''

        # 处理日期
        today = datetime.date.today()
        print(data['sid'])

        s = getEvent(config.config.SID, today, today, 'hit::pt:engageId,hit::pt:engageName', 'pt:engageView')
        print(s[0]) # 返回status code
        print(s[1]) # 返回内容
        print(s[2]) # 响应时间s



if __name__ == '__main__':
    unittest.main()