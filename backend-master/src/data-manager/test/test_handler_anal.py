from services.data_services.analyze import AnalyzeDataHandler

import pandas as pd


def test_me():
    """ Fetching Data: analyze function UT """

    data_rows = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5], [6, 6, 6], [99, 99, 99]]

    df = pd.DataFrame(data=data_rows, columns=['col1', 'col2', 'col3'])

    df['d1'] = ['a', 'a', 'b', 'b', 'c', 'c', 'c']
    df['d2'] = ['a', 'b', 'c', 'a', 'b', 'c', 'c']
    df['d3'] = ['a', 'b', 'c', 'a', 'a', 'c', 'c']

    df = df.reindex(columns=['d1', 'd2', 'd3', 'col1', 'col2', 'col3'])

    cols_operation_map = {
        'col1': 'cumulate',
        'col2': 'growth_rate',
        'col3': 'proportion'
    }

    res_df = AnalyzeDataHandler(data_frame=df, cols_operation_map=cols_operation_map,
                                group_by_columns=['d1', 'd2', 'd3']).execute()

    result = res_df.where(res_df.notnull(), None).values.tolist()
    answer = [
        ['a', 'a', 'a', 1.0, None, 0.0476],
        ['a', 'b', 'b', 2.0, None, 0.0952],
        ['b', 'c', 'c', 3.0, None, 0.1429],
        ['b', 'a', 'a', 5.0, 3.0, 0.1905],
        ['c', 'b', 'a', 5.0, None, 0.2381],
        ['c', 'c', 'c', 9.0, 1.0, 0.2857],
        ['c', 'c', 'c', None, None, None]
    ]

    assert answer == result
