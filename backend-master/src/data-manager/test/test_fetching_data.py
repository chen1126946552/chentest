import requests_mock
import json
from deepdiff import DeepDiff
from dataclasses import asdict
from services.data_services.data import FetchingDataHandler


@requests_mock.Mocker(kw='mock')
def test_data_fetching(test_client, **kwargs):
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
    "paging":{
        "size":10000
    },
    "fields":[
        {
            "id":"ga:date",
            "type":"date",
            "dataFormat":"day",
            "groupBy":true,
            "uuid":"bb70d0b9-d76e-4883-8601-8a8b669c8a40"
        },
        {
            "id":"ga:userType",
            "type":"string",
            "groupBy":true,
            "uuid":"21010164-3fc1-401f-8c73-5ea01461c708"
        },
        {
            "id":"ga:users",
            "type":"number",
            "uuid":"4365ddac-8141-4032-be55-ee8b474040a1"
        },
        {
            "id":"ga:users",
            "type":"number",
            "anal":"proportion",
            "uuid":"d44a893c-37db-49b9-872d-8f6591aaaf80"
        },
        {
            "id":"ga:newUsers",
            "type":"number",
            "uuid":"722ac0dd-40b0-4550-8905-4c81effa18e0"
        }
    ],
    "filters":[

    ],
    "segment":{

    },
    "sort":{
        "field":{
            "id":"1edd6ab5-416d-11e9-be9c-1002b5d9f459",
            "type":"number",
            "isCal":true,
            "uuid":"a9e5c966-a7b0-4a0c-8aa7-a48787c3f425"
        },
        "order":"asc"
    },
    "dateRange":{
        "field":null,
        "code":"custom",
        "value":"2019/01/01|2019/03/01"
    },
    "compareWithPrevious":{

    },
    "noCache":true,
    "calculatedFields":[
        {
            "id":"1edd6ab5-416d-11e9-be9c-1002b5d9f459",
            "type":"number",
            "anal":"proportion",
            "isCal":true,
            "uuid":"a9e5c966-a7b0-4a0c-8aa7-a48787c3f425",
            "expression":"$id_ga:users+100 + $id_ga:sessions",
            "keys":[
                "ga:users",
                "ga:sessions"
            ],
            "fields":[
                {
                    "id":"ga:users",
                    "name":"Users",
                    "type":"number",
                    "displayFormat":null,
                    "allowFilter":false,
                    "allowGroupby":false,
                    "allowSegment":true
                },
                {
                    "id":"ga:sessions",
                    "name":"Sessions",
                    "type":"number",
                    "displayFormat":null,
                    "allowFilter":false,
                    "allowGroupby":false,
                    "allowSegment":true
                }
            ],
            "allow_filter":false,
            "filter_ops":[

            ],
            "allow_aggregation":false,
            "aggregation_ops":[

            ]
        }
    ],
    "seq":[
        "bb70d0b9-d76e-4883-8601-8a8b669c8a40",
        "21010164-3fc1-401f-8c73-5ea01461c708",
        "4365ddac-8141-4032-be55-ee8b474040a1",
        "a9e5c966-a7b0-4a0c-8aa7-a48787c3f425",
        "d44a893c-37db-49b9-872d-8f6591aaaf80",
        "722ac0dd-40b0-4550-8905-4c81effa18e0"
    ]
}
    """

    REQ_TO_GA_ANSWER = {'token': None, 'path': ['61079646', 'UA-61079646-1', '102134393'],
                        'locale': 'en_US', 'timezoneOffset': 28800, 'paging': {'size': 10000},
                        'filters': [],
                        'dateRange': {'field': None, 'start': 1546272000000, 'end': 1551456000000},
                        'sort': {}, 'segment': {}, 'fields': [
            {'id': 'ga:date', 'type': 'date', 'dataFormat': 'day', 'groupBy': True,
             'uuid': 'bb70d0b9-d76e-4883-8601-8a8b669c8a40'},
            {'id': 'ga:userType', 'type': 'string', 'groupBy': True,
             'uuid': '21010164-3fc1-401f-8c73-5ea01461c708'},
            {'id': 'ga:users', 'type': 'number', 'uuid': '4365ddac-8141-4032-be55-ee8b474040a1'},
            {'id': 'ga:users', 'type': 'number', 'anal': 'proportion',
             'uuid': 'd44a893c-37db-49b9-872d-8f6591aaaf80'},
            {'id': 'ga:newUsers', 'type': 'number', 'uuid': '722ac0dd-40b0-4550-8905-4c81effa18e0'},
            {'id': 'ga:sessions', 'name': 'Sessions', 'type': 'number', 'displayFormat': None,
             'allowFilter': False, 'allowGroupby': False, 'allowSegment': True,
             'uuid': 'hidden_field:1'}], 'calculatedFields': None}

    resp_from_ga = {'data': [[1552233600000, 'New Visitor', 50279, 50279, 50444, 50444],
                             [1552233600000, 'Returning Visitor', 1388, 1388, 0, 1572],
                             [1552320000000, 'New Visitor', 51270, 51270, 50441, 50441],
                             [1552320000000, 'Returning Visitor', 1410, 1410, 0, 1562],
                             [1552406400000, 'New Visitor', 26733, 26733, 26603, 26603],
                             [1552406400000, 'Returning Visitor', 964, 964, 0, 1055]],
                    'immutable': False,
                    'summaryValues': [130846, 130846, 127486, 131677]}

    RESULT_ANSWER = {
        'header': [
            {'id': 'ga:date', 'type': 'date', 'dataFormat': 'day', 'groupBy': True,
             'uuid': 'bb70d0b9-d76e-4883-8601-8a8b669c8a40'},
            {'id': 'ga:userType', 'type': 'string', 'groupBy': True,
             'uuid': '21010164-3fc1-401f-8c73-5ea01461c708'},
            {'id': 'ga:users', 'type': 'number', 'uuid': '4365ddac-8141-4032-be55-ee8b474040a1'},
            {'id': '1edd6ab5-416d-11e9-be9c-1002b5d9f459', 'type': 'number', 'anal': 'proportion',
             'isCal': True, 'uuid': 'a9e5c966-a7b0-4a0c-8aa7-a48787c3f425',
             'expression': '$id_ga:users+100 + $id_ga:sessions',
             'keys': ['ga:users', 'ga:sessions'],
             'fields': [{'id': 'ga:users', 'name': 'Users', 'type': 'number', 'displayFormat': None,
                         'allowFilter': False, 'allowGroupby': False, 'allowSegment': True},
                        {'id': 'ga:sessions', 'name': 'Sessions', 'type': 'number',
                         'displayFormat': None, 'allowFilter': False, 'allowGroupby': False,
                         'allowSegment': True, 'uuid': 'hidden_field:1'}], 'allow_filter': False,
             'filter_ops': [], 'allow_aggregation': False, 'aggregation_ops': []},
            {'id': 'ga:users', 'type': 'number', 'anal': 'proportion',
             'uuid': 'd44a893c-37db-49b9-872d-8f6591aaaf80'},
            {'id': 'ga:newUsers', 'type': 'number', 'uuid': '722ac0dd-40b0-4550-8905-4c81effa18e0'}
        ],
        'data': [
            [1552406400000, 'Returning Visitor', 964, 0.008, 0.0073, 0],
            [1552233600000, 'Returning Visitor', 1388, 0.0116, 0.0105, 0],
            [1552320000000, 'Returning Visitor', 1410, 0.0116, 0.0107, 0],
            [1552406400000, 'New Visitor', 26733, 0.2022, 0.2025, 26603],
            [1552233600000, 'New Visitor', 50279, 0.3814, 0.3808, 50444],
            [1552320000000, 'New Visitor', 51270, 0.3852, 0.3883, 50441]
        ],
        'summaryValues': [None, None, 130846, None, None, 127486]
    }

    kwargs['mock'].post(f'http://datadeck-datasource-{ds_code}:9090/data',
                        json=resp_from_ga)

    req_params = json.loads(req_from_business)

    hack_in_middle = FetchingDataHandler(ds_code=ds_code, params=req_params)

    result = hack_in_middle.get_result()

    req_body = asdict(hack_in_middle.req_body)

    diff1 = DeepDiff(req_body, REQ_TO_GA_ANSWER)

    assert not diff1

    diff2 = DeepDiff(result, RESULT_ANSWER)

    assert not diff2


@requests_mock.Mocker(kw='mock')
def test_data_fetching_cwp(test_client, **kwargs):
    # prepare connection id
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
    "paging":{
        "size":10000
    },
    "fields":[
        {
            "id":"ga:date",
            "type":"date",
            "dataFormat":"day",
            "groupBy":true,
            "uuid":"86df36e1-f990-42b9-81b7-78ccf574aa9e"
        },
        {
            "id":"ga:userType",
            "type":"string",
            "groupBy":true,
            "uuid":"63fa8ecd-eead-4ede-84f8-8f0590d06bb4"
        },
        {
            "id":"ga:users",
            "type":"number",
            "anal":"proportion",
            "uuid":"8ecdaae4-14da-49ed-8cf7-2d16a3de0015"
        },
        {
            "id":"ga:users",
            "type":"number",
            "uuid":"6bf3932d-e064-452e-8a42-f22b3b01901a"
        },
        {
            "id":"ga:newUsers",
            "type":"number",
            "uuid":"b41051f6-4dcb-47e6-b91d-badce07adf70"
        }
    ],
    "filters":[
        {
            "field":{
                "id":"ga:users",
                "type":"number",
                "groupBy":true,
                "uuid":"c49c2653-6a5f-4d04-b513-2b2e8017b08c"
            },
            "operator":"gt",
            "values":[
                "1000"
            ]
        }
    ],
    "segment":{

    },
    "sort":{
        "field":{
            "id":"ga:newUsers",
            "type":"number",
            "uuid":"b41051f6-4dcb-47e6-b91d-badce07adf70"
        },
        "order":"desc"
    },
    "dateRange":{
        "field":null,
        "code":"custom",
        "value":"2019/01/01|2019/03/01"
    },
    "compareWithPrevious":{
        "fields":[
            {
                "id":"ga:users",
                "type":"number",
                "anal":"proportion",
                "uuid":"8ecdaae4-14da-49ed-8cf7-2d16a3de0015"
            },
            {
                "id":"ga:users",
                "type":"number",
                "uuid":"6bf3932d-e064-452e-8a42-f22b3b01901a"
            },
            {
                "id":"1edd6ab5-416d-11e9-be9c-1002b5d9f459",
                "type":"number",
                "isCal":true,
                "uuid":"30289529-8f19-416f-89ed-c03c5a173318"
            },
            {
                "id":"ga:newUsers",
                "type":"number",
                "uuid":"b41051f6-4dcb-47e6-b91d-badce07adf70"
            }
        ],
        "code":"mom",
        "computing":null
    },
    "noCache":true,
    "calculatedFields":[
        {
            "id":"1edd6ab5-416d-11e9-be9c-1002b5d9f459",
            "type":"number",
            "isCal":true,
            "uuid":"30289529-8f19-416f-89ed-c03c5a173318",
            "expression":"$id_ga:users+100 + $id_ga:sessions",
            "keys":[
                "ga:users",
                "ga:sessions"
            ],
            "fields":[
                {
                    "id":"ga:users",
                    "name":"Users",
                    "type":"number",
                    "displayFormat":null,
                    "allowFilter":false,
                    "allowGroupby":false,
                    "allowSegment":true
                },
                {
                    "id":"ga:sessions",
                    "name":"Sessions",
                    "type":"number",
                    "displayFormat":null,
                    "allowFilter":false,
                    "allowGroupby":false,
                    "allowSegment":true
                }
            ],
            "allow_filter":false,
            "filter_ops":[

            ],
            "allow_aggregation":false,
            "aggregation_ops":[

            ]
        }
    ],
    "seq":[
        "86df36e1-f990-42b9-81b7-78ccf574aa9e",
        "63fa8ecd-eead-4ede-84f8-8f0590d06bb4",
        "8ecdaae4-14da-49ed-8cf7-2d16a3de0015",
        "6bf3932d-e064-452e-8a42-f22b3b01901a",
        "30289529-8f19-416f-89ed-c03c5a173318",
        "b41051f6-4dcb-47e6-b91d-badce07adf70"
    ]
}
    """

    REQ_TO_GA_ANSWER_IN_SECOND_TIME_FOR_CWP = {'token': None,
                                               'path': ['61079646', 'UA-61079646-1', '102134393'],
                                               'locale': 'en_US', 'timezoneOffset': 28800,
                                               'paging': {'size': 10000}, 'filters': [
            {'fieldId': 'ga:users', 'operator': 'gt', 'values': ['1000']}],
                                               'dateRange': {'field': None, 'start': 1543593600000,
                                                             # 2018/12/1 - 2019/2/1
                                                             'end': 1549036798999}, 'sort': {
            'field': {'id': 'ga:newUsers', 'type': 'number',
                      'uuid': 'b41051f6-4dcb-47e6-b91d-badce07adf70'}, 'order': 'desc'},
                                               'segment': {}, 'fields': [
            {'id': 'ga:date', 'type': 'date', 'dataFormat': 'day', 'groupBy': True,
             'uuid': '86df36e1-f990-42b9-81b7-78ccf574aa9e'},
            {'id': 'ga:userType', 'type': 'string', 'groupBy': True,
             'uuid': '63fa8ecd-eead-4ede-84f8-8f0590d06bb4'},
            {'id': 'ga:users', 'type': 'number', 'anal': 'proportion',
             'uuid': '8ecdaae4-14da-49ed-8cf7-2d16a3de0015'},
            {'id': 'ga:users', 'type': 'number', 'uuid': '6bf3932d-e064-452e-8a42-f22b3b01901a'},
            {'id': 'ga:newUsers', 'type': 'number', 'uuid': 'b41051f6-4dcb-47e6-b91d-badce07adf70'},
            {'id': 'ga:sessions', 'name': 'Sessions', 'type': 'number', 'displayFormat': None,
             'allowFilter': False, 'allowGroupby': False, 'allowSegment': True,
             'uuid': 'hidden_field:1'}], 'calculatedFields': None}

    hack_in_middle = FetchingDataHandler(ds_code=ds_code, params=json.loads(req_from_business))

    try:
        # data fetching request within compare with previous fields CANNOT BE MOCKED HERE
        # because it will calling two times external service in one request!
        # This is just to trigger the handler to execute, make the request body for testing
        result = hack_in_middle.get_result()
    except:
        pass

    assert hack_in_middle.is_cal_active is True
    assert hack_in_middle.is_cwp_active is True

    hack_in_middle.req_body.dateRange = hack_in_middle.parse_date_range_cwp()
    req_body_the_second_time = asdict(hack_in_middle.req_body)

    diff = DeepDiff(req_body_the_second_time, REQ_TO_GA_ANSWER_IN_SECOND_TIME_FOR_CWP)

    assert not diff
