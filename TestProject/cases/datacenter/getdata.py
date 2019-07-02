# -*-conding:utf-8-*-
# 用例处理DC各个接口获取数据之后的处理

import json
import jsonpath
from common.inter import getToken
from common.inter import getDC
import datetime
import time

def dc_obase(d):
    vi = jsonpath.jsonpath(d, '$..vi')
    pv = jsonpath.jsonpath(d, '$..pv')
    nv = jsonpath.jsonpath(d, '$..nv')
    st = jsonpath.jsonpath(d, '$..st')
    lt = jsonpath.jsonpath(d, '$..lt')
    br = jsonpath.jsonpath(d, '$..br')
    en = jsonpath.jsonpath(d, '$..en')
    print(vi, pv, nv, st, lt, br, en)

def dc_obaseuv(d):
    uv = jsonpath.jsonpath(d, '$..uv')
    print(uv)

def dc_oplatform(d):
    vi = jsonpath.jsonpath(d, '$..vi')
    pc = jsonpath.jsonpath(d, '$..pc')
    smartphone = jsonpath.jsonpath(d, '$..smartphone')
    tablet = jsonpath.jsonpath(d, '$..tablet')
    other = jsonpath.jsonpath(d, '$..other')
    print(vi, pc, smartphone, tablet, other)


if __name__ == "__main__":
    # 处理日期
    today = datetime.date.today()
    today_time = int(time.mktime(today.timetuple()))

    today_7 = datetime.date.today() + datetime.timedelta(-7)
    today_7_time = int(time.mktime(today_7.timetuple()))
    token = getToken()
    # a = getDC('dc_obase', "2b1ab5d0", today_7_time, today_time, token, 'overview', 'overview')
    # d = json.loads(a)
    # dc_obase(d)
    # print('---------------')
    # a = getDC('dc_obaseuv', "2b1ab5d0", today_7_time, today_time, token, 'overview', 'overview')
    # d = json.loads(a)
    # dc_obaseuv(d)
    # print('---------------')
    a = getDC('dc_oplatform', "2b1ab5d0", today_7_time, today_time, token, 'overview', 'overview')
    d = json.loads(a)
    dc_oplatform(d)
    print('---------------')

