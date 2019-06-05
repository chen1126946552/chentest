# -*- coding: UTF-8 -*-
# datetime是python处理日期和时间的标准库
# timedelta用户对日期时间的加减
# timezone时区设置

from datetime import datetime, timedelta, timezone

print('获取当前datetime')
now = datetime.now()
print(now)

print('用指定的日期时间创建datetime')
dt = datetime(2015, 4, 19, 12, 20)
print(dt)

print('把datetime转换成timestamp')
ts = dt.timestamp()
print(ts)

print('将timestamp转换为datetime，根据本地时间')
dtt = datetime.fromtimestamp(ts)
print(dtt)

print('将timestamp转换为datetime，根据UTC时间')
dtutc = datetime.utcfromtimestamp(ts)
print(dtutc)

print('将字符串转化为日期指定格式')
cday = datetime.strptime('2015-6-1 18:19:45', '%Y-%m-%d %H:%M:%S')
print(cday)

print('将datetime转换为str')
s = now.strftime('%a, %b %d %H:%M')
print(s)

print('datetime加减')
# datetime加减
now10hour = now + timedelta(hours=10)
print(now10hour)

now1day = now - timedelta(days=1)
print(now1day)

now2day12hours = now + timedelta(days=2, hours=12)
print(now2day12hours)

print('本地时间转换为UTC时间')
# 创建时区UTC+8:00
tz_utc_8 = timezone(timedelta(hours=8))
# 强制设置为UTC+8:00
dt = now.replace(tzinfo=tz_utc_8)
print(dt)

print('时区转换')
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_dt)
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print(bj_dt)
tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
print(tokyo_dt)
tokyo_dt2 = bj_dt.astimezone(timezone(timedelta(hours=9)))
print(tokyo_dt2)
