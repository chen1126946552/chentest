from services.data_services.calculate import CalculatedDataHandler
import pandas as pd


def test_me():
    """ Fetching Data: calculated fields function UT """

    data_rows = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5], [6, 6, 6], [99, 99, 99]]

    df = pd.DataFrame(data=data_rows, columns=['col1', 'col2', 'col3'])

    df['d1'] = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    df = df.reindex(columns=['d1', 'col1', 'col2', 'col3'])

    fields = [
        {'id': 'd1', 'type': 'string', 'groupBy': True, 'uuid': 'd1'},
        {'id': 'col1', 'type': 'number', 'uuid': 'col1'},
        {'id': 'col2', 'type': 'number', 'uuid': 'col2'},
        {'id': 'col3', 'type': 'number', 'uuid': 'col3'},
    ]

    cal_fields = [
        {'id': 'c1', 'type': 'number', 'isCal': True,
         'uuid': 'c1',
         'expression': "$id_col1 + $id_col1 + $id_col1*3",
         'keys': ['col1'],
         'fields': [
             {'id': 'col1', 'name': 'col1', 'type': 'number', 'displayFormat': None,
              'allowFilter': False, 'allowGroupby': False, 'allowSegment': True
              }
         ]
         },
        {'id': 'c2', 'type': 'number', 'isCal': True,
         'uuid': 'c2',
         'expression': "($id_col1*($id_col2/$id_col3-10))*$id_col2",
         'keys': ['col1', 'col2', 'col3'],
         'fields': [
             {'id': 'col1', 'name': 'col1', 'type': 'number', 'displayFormat': None,
              'allowFilter': False, 'allowGroupby': False, 'allowSegment': True
              },
             {'id': 'col2', 'name': 'col2', 'type': 'number', 'displayFormat': None,
              'allowFilter': False, 'allowGroupby': False, 'allowSegment': True
              },
             {'id': 'col3', 'name': 'col3', 'type': 'number', 'displayFormat': None,
              'allowFilter': False, 'allowGroupby': False, 'allowSegment': True
              }
         ]
         }
    ]

    info = CalculatedDataHandler.check_calf_expression("$id_a + $id_b", keys=['a', 'b'])

    assert info
    assert info['function_contain'] is False
    assert info['group_function_contain'] is False

    res_df = CalculatedDataHandler(df, fields=fields, cal_fields=cal_fields).execute()

    result = res_df.values.tolist()

    answer = [['a', 1, 1, 1, 5, -9.0],
              ['b', 2, 2, 2, 10, -36.0],
              ['c', 3, 3, 3, 15, -81.0],
              ['d', 4, 4, 4, 20, -144.0],
              ['e', 5, 5, 5, 25, -225.0],
              ['f', 6, 6, 6, 30, -324.0],
              ['g', 99, 99, 99, 495, -88209.0]
              ]

    assert result == answer