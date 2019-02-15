# -*- coding: UTF-8 -*-
# 假设你获取了用户输入的日期和时间如2015-1-21 9:01:30，
# 以及一个时区信息如UTC+5:00，均是str

from datetime import datetime, timezone, timedelta


def to_timestamp(dt_str, tz_str):
    datetimeformatstr1 = '%Y-%m-%d %H:%M:%S'
    _timezone = timezone(timedelta(hours=get_timedelta(tz_str)))
    time = datetime.strptime(dt_str, datetimeformatstr1).replace(tzinfo=_timezone)
    return time.timestamp()


def get_timedelta(tz_str):
    import re
    timedelta1 = int(re.split(r'UTC|:', tz_str)[1])
    print(timedelta1)
    return timedelta1


t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
print(t1)

t2 = to_timestamp('2015-6-1 08:10:30', 'UTC-9:00')
print(t2)
