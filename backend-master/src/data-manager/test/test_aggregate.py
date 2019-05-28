"""Aggregate test"""

from services.data_services.aggregate import AggregateHandler
import pandas as pd

data_list = [[1555327576, 'charge', 12516], [1555322403, 'charge', 41976], [1555321594, 'charge', 41976],
             [1555241191, 'charge', 12514], [1555235142, 'charge', 41965], [1555154950, 'charge', 12514],
             [1555148633, 'charge', 41965], [1555068663, 'charge', 12568], [1555062300, 'charge', 42149],
             [1554982143, 'charge', 12547], [1554975899, 'charge', 42078], [1554895560, 'charge', 12560],
             [1554889495, 'charge', 42122], [1554815327, 'charge', 12548], [1554803324, 'charge', 42144],
             [1554799407, 'charge', 7276], [1554722765, 'charge', 12614], [1554716771, 'charge', 42302],
             [1554636413, 'charge', 12610], [1554630262, 'charge', 42288], [1554550021, 'charge', 12610],
             [1554544021, 'charge', 42288], [1554463532, 'charge', 12607], [1554457474, 'charge', 42278],
             [1554377170, 'charge', 12582], [1554371188, 'charge', 42196], [1554290683, 'charge', 12630],
             [1554284663, 'charge', 42358], [1554204408, 'charge', 12628], [1554198290, 'charge', 42351],
             [1554117962, 'charge', 12606], [1554111853, 'charge', 42275], [1554031571, 'charge', 12610],
             [1554025485, 'charge', 42288], [1554022621, 'charge', 25329], [1553945193, 'charge', 12610],
             [1553939156, 'charge', 42288], [1553936144, 'charge', 25329], [1553858844, 'charge', 12600],
             [1553852777, 'charge', 42255], [1553849798, 'charge', 25309], [1553772359, 'charge', 12575],
             [1553766387, 'charge', 42172], [1553765540, 'charge', 120731], [1553763431, 'charge', 25259],
             [1553762354, 'charge', 7281], [1553685918, 'charge', 12551], [1553679922, 'charge', 42095],
             [1553677094, 'charge', 25213], [1553649209, 'payout', -2892767], [1553599601, 'charge', 12506],
             [1553593463, 'charge', 41940], [1553590586, 'charge', 25120], [1553513215, 'charge', 12529],
             [1553507067, 'charge', 42019], [1553504241, 'charge', 25168], [1553426680, 'charge', 12515],
             [1553420669, 'charge', 41972], [1553417702, 'charge', 25139], [1553340349, 'charge', 12515],
             [1553334242, 'charge', 41972], [1553331319, 'charge', 25139], [1553253918, 'charge', 12443],
             [1553247935, 'charge', 41731], [1553245036, 'charge', 24995], [1553167609, 'charge', 12380],
             [1553161570, 'charge', 41519], [1553158575, 'charge', 24868], [1553081157, 'charge', 12460],
             [1553075032, 'charge', 41788], [1553072186, 'charge', 25029], [1552994819, 'charge', 12483],
             [1552988681, 'charge', 41864], [1552987074, 'charge', 6275], [1552987073, 'charge', 6275],
             [1552985795, 'charge', 25075], [1552908337, 'charge', 12500], [1552902330, 'charge', 41920],
             [1552899405, 'charge', 25108], [1552821931, 'charge', 12484], [1552815964, 'charge', 41870],
             [1552812936, 'charge', 25078]]


class RequestBody:

    def __init__(self) -> None:
        self.fields = [
            {'id': 'created', 'type': 'date', 'groupBy': True, 'uuid': '1b7a4a90-d0f7-40b5-b271-3ea3b9781242'},
            {'id': 'type', 'type': 'string', 'groupBy': True, 'uuid': '377fde1e-c3a0-4d72-8971-d27a524b5577'},
            {'id': 'net', 'type': 'number', 'agg': 'sum', 'uuid': '8a4d42c9-caef-4952-be8a-55fae784ac01'}]
        self.sort = {'field': {'id': 'net', 'type': 'number', 'agg': 'sum',
                               'uuid': '8a4d42c9-caef-4952-be8a-55fae784ac01'}, 'order': 'desc'}


def test_aggregate():
    req_body = RequestBody()

    cols = [f['uuid'] for f in req_body.fields]
    df = pd.DataFrame(data=data_list, columns=cols, dtype=object)
    data_result = AggregateHandler(df, req_body).execute()
    assert data_result.get('summaryValues')[0] == -686952
