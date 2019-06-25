import unittest
import ddt
from common.read_excel import ExcelUtil
import os
import datetime
from common.inter import getEvent
from common.inter import getEventTotal
from common.inter import returnabs

cur = os.path.dirname(os.path.realpath(__file__))
excelPath = os.path.join(cur, "event.xlsx")
print("event.xlsx文件地址：%s"%excelPath)

data = ExcelUtil(excelPath=excelPath, sheetName="Sheet1")
dates = data.dict_data()
print(dates)


@ddt.ddt
class TestEvent(unittest.TestCase):

    @ddt.data(*dates)
    def test_event(self, data):
        '''事件请求接口'''
        print(data["name"])

        # 处理日期
        today = datetime.date.today()
        yesterday = datetime.date.today() + datetime.timedelta(-1)
        today_7 = datetime.date.today() + datetime.timedelta(-7)
        yesterday_7 = datetime.date.today() + datetime.timedelta(-1)

        s = getEvent('349127e9', yesterday, today, data["dimensions"], data["metrics"], data["segment"], data['filters'])
        print(s[0]) # 返回status code
        print(s[1]) # 返回内容
        print(s[2]) # 响应时间s
        exp1 = 'totalResults'

        self.assertIn(exp1,s[1])

        s2 = getEvent('349127e9', yesterday_7, today_7, data["dimensions"], data["metrics"], data["segment"],
                     data['filters'])

        self.assertLess(returnabs(getEventTotal(s[1]),getEventTotal(s2[1])),0.5)



if __name__ == '__main__':
    unittest.main()