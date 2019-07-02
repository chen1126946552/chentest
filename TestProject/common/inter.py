# -*- coding: utf-8 -*-

import requests
import urllib

def getEvent(request_url, profileId, startdate, enddate, dimensions, meterics, segment=None, filters=None):

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
    r = requests.post(request_url, data=body, headers=headers)
    print(body)
    return r.status_code, r.text, r.elapsed.microseconds / 1000

# 提取event接口返回的totalResults的值
def getEventTotal(text):
    d = eval(text)
    return d['totalResults']

def getToken(url):
    r = requests.get(url)
    return r.json()['key']


def getDC(request_url, name, profileId, startdate, enddate, token, mainitem, subitem):
    head = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    body = {
        "data": {
            name: {
                "time": {
                    "starttime": startdate,
                    "endtime": enddate,
                    "timezone": "+08:00"
                },
                "filter": "",
                "range": {
                    "rangetype": "site",
                    "sid": profileId,
                    "rangeparam": profileId
                },
                "parameter": {
                    "merge": {
                        "paramlist": []
                    }
                },
                "item": {
                    "token": token,
                    "mainitem": mainitem,
                    "subitem": subitem,
                    "limit": 100,
                    "sort": 2
                },
                "conversion_target": "all",
                "conversion_target_name": "All conversions",
                "search": {
                    "value": "",
                    "field": 1,
                    "state": 0
                }
            }
        }
    }

    data2 = urllib.parse.urlencode(body)
    # 不知道为什么 urlencode 之后双引号变为了单引号，所以需要字符串替换一下
    data2 = str(data2).replace("%27", "%22")
    print(data2)
    r = requests.post(request_url, data=data2, headers=head)
    print(r.text)
    print(r.elapsed.microseconds / 1000)
    return r.status_code, r.text, r.elapsed.microseconds / 1000

def returnabs(a,b):
    if b == 0:
        return 0
    else:
        return abs(a-b)/b


#if __name__ == "__main__":
   # getEvent()
   # print()
   # getDC(getToken())
   # today = datetime.date.today()
   # yesterday = datetime.date.today() + datetime.timedelta(-1)
   # s = getEvent('349127e9', yesterday, today, 'pt:hour,pt:eventName', 'pt:eventCount,pt:sessions')
   # s = getEvent('349127e9', today, today, 'hit::pt:engageId,hit::pt:engageName', 'pt:engageView')
   # print(s)
