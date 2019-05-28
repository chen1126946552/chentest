from common.uncategorized.datetime_util import DateTime as DT
from datetime import datetime
import pytz


def test():
    """
            Feb 2019
    Sun Mon Tue Wed Thu Fri Sat
                         1   2
     3   4   5   6   7   8   9
    10  11  12  13 |14| 15  16
    17  18  19  20  21  22  23
    24  25  26  27  28

    """

    zone = 'Asia/Shanghai'
    tz = pytz.timezone(zone)
    now = datetime(2019, 2, 14, 8, 0, 0, 0, tzinfo=tz)
    ts = int(now.timestamp() * 1000)

    # injecting fake _get_now method
    dt = DT(dt=now)
    # setattr(dt, '_datetime_init', lambda *args: now)

    # utc time
    s1 = dt.datetime.strftime('%Y-%m-%d %H:%M:%S')
    assert s1 == '2019-02-14 08:00:00'

    s2 = dt.today_start.datetime.strftime('%Y-%m-%d %H:%M:%S')
    assert s2 == '2019-02-14 00:00:00'
    s3 = dt.today_end.datetime.strftime('%Y-%m-%d %H:%M:%S')
    assert s3 == '2019-02-15 00:00:00'

    s4 = dt.week_start.datetime.strftime('%Y-%m-%d %H:%M:%S')
    assert s4 == '2019-02-11 00:00:00'
    s5 = dt.week_end.datetime.strftime('%Y-%m-%d %H:%M:%S')
    assert s5 == '2019-02-18 00:00:00'
    assert dt.month_start.datetime.strftime('%Y-%m-%d %H:%M:%S') == '2019-02-01 00:00:00'
    assert dt.month_end.datetime.strftime('%Y-%m-%d %H:%M:%S') == '2019-03-01 00:00:00'

    assert dt.offset(month=-1).datetime.strftime('%Y-%m-%d %H:%M:%S') == '2019-01-14 08:00:00'
    assert dt.offset(month=1).datetime.strftime('%Y-%m-%d %H:%M:%S') == '2019-03-14 08:00:00'
    assert dt.offset(year=-1).datetime.strftime('%Y-%m-%d %H:%M:%S') == '2018-02-14 08:00:00'
    assert dt.offset(year=1).datetime.strftime('%Y-%m-%d %H:%M:%S') == '2020-02-14 08:00:00'
    assert dt.offset(day=-1).datetime.strftime('%Y-%m-%d %H:%M:%S') == '2019-02-13 08:00:00'
    assert dt.offset(day=1).datetime.strftime('%Y-%m-%d %H:%M:%S') == '2019-02-15 08:00:00'

    assert DT.get_offset(zone) == 28800
