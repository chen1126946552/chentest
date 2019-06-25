import unittest
import requests
import ddt
from common.read_excel import ExcelUtil
import os
import datetime

cur = os.path.dirname(os.path.realpath(__file__))
excelPath = os.path.join(cur, "event.xlsx")
print("event.xlsx文件地址：%s"%excelPath)

data = ExcelUtil(excelPath=excelPath, sheetName="Sheet1")
dates = data.dict_data()
print(dates)


@ddt.ddt
class TestLogin(unittest.TestCase):

    @ddt.data(*dates)
    def test_login_01(self, xxx):
        '''事件请求接口  xxx["name"]'''
        url2 = "https://dmquery.ptengine.jp/wa/dmevent/v1_0/data?"

        # 处理日期
        today = datetime.date.today()
        print(today)

        yes = datetime.date.today() + datetime.timedelta(-1)
        print(yes)

        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }

        body = {
            'profileId': '349127e9',
            'start-date': yes,
            'end-date': today,
            'dimensions': xxx["dimensions"],
            'metrics': xxx["metrics"],
            'segment': xxx["segment"],
            'filters': xxx['filters'],
            'start-index': 1,
            'max-results': 10000
        }
        print(body)
        r2 = requests.post(url2, data=body, headers=headers)
        print(r2.status_code)
        print(r2.text)
        print(r2.elapsed.microseconds / 1000)

if __name__ == '__main__':
    unittest.main()