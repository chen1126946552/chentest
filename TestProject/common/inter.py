import datetime
import requests
import urllib
import time

def getEvent(profileId, startdate, enddate, dimensions, meterics, segment=None, filters=None):
    # 事件请求接口
    url2 = "https://dmquery.ptengine.jp/wa/dmevent/v1_0/data?"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    body = {
        'profileId': profileId,
        'start-date': startdate,
        'end-date': enddate,
        'dimensions': dimensions,
        'metrics': meterics,
        'segment': segment,
        'filters': filters,
        'start-index': 1,
        'max-results': 10000
    }
    r = requests.post(url2, data=body, headers=headers)
    return r.status_code, r.text, r.elapsed.microseconds / 1000

# 提取event接口返回的totalResults的值
def getEventTotal(text):
    d = eval(text)
    return d['totalResults']

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

def returnabs(a,b):
    if b == 0:
        return 0
    else:
        return abs(a-b)/b


if __name__ == "__main__":
    # getEvent()
    # print()
    # getDC(getToken())
    today = datetime.date.today()
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    s = getEvent('349127e9', yesterday, today, 'pt:hour,pt:eventName', 'pt:eventCount,pt:sessions')
    print(s[0])
    print(s[1])
    print(s[2])
    print(type(s))
    d = eval(s[1])
    print(d)
    d2 = d['totalResults']
    print(d2)
