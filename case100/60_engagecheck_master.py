# -*- coding: utf-8 -*-
import pymysql
import datetime
import requests
import time


# 查询当前设置engage的sid
def engage_sid_sql():
    # 打开数据库连接
    db = pymysql.connect(host='172.19.3.14',
                         port=3308,
                         user='Ptreadonly',
                         passwd='PtMind123qwe',
                         db='ptmind_common')

    # 使用 cursor() 方法创建一个游标对象cur
    cur = db.cursor()

    sql = 'select DISTINCT pt_engage_base.sid from pt_engage_base INNER JOIN ref_site_status ON ref_site_status.sid = pt_engage_base.sid WHERE pt_engage_base.`status`=1 and pt_engage_base.deleted=0 and ref_site_status.`status`=1;'
    # 使用 execute()  方法执行 SQL 查询
    cur.execute(sql)
    r = []
    for i in cur.fetchall():
        s = {'sid':i[0]}
        r.append(s)

    # 一定要提交
    db.commit()
    db.close()
    return r

# 查询engage曝光次数
def getdata(profileId, startdate, enddate, dimensions, meterics,):
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
        'start-index': 1,
        'max-results': 10000
    }
    r = requests.post(url2, data=body, headers=headers)
    print(body)
    return r.status_code, r.text, r.elapsed.microseconds / 1000

def getrows(text):
    d = eval(text)
    print(type(d['totalResults']))
    print(d['totalResults'])
    print(type(d['rows']))
    print(d['rows'])



# 查询engage数据插入数据库
def engage_data_sql(sql):
    # 打开数据库连接
    db = pymysql.connect(host='139.220.242.36',
                         port=23306,
                         user='qa_auto',
                         passwd='qa_auto',
                         db='qa_auto_ptengine',
                         charset='utf8')
    # 使用 cursor() 方法创建一个游标对象cur

    cur = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cur.execute(sql)

    # 一定要提交
    db.commit()
    db.close()

if __name__ == "__main__":
    sidlist = engage_sid_sql()
    today = datetime.date.today()
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    engageView = 0
    print(today)
    for i in sidlist:
        s = getdata(i['sid'],today, today, 'hit::pt:engageId,hit::pt:engageName', 'pt:engageView,pt:engageCTR,pt:engageCloseRate,pt:perExit,pt:conversions,pt:conversionRate')
        d = eval(s[1])
        rows = d['rows']
        if len(rows) == 0:
            sql = "insert into pt_engage(sid,engageID,engageName,engageView,engageCTR,engageCloseRate,perExit,conversions,conversionRate,date) values('{0}',0,'',0,0,0,0,0,0,'{1}')".format(
                i['sid'], int(time.time()))
            print(sql)
            engage_data_sql(sql)
        else:
            for j in rows:
                print(j)
                sql = "insert into pt_engage(sid,engageID,engageName,engageView,engageCTR,engageCloseRate,perExit,conversions,conversionRate,date) values('{0}',{1},'{2}',{3},{4},{5},{6},{7},{8},{9})" .format(i['sid'],j[0],j[1].replace("'", ""),j[2],j[3],j[4],j[5],j[6],j[7], int(time.time()))
                engageView += j[2]
                print(sql)
                engage_data_sql(sql)

    print(engageView)
    slackQaUrl = "https://hooks.slack.com/services/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"
    slackText = 'today engageView Count is {0}' .format(engageView)
    if engageView < 100:
        requests.post(slackQaUrl, json={'text': slackText})

