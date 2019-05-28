import requests_mock
import json
from deepdiff import DeepDiff
from dataclasses import asdict
from services.data_services.data import FetchingDataHandler


@requests_mock.Mocker(kw='mock')
def test_data_fetching_map(test_client, **kwargs):
    ds_code = 'gav4_or_whatever'

    req_from_business = """
    {
    "weekStartOn":"monday",
    "timezone":"Asia/Shanghai",
    "path":[
        "61079646",
        "UA-61079646-1",
        "102134393"
    ],
    "locale":"en_US",
    "graphType":"map",
    "map":{
        "mapType":"country",
        "geographyField":"ga:region",
        "mapCode":"Japan"
    },
    "paging":{
        "size":10000
    },
    "fields":[
        {
            "type":"string",
            "uuid":"232c08dd-4c7b-11e9-8efd-1002b5d9f459",
            "groupBy":true,
            "id":"ga:region"
        },
        {
            "id":"ga:users",
            "type":"number",
            "uuid":"456d5858-fad1-4352-8e56-4b32caf90b3d"
        }
    ],
    "filters":[
        {
            "field":{
                "id":"ga:country",
                "type":"string",
                "groupBy":true,
                "uuid":"232c08de-4c7b-11e9-8efd-1002b5d9f459"
            },
            "operator":"equal",
            "values":[
                "Japan"
            ]
        }
    ],
    "segment":{

    },
    "sort":{

    },
    "dateRange":{
        "field":null,
        "code":"custom",
        "value":"2019/03/15|2019/03/22"
    },
    "compareWithPrevious":{

    },
    "noCache":true,
    "calculatedFields":[

    ],
    "seq":[
        "232c08dd-4c7b-11e9-8efd-1002b5d9f459",
        "456d5858-fad1-4352-8e56-4b32caf90b3d"
    ]
}
    """
    REQ_TO_GA_ANSWER = {'token': None,
                        'path': ['61079646', 'UA-61079646-1', '102134393'], 'locale': 'en_US',
                        'timezoneOffset': 28800, 'paging': {'size': 10000}, 'filters': [
            {'fieldId': 'ga:country', 'operator': 'equal', 'values': ['Japan']}],
                        'dateRange': {'field': None, 'start': 1552579200000, 'end': 1553270400000},
                        'sort': {}, 'segment': {}, 'fields': [
            {'type': 'string', 'uuid': '232c08dd-4c7b-11e9-8efd-1002b5d9f459', 'groupBy': True,
             'id': 'ga:region'},
            {'id': 'ga:users', 'type': 'number', 'uuid': '456d5858-fad1-4352-8e56-4b32caf90b3d'}],
                        'calculatedFields': None}

    resp_from_ds = {
        'data': [
            ['(not set)', 4149], ['Aichi Prefecture', 25], ['Aomori Prefecture', 1],
            ['Chiba Prefecture', 4], ['Ehime Prefecture', 7], ['Fukuoka Prefecture', 7],
            ['Fukushima Prefecture', 3], ['Gunma Prefecture', 1], ['Hiroshima Prefecture', 19],
            ['Hokkaido', 86], ['Hyogo Prefecture', 9], ['Kanagawa Prefecture', 26],
            ['Kumamoto Prefecture', 140], ['Kyoto Prefecture', 839], ['Miyagi Prefecture', 1],
            ['Nagano Prefecture', 1], ['Nagasaki Prefecture', 2], ['Niigata Prefecture', 1],
            ['Okinawa Prefecture', 5], ['Osaka Prefecture', 662], ['Saitama Prefecture', 6],
            ['Shizuoka Prefecture', 3], ['Tochigi Prefecture', 2], ['Tokyo', 31501],
            ['Toyama Prefecture', 2], ['Yamanashi Prefecture', 194]
        ],
        'immutable': False,
        'summaryValues': [37772]
    }

    RESULT_ANSWER = {
        "header": [
            {"type": "string", "uuid": "232c08dd-4c7b-11e9-8efd-1002b5d9f459", "groupBy": True,
             "id": "ga:region"},
            {"id": "ga:users", "type": "number", "uuid": "456d5858-fad1-4352-8e56-4b32caf90b3d"}
        ],
        "data": [
            ["(not set)", 4149], ["Aichi Prefecture", 25],
            ["Aomori Prefecture", 1],
            ["Chiba Prefecture", 4], ["Ehime Prefecture", 7],
            ["Fukuoka Prefecture", 7],
            ["Fukushima Prefecture", 3], ["Gunma Prefecture", 1],
            ["Hiroshima Prefecture", 19], ["Hokkaido", 86],
            ["Hyogo Prefecture", 9],
            ["Kanagawa Prefecture", 26], ["Kumamoto Prefecture", 140],
            ["Kyoto Prefecture", 839], ["Miyagi Prefecture", 1],
            ["Nagano Prefecture", 1],
            ["Nagasaki Prefecture", 2], ["Niigata Prefecture", 1],
            ["Okinawa Prefecture", 5],
            ["Osaka Prefecture", 662], ["Saitama Prefecture", 6],
            ["Shizuoka Prefecture", 3],
            ["Tochigi Prefecture", 2], ["Tokyo", 31501], ["Toyama Prefecture", 2],
            ["Yamanashi Prefecture", 194]
        ],
        "summaryValues": [None, 37772]
    }

    kwargs['mock'].post(f'http://datadeck-datasource-{ds_code}:9090/data',
                        json=resp_from_ds)

    req_params = json.loads(req_from_business)

    hack_in_middle = FetchingDataHandler(ds_code=ds_code, params=req_params)

    result = hack_in_middle.get_result()

    req_body = asdict(hack_in_middle.req_body)

    diff1 = DeepDiff(req_body, REQ_TO_GA_ANSWER)

    assert not diff1

    diff2 = DeepDiff(result, RESULT_ANSWER)

    assert not diff2
