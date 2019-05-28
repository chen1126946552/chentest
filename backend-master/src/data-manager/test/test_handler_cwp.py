from services.data_services.compare_with_previous import CompareWithPreviousHandler
from common.uncategorized.datetime_util import DateTime
import pandas as pd
from deepdiff import DeepDiff
import pytz


def test_me():
    """ Fetching Data: compare with previous function UT """

    dates = [
        "2018-12-01",
        "2019-01-01",
        "2019-02-01",
        "2019-03-01",
        "2019-04-01",
        "2019-05-01",
        "2019-06-01",
        "2019-07-01",
    ]

    tz_name = 'Asia/Shanghai'

    dates_ts_1 = [DateTime(tz=tz_name, ds=ds, fmt="%Y-%m-%d").timestamp for ds in
                  dates[1:]] + [1]
    dates_ts_2 = [DateTime(tz=tz_name, ds=ds, fmt="%Y-%m-%d").timestamp for ds in
                  dates[:-1]] + [1]
    print('\ntimestamp1: ', dates_ts_1, '\ntimestamp2: ', dates_ts_2)

    data_1 = [[72, 89], [24, 75], [50, 19], [0, 18], [63, 1], [15, 32], [66, 12], [10000, 10000]]
    data_2 = [[76, 58], [70, 36], [0, 20], [52, 51], [57, 8], [3, 13], [6, 20], [999, 999]]

    dfx = pd.DataFrame(data=data_1, columns=['a', 'b'])
    dfy = pd.DataFrame(data=data_2, columns=['a', 'b'])

    dfx['t'] = dates_ts_1
    dfy['t'] = dates_ts_2

    dfx = dfx.reindex(columns=['t', 'a', 'b'])
    dfy = dfy.reindex(columns=['t', 'a', 'b'])

    assert list(dfx) == ['t', 'a', 'b']

    fields = [
        {'id': 't', 'uuid': 't', 'type': 'date', 'dataFormat': 'day', 'groupBy': True},
        {'id': 'a', 'uuid': 'a', 'type': 'number'},
        {'id': 'b', 'uuid': 'b', 'type': 'number'}
    ]

    setting = {
        'fields': [fields[1], fields[2]],
        'code': 'mom',
        'computing': 'growth_rate',
    }

    result = CompareWithPreviousHandler(
        df1=dfx, df2=dfy, fields=fields, setting=setting, sort={}, timezone=tz_name,
        week_start_on='monday'
    ).execute()

    result = result.values.tolist()

    answer = [
        [1546272000000, 72, -0.0526, 89, 0.5345],
        [1548950400000, 24, -0.6571, 75, 1.0833],
        [1551369600000, 50, None, 19, -0.05],
        [1554048000000, 0, -1.0, 18, -0.6471],
        [1556640000000, 63, 0.1053, 1, -0.875],
        [1559318400000, 15, 4.0, 32, 1.4615],
        [1561910400000, 66, 10.0, 12, -0.4],
        [1, 10000, None, 10000, None]
    ]

    assert result == answer
