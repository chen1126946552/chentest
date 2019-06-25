import datetime
import requests
import urllib
import time

def getEvent():
    # 事件请求接口
    url2 = "https://dmquery.ptengine.jp/wa/dmevent/v1_0/data?"

    # 处理日期
    today = datetime.date.today()
    print (today)

    yes = datetime.date.today() + datetime.timedelta(-1)
    print(yes)

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    body = {
        'profileId': '349127e9',
        'start-date': yes,
        'end-date': today,
        'dimensions': 'pt:hour,pt:eventName',
        'metrics': 'pt:eventCount,pt:sessions',
        'start-index': 1,
        'max-results': 10000
    }

    r2 = requests.post(url2, data=body, headers=headers)
    print(r2.status_code)
    print(r2.text)
    print(r2.elapsed.microseconds / 1000)

def getToken():
    url = "https://reportv3.ptengine.jp/token.key"
    r = requests.get(url)
    return r.json()['key']


def getDC(token):
    request_url = 'https://hquery.ptengine.jp/d'
    head = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    today = datetime.date.today()
    today_time = int(time.mktime(today.timetuple()))
    print(today_time)

    yes = datetime.date.today() + datetime.timedelta(-1)
    yes_time = int(time.mktime(yes.timetuple()))
    print(yes_time)

    body = {
        "data": {
            "dict": {
                "time": {
                    "starttime": yes_time,
                    "endtime": today_time,
                    "timezone": "+08:00"
                },
                "filter": "",
                "range": {
                    "rangetype": "site",
                    "sid": "678c8654",
                    "rangeparam": "678c8654"
                },
                "parameter": {
                    "merge": {
                        "paramlist": []
                    }
                },
                "item": {
                    "token": token,
                    "mainitem": "overview",
                    "subitem": "cvn",
                    "limit": 100
                }
            }
        }
    }

    data2 = urllib.parse.urlencode(body)
    print(type(data2))
    print(data2)
    # 不知道为什么 urlencode 之后双引号变为了单引号，所以需要字符串替换一下
    data2 = str(data2).replace("%27", "%22")
    print(data2)
    r2 = requests.post(request_url, data=data2, headers=head)
    print(r2.text)
    print(r2.elapsed.microseconds / 1000)


if __name__ == "__main__":
    # getEvent()
    # print()
    getDC(getToken())