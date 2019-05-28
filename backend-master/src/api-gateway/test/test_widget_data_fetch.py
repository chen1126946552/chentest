import re
import json
import requests_mock
import pytest

from services.adaptors.data import DataAdaptor
from blueprints.widget import widget_export_data

DOWNSTREAM_BUSINESS_HOST = "http://datadeck-business:9081/api/v1"
DOWNSTREAM_V2_HOST = "https://middlev2.datadeck.com"

resp_datasources = [
    {'id': '423749823749', 'code': 'googleanalytics-v4',
     'name': 'googleanalytics-v4', 'description': 'googleanalytics-v4',
     'api_version': 'v4', 'published': True, 'ds_id': 1001, 'type': 'api'},
    {'id': '423749823750', 'code': 'redshift',
     'name': 'redshift', 'description': 'redshift',
     'api_version': 'v4', 'published': True, 'ds_id': 1002, 'type': 'db'},

]


@requests_mock.Mocker(kw='mock')
def test_fields(test_client, **kwargs):
    ds_connection_id = "028b02e2-3d4c-4077-89b6-30dd2701b80b"
    business_connection_id = "bc123"

    matcher0 = re.compile(DOWNSTREAM_V2_HOST + "/api/v2/users/signinValidate")
    matcher1 = re.compile(DOWNSTREAM_V2_HOST + "/api/v2/spaces")

    # mock token check
    kwargs['mock'].get(matcher0,
                       json={"success": True})

    kwargs['mock'].get(matcher1, json={'success': True, 'data': {'weekStart': 'monday'}})
    # mock datasources api
    kwargs['mock'].get(f"{DOWNSTREAM_BUSINESS_HOST}/datasources",
                       json=resp_datasources)

    kwargs['mock'].get(f'{DOWNSTREAM_V2_HOST}/api/v1/connections/config/my_ds_connection_id', json={'success': True, 'message': None, 'stackTrace': None, 'data': {'dsConnectionId': '143b6ecb-268f-4d58-bf44-0502fa86783d', 'config': [{'index': 0, 'id': 'my_business_connection_id', 'noAuth': True, 'name': 'bingxing.kang@ptmind.com', 'type': 'account'}, {'type': 'profile', 'noAuth': True, 'index': 1, 'requestParams': {'id': 'profile', 'provider': 'googleanalytics-v4', 'params': {'account.id': 'aad1ea87-1576-11e9-9d60-1002b5d9f459', 'account.name': 'bingxing.kang@ptmind.com'}}, 'name': 'All Website', 'id': '["112670961", "UA-112670961-1", "168081726"]'}], 'dsId': 1001, 'uid': None, 'spaceId': 'c7ecdc29-bcd9-404c-80b6-a1a32329b93e'}, 'errorCode': None, 'params': None})

    kwargs['mock'].post(f'{DOWNSTREAM_BUSINESS_HOST}/connections/my_business_connection_id/data', json={
        'header': [{'id': 'ga:userDefinedValue', 'type': 'string', 'groupBy': True, 'uuid': '157edf42-572a-47be-8dc8-bd6a3b217b53'},
                   {'id': 'ga:sessionCount', 'type': 'string', 'groupBy': True, 'uuid': '7671076c-9955-41e4-83d5-69dccbf4b4fc'},
                   {'id': 'ga:newUsers', 'type': 'number', 'uuid': '1c8cae01-280c-49e6-bb05-c5ea2f5c1adb', },
                   {'id': 'ga:users', 'type': 'number', 'uuid': '4cd78734-5ba4-4da3-8b39-0b9f6fa213fe'}],
        'data': [[1, "a", 2, 3], [2, "b", 3, 4]],
        'summaryValues': [3, 4, 5, 6],
        'nextPageCursor': 'xxx'
    })


    preview_data_req_body = """
    {"widgetId":null,"spaceId":"c7ecdc29-bcd9-404c-80b6-a1a32329b93e","panelId":"1ab7b7c9-aef4-4b79-b003-8c2edf3559e7","dsConnectionId":"my_ds_connection_id","name":"","isTitleUpdate":"0","graphType":"table","widgetType":"chart","fields":[{"allowFilter":0,"allowGroup":true,"allowScope":null,"allowSegment":1,"code":"ga:userDefinedValue","containGroupFunction":false,"dataType":"STRING","defaultScope":null,"extra":{"allowFilter":0,"allowGroup":true,"allowScope":null,"allowSegment":1,"code":"ga:userDefinedValue","containGroupFunction":false,"defaultScope":null,"skipExistCheck":null,"type":"metrics"},"fieldId":"ga:userDefinedValue","id":"ga:userDefinedValue","name":"用户指定的值","skipExistCheck":null,"type":"category","uuid":"157edf42-572a-47be-8dc8-bd6a3b217b53","validateStatus":"1","labelName":null,"calculateType":null,"granularity":null},{"allowFilter":0,"allowGroup":true,"allowScope":null,"allowSegment":1,"code":"ga:sessionCount","containGroupFunction":false,"dataType":"STRING","defaultScope":null,"extra":{"allowFilter":0,"allowGroup":true,"allowScope":null,"allowSegment":1,"code":"ga:sessionCount","containGroupFunction":false,"defaultScope":null,"skipExistCheck":null,"type":"metrics"},"fieldId":"ga:sessionCount","id":"ga:sessionCount","name":"会话次数","skipExistCheck":null,"type":"category","uuid":"7671076c-9955-41e4-83d5-69dccbf4b4fc","validateStatus":"1","labelName":null,"calculateType":null,"granularity":null},{"alias":"user_alias","allowFilter":0,"allowGroup":false,"allowScope":null,"allowSegment":1,"code":"ga:newUsers","containGroupFunction":false,"dataType":"INTEGER","defaultScope":null,"extra":{"allowFilter":0,"allowGroup":false,"allowScope":null,"allowSegment":1,"code":"ga:newUsers","containGroupFunction":false,"defaultScope":null,"skipExistCheck":null,"type":"metrics"},"fieldId":"ga:newUsers","id":"ga:newUsers","name":"新用户","skipExistCheck":null,"type":"yAxis","uuid":"1c8cae01-280c-49e6-bb05-c5ea2f5c1adb","validateStatus":"1","labelName":null,"calculateType":null,"granularity":null},{"allowFilter":0,"allowGroup":false,"allowScope":null,"allowSegment":0,"code":"ga:users","containGroupFunction":false,"dataType":"INTEGER","defaultScope":null,"extra":{"allowFilter":0,"allowGroup":false,"allowScope":null,"allowSegment":0,"code":"ga:users","containGroupFunction":false,"defaultScope":null,"skipExistCheck":null,"type":"metrics"},"fieldId":"ga:users","id":"ga:users","name":"用户数","skipExistCheck":null,"type":"yAxis","uuid":"4cd78734-5ba4-4da3-8b39-0b9f6fa213fe","validateStatus":"1","labelName":null,"calculateType":null,"granularity":null}],"sort":{"uuid":"7671076c-9955-41e4-83d5-69dccbf4b4fc","order":"asc"},"filters":null,"pteSegments":null,"segment":null,"time":{"field":null,"code":"past","value":"100","isIncludeToday":false},"map":null,"targetValue":null,"settings":{"date":{"visible":false},"total":{"visible":true,"item":"1c8cae01-280c-49e6-bb05-c5ea2f5c1adb"},"maxLimit":{"rows":null},"tableSettings":{"table":{"fontSize":"14px","grid":{"wrap":{"showGrid":true,"gridColor":{"color":"#e9e9e9","type":"theme"}},"col":{"showGrid":true,"gridColor":{"color":"#e9e9e9","type":"theme"}},"row":{"showGrid":true,"gridColor":{"color":"#e9e9e9","type":"theme"}}},"widthOverflow":false,"numberWidth":null},"tableHeader":{"textWrap":false,"fontColor":{"color":"#bbbbbb","type":"theme"},"cellBackgroundColor":{"color":"#ffffff","type":"theme"}},"tableBody":{"fontSize":"14px","showNumber":false,"row":{"textWrap":false,"even":{"fontColor":{"color":"#444444","type":"theme"},"cellBackgroundColor":{"color":"#ffffff","type":"theme"}},"odd":{"fontColor":{"color":"#444444","type":"theme"},"cellBackgroundColor":{"color":"#f9f9f9","type":"theme"}}},"col":{"default":{"fontColor":{"color":"transparent","type":"custom"},"cellBackgroundColor":{"color":"transparent","type":"custom"}},"settings":[]}},"tableFooter":{"showTotal":false,"fontColor":{"color":"#444444","type":"theme"},"cellBackgroundColor":{"color":"#ffffff","type":"theme"}},"pagination":{"showPagination":true,"currentPage":1,"pageLength":10}}},"disconnectMessage":"","isDemo":"0","toolData":{"extend":null},"sourceType":"USER_CREATED","compareWithPrevious":{"compareWithPreviousStatus":false,"autoInsert":true,"comparePeriod":"none","compareDisplay":"","compareFields":[{"allowFilter":0,"allowGroup":false,"allowScope":null,"allowSegment":1,"code":"ga:newUsers","containGroupFunction":false,"dataType":"INTEGER","defaultScope":null,"extra":{"allowFilter":0,"allowGroup":false,"allowScope":null,"allowSegment":1,"code":"ga:newUsers","containGroupFunction":false,"defaultScope":null,"skipExistCheck":null,"type":"metrics"},"fieldId":"ga:newUsers","id":"ga:newUsers","name":"新用户","skipExistCheck":null,"type":"yAxis","uuid":"1c8cae01-280c-49e6-bb05-c5ea2f5c1adb","validateStatus":"1","labelName":null,"calculateType":null,"granularity":null},{"allowFilter":0,"allowGroup":false,"allowScope":null,"allowSegment":0,"code":"ga:users","containGroupFunction":false,"dataType":"INTEGER","defaultScope":null,"extra":{"allowFilter":0,"allowGroup":false,"allowScope":null,"allowSegment":0,"code":"ga:users","containGroupFunction":false,"defaultScope":null,"skipExistCheck":null,"type":"metrics"},"fieldId":"ga:users","id":"ga:users","name":"用户数","skipExistCheck":null,"type":"yAxis","uuid":"4cd78734-5ba4-4da3-8b39-0b9f6fa213fe","validateStatus":"1","labelName":null,"calculateType":null,"granularity":null}]},"widgetTemplateConfig":""}
    """
    preview_data_req_headers = {'UID': '1001592', 'SpaceId': 'c7ecdc29-bcd9-404c-80b6-a1a32329b93e', 'TraceId':'dummy', 'Token':'bingxing.kang@ptmind.com:12dc8f3e-67b8-44af-9ef3-331456d80fc8:prod'}

    j_body = json.loads(preview_data_req_body)
    resp = test_client.post('/api/v1/widgets/data/preview', json=j_body, headers={})
    assert resp.status_code == 200
    j = resp.json
    rows = j['data']['data'][0]['rows']
    assert len(rows) == 3
    assert rows[0][2] == 'user_alias'
    assert rows[1] == [1, "a", 2, 3]

    import copy
    for code in ['today', 'this_month', 'this_month', 'this_year', 'yesterday', 'last_week', 'last_month', 'last_year', 'tomorrow', 'next_week', 'next_month', 'next_year', 'next', 'custom_today', 'custom']:
        j_body_new = copy.deepcopy(j_body)
        j_body_new['time']['code'] = code

        if code == 'custom_today':
            j_body_new['time']['value'] = '2018/01/01'
        elif code == 'custom':
            j_body_new['time']['value'] = '2018/01/01|2019/01/01'

        resp = test_client.post('/api/v1/widgets/data/preview', json=j_body_new, headers={})
        assert resp.status_code == 200


def test_colorby():

    data = {'data':[[5,3,2], [2,None,2], [3,2,3], [4,6,5], [4,8,5]],
            'summaryValues': [None, 24, 1],
            'header': [{'id': 'ga:date', 'uuid': '38d23df0-7796-4a10-9649-1f3648000999'},
                       {'id': 'ga:users', 'uuid': '4e635f12-fa29-4ebb-8f9f-450c9e03f951'},
                       {'id': 'ga:language', 'uuid': 'b89153ef-eb13-432f-93aa-2bfb50991088'}]}

    request = '''
    {
    "widgetId":null,
    "panelId": "38d23df0-7796-4a10-9649-1f3648000999",
    "name": "test",
    "graphType": "column",
    "sort": {
        "uuid": "38d23df0-7796-4a10-9649-1f3648000999",
        "order": "asc"
    },
    "filters": [],
    "pteSegments": null,
    "segment": null,
    "time": {
        "field": null,
        "code": "past",
        "value": 30,
        "isIncludeToday": false
    },

    "fields": [{
        "allowFilter": 1,
        "allowGroup": true,
        "allowScope": null,
        "allowSegment": 1,
        "code": "ga:date",
        "containGroupFunction": false,
        "dataType": "DATE",
        "defaultScope": null,
        "fieldId": "ga:date",
        "id": "ga:date",
        "name": "Date",
        "skipExistCheck": null,
        "type": "xAxis",
        "uuid": "38d23df0-7796-4a10-9649-1f3648000999",
        "validateStatus": "1",
        "labelName": null,
        "calculateType": null,
        "granularity": null
    },
    {
        "id": "ga:users",
        "uuid": "4e635f12-fa29-4ebb-8f9f-450c9e03f951",
        "fieldId": "ga:users",
        "name": "Users",
        "dataType": "INTEGER",
        "calculateType": null,
        "dataFormat": null,
        "validateStatus": "1",
        "columnType": null,
		"alias": "user_alias",
        "granularity": null,
        "type": "yAxis",
        "labelName": null,
        "analysisFunctionType": null,
        "dataScope": null,
        "showName": "Users"
    },
    {
        "allowFilter": 1,
        "allowGroup": true,
        "allowScope": null,
        "allowSegment": 1,
        "code": "ga:language",
        "containGroupFunction": false,
        "dataType": "STRING",
        "defaultScope": null,
        "fieldId": "ga:language",
        "id": "ga:language",
        "name": "Language",
        "skipExistCheck": null,
        "type": "legend",
        "uuid": "b89153ef-eb13-432f-93aa-2bfb50991088",
        "validateStatus": "1",
        "labelName": null,
        "calculateType": null,
        "granularity": null
    }],
    "settings": {
        "maxLimit": {
            "bars": 1000,
            "barsIsChange": false,
            "series": 2
        }
    }
}

    '''

    dataAdapter = DataAdaptor(data, json.loads(request), locale='en_US')
    result = dataAdapter.collect()

    print (json.dumps(result))

    assert result['metricsAmountsMap']['4e635f12-fa29-4ebb-8f9f-450c9e03f951']['showName'] == 'user_alias'
    series_data = result['data']
    assert len(series_data) == 2

    assert series_data[0]['variableName'] == 5
    assert series_data[0]['rows'] == [[4,6], [4,8]]
    assert series_data[0]['metricsName'] == 'user_alias'
    assert series_data[0]['totals'] == {}

    assert series_data[1]['variableName'] == 2
    assert series_data[1]['rows'] == [[5,3], [2,None]]
    assert series_data[0]['metricsName'] == 'user_alias'
    assert series_data[0]['totals'] == {}

    category = dataAdapter._get_category()
    assert category == [5,2,3,4]


def test_limit():
    data = {'data':[['1',3], ['2', None], ['3',4], ['4',None], ['4',8]],
            'summaryValues': [None, 24, 1],
            'header': [{'id': 'ga:date', 'uuid': '38d23df0-7796-4a10-9649-1f3648000999'},
                       {'id': 'ga:users', 'uuid': '4e635f12-fa29-4ebb-8f9f-450c9e03f951'}]}
    request = '''
       {
    "widgetId":null,
    "panelId": "38d23df0-7796-4a10-9649-1f3648000999",
    "name": "test",
    "graphType": "column",
    "sort": {
        "uuid": "38d23df0-7796-4a10-9649-1f3648000999",
        "order": "asc"
    },
    "filters": [],
    "pteSegments": null,
    "segment": null,
    "time": {
        "field": null,
        "code": "past",
        "value": 30,
        "isIncludeToday": false
    },

    "fields": [{
        "dataType": "DATE",
        "fieldId": "ga:date",
        "id": "ga:date",
        "name": "Date",
        "type": "xAxis",
        "uuid": "38d23df0-7796-4a10-9649-1f3648000999"
    },
    {
        "id": "ga:users",
        "uuid": "4e635f12-fa29-4ebb-8f9f-450c9e03f951",
        "fieldId": "ga:users",
        "name": "Users",
        "dataType": "INTEGER",
        "type": "yAxis"
    }],
    "settings": {
        "maxLimit": {
            "bars": 2,
            "barsIsChange": false,
            "series": 2
        },
        "showOther":
        {
           "visible": true
        }
    }
}
    '''
    dataAdapter = DataAdaptor(data, json.loads(request), locale='en_US')
    result = dataAdapter.collect()
    assert result['categories'] == ['1','2','Others']
    assert result['data'][0]['rows'] == [['1', 3], ['2', None], ['Others', 12]]



def test_export():
    widget = '''
    {
	"fields": [{
		"alias": "date_alias",
		"name": "Date",
		"type": "xAxis",
		"uuid": "3dea4da2-d02a-4722-87d0-b349aef19d8f"
	},
	{
		"alias": "user_alias",
		"name": "Users",
		"type": "yAxis",
		"uuid": "05d9a94d-424c-46e1-9d63-a30b0afb4bbd"
	},
	{
		"alias": null,
		"name": "User Type",
		"type": "legend",
		"uuid": "2abb7f0f-3cb7-4d71-9103-db3191c01c35"
	}],
	"graphType": "column",
        "compareWithPreviousPeriod":{}
    }
    '''

    original_data = '''
    {
	"availableDatePeriod": [],
	"categories": ["2019-02-20",
	"2019-02-21",
	"2019-02-22",
	"Others"],
	"data": [{
		"dataTypeMap": {
			"05d9a94d-424c-46e1-9d63-a30b0afb4bbd": "INTEGER",
			"05d9a94d-424c-46e1-9d63-a30b0afb4bbd(2)": "PERCENT",
			"2abb7f0f-3cb7-4d71-9103-db3191c01c35": "STRING",
			"2abb7f0f-3cb7-4d71-9103-db3191c01c35(2)": "PERCENT",
			"ae7632aa-3414-4ce9-8256-0ee720bc63b0": "DATETIME"
		},
        "metricsKey": "05d9a94d-424c-46e1-9d63-a30b0afb4bbd",
        "metricsSign": "Returning Visitor",
        "dimensionsId": "Returning Visitor",
		"orderColumn": null,
		"orderRule": null,
		"orderType": null,
		"rows": [["2019-02-20",
		274],
		["2019-02-21",
		242],
		["2019-02-22",
		240],
		["Others",
		5547]],
		"variableName": "Users-Returning Visitor"
	},
	{
        "metricsKey": "05d9a94d-424c-46e1-9d63-a30b0afb4bbd",
		"metricsSign": "New Visitor",
        "dimensionsId": "New Visitor",
		"rows": [["2019-02-20",
		223],
		["2019-02-21",
		115],
		["2019-02-22",
		192],
		["Others",
		3896]]
	},
	{
        "metricsKey": "05d9a94d-424c-46e1-9d63-a30b0afb4bbd(2)",
		"metricsSign": "Returning Visitor",
        "dimensionsId": "Returning Visitor",
		"rows": [["2019-02-20",
		20.7],
		["2019-02-21",
		-0.41],
		["2019-02-22",
		-0.41],
		["Others",
		2761.8399999999997]]
	},
	{
        "metricsKey": "05d9a94d-424c-46e1-9d63-a30b0afb4bbd(2)",
		"metricsSign": "New Visitor",
        "dimensionsId": "New Visitor",
		"rows": [["2019-02-20",
		82.79],
		["2019-02-21",
		-28.12],
		["2019-02-22",
		24.68],
		["Others",
		2032.8299999999997]]
	}],
	"graphType": "column",
	"metricsAmountsMap": {
		"05d9a94d-424c-46e1-9d63-a30b0afb4bbd": {
			"code": "ga:users",
			"dataFormat": null,
			"dataType": "INTEGER",
			"id": 1,
			"invalid": false,
			"key": "05d9a94d-424c-46e1-9d63-a30b0afb4bbd",
			"name": "Users",
			"showName": "user_alias",
			"unit": "",
			"value": null
		},
		"05d9a94d-424c-46e1-9d63-a30b0afb4bbd(2)": {
			"code": "ga:users(2)",
			"dataFormat": null,
			"dataType": "PERCENT",
			"id": 2,
			"invalid": false,
			"key": "05d9a94d-424c-46e1-9d63-a30b0afb4bbd(2)",
			"name": "Users - % Growth",
			"showName": "user_alias - % Growth",
			"unit": "",
			"value": null
		}
	}
    }
    '''

    result = widget_export_data(json.loads(widget), json.loads(original_data))

    data = result['data'][0]
    rows = data['rows']

    assert len(rows) == 9
    assert rows[0] == ["date_alias", "User Type", "user_alias", "user_alias - % Growth"]
    assert rows[4] == ["Others", "Returning Visitor", 5547, 2761.8399999999997]
    assert rows[7] == ["2019-02-22", "New Visitor", 192, 24.68]

    assert data['metricsKey'] == '05d9a94d-424c-46e1-9d63-a30b0afb4bbd,05d9a94d-424c-46e1-9d63-a30b0afb4bbd(2)'
    assert data['dimensionsKey'] == '3dea4da2-d02a-4722-87d0-b349aef19d8f,2abb7f0f-3cb7-4d71-9103-db3191c01c35'


def test_comparsion():
    data = '''
	{
    "header": [{
		"id": "ga:date",
		"type": "date",
		"dataFormat": "day",
		"groupBy": true,
		"uuid": "3dea4da2-d02a-4722-87d0-b349aef19d8f"
	},
	{
		"id": "ga:users",
		"type": "number",
		"uuid": "78617ce1-e133-47fd-8903-971dd4e545c9"
	},
	{
		"id": "ga:users",
		"type": "number",
		"uuid": "78617ce1-e133-47fd-8903-971dd4e545c9:cwp",
		"dataFormat": "percentage"
	}],
	"data": [["2019-03-14",
	429,
	12.3],
	["2019-03-15",
	553,
	20.48],
	["2019-03-16",
	165,
	-61.54],
	["2019-03-17",
	114,
	-40.93],
	["2019-03-18",
	383,
	241.96],
	["2019-03-19",
	410,
	0.24],
	["2019-03-20",
	374,
	-18.16],
	["2019-03-21",
	335,
	-17.89]],
	"summaryValues": [null,
	1759.0,
	null],
    "extra_info": {
    "cwp_date_range": {
    "start": 0,
    "end": 1000
    }
    }}
    '''

    request = '''
    {
	"children": null,
	"commentCount": null,
	"compareWithPreviousPeriod": {
		"autoInsert": true,
		"compareDisplay": "growRate",
		"compareFields": [{
			"alias": null,
			"analysisFunctionType": null,
			"calculateType": null,
			"columnType": null,
			"dataFormat": null,
			"dataScope": null,
			"dataType": "INTEGER",
            "extra": {
				"allowAggregation": true,
				"allowFilter": 1,
				"allowGroup": false,
				"allowSegment": 0,
				"code": "ga:users",
				"containGroupFunction": false,
				"type": "metrics"
			},
			"fieldId": "ga:users",
			"granularity": null,
			"graphAxis": null,
			"id": "ga:users",
			"labelName": null,
			"name": "Users",
			"showName": "Users",
			"type": "yAxis",
			"uuid": "78617ce1-e133-47fd-8903-971dd4e545c9",
			"validateStatus": "1"
		}],
		"comparePeriod": "compareWithPreviousPeriod",
		"compareWithPreviousPeriodStatus": true
	},
	"fields": [{
		"alias": "date_alias",
		"analysisFunctionType": "none",
		"calculateType": null,
		"columnType": null,
		"dataFormat": "day",
		"dataScope": "session",
		"dataType": "DATETIME",
		"extra": {
			"allowFilter": 1,
			"allowGroup": true,
			"allowSegment": 0,
			"code": "ga:date",
			"containGroupFunction": false,
			"type": "dimension"
		},
		"fieldId": "ga:date",
		"granularity": null,
		"graphAxis": null,
		"id": "ga:date",
		"labelName": null,
		"name": "Date",
		"showName": "date_alias",
		"type": "xAxis",
		"uuid": "3dea4da2-d02a-4722-87d0-b349aef19d8f",
		"validateStatus": "1"
	},
	{
		"alias": null,
		"analysisFunctionType": null,
		"calculateType": null,
		"columnType": null,
		"dataFormat": null,
		"dataScope": null,
		"dataType": "INTEGER",
        "extra": {
				"allowAggregation": true,
				"allowFilter": 1,
				"allowGroup": false,
				"allowSegment": 0,
				"code": "ga:users",
				"containGroupFunction": false,
				"type": "metrics"
			},
		"fieldId": "ga:users",
		"granularity": null,
		"graphAxis": null,
		"id": "ga:users",
		"labelName": null,
		"name": "Users",
		"showName": "Users",
		"type": "yAxis",
		"uuid": "78617ce1-e133-47fd-8903-971dd4e545c9",
		"validateStatus": "1"
	}],
	"filters": [],
	"graphType": "column",
	"widgetId": "baf53a03-8616-48c0-92a2-c7846679f1a4"
    }
    '''

    dataAdapter = DataAdaptor(json.loads(data), json.loads(request), locale='en_US')
    result = dataAdapter.collect()
    assert result['data'][0]['rows'] == [['2019-03-14', 429], ['2019-03-15', 553], ['2019-03-16', 165], ['2019-03-17', 114], ['2019-03-18', 383], ['2019-03-19', 410], ['2019-03-20', 374], ['2019-03-21', 335]]
    assert result['data'][1]['rows'] == [['2019-03-14', 12.3, '2019-03-13'], ['2019-03-15', 20.48, '2019-03-14'], ['2019-03-16', -61.54, '2019-03-15'], ['2019-03-17', -40.93, '2019-03-16'], ['2019-03-18', 241.96, '2019-03-17'], ['2019-03-19', 0.24, '2019-03-18'], ['2019-03-20', -18.16, '2019-03-19'], ['2019-03-21', -17.89, '2019-03-20']]




def test_global_filter():

    data = '''
    {
	"header": [{
		"id": "ga:date",
		"type": "date",
		"dataFormat": "day",
		"groupBy": true,
		"uuid": "6b2683b9-e444-4dea-9544-d03a391a9d49"
	},
	{
		"id": "ga:users",
		"type": "number",
		"uuid": "a8ee2355-ae00-4cc1-a846-441006390f00"
	}],
	"data": [["2019-03-15",
	553]],
	"summaryValues": [null,
	2772.0]
    }
    '''
    request = '''
    {
        "widgetId": "1af38c2e-80bc-4c5d-9443-61c8e26296f9",
        "global_filter": true,
        "global_time": true,
        "fields": [{
            "id": "ga:date",
            "uuid": "6b2683b9-e444-4dea-9544-d03a391a9d49",
            "fieldId": "ga:date",
            "name": "Date",
            "dataType": "DATETIME"
        },
        {
            "id": "ga:users",
            "uuid": "a8ee2355-ae00-4cc1-a846-441006390f00",
            "fieldId": "ga:users",
            "name": "Users",
            "dataType": "INTEGER"
        }],
        "panelFilterComponents": [{
            "componentId": "7854aa6c-6a89-4fd1-883d-f85b58ebc46f",
            "panelId": "de92fae8-c5d7-4bdf-a9c5-a75d497886de",
            "code": "GLOBAL_FILTER",
            "name": "Users(Greater than 10)",
            "settings": {}
        },
        {
            "componentId": "7bf16aa1-7d11-475b-a626-ddb5c4fa8c0a",
            "panelId": "de92fae8-c5d7-4bdf-a9c5-a75d497886de",
            "code": "GLOBAL_FILTER",
            "name": "Users(Greater than 100)",
            "settings": {}
        }],
        "panelTimeComponent": {
            "switch": "1",
            "isChange": true,
            "settings": {
                "code": "past",
                "value": "15",
                "isIncludeToday": false
            },
            "name": "Last 15 days",
            "code": "GLOBAL_TIME"
        }
    }

    '''

    dataAdapter = DataAdaptor(json.loads(data), json.loads(request), locale='en_US')
    panel_components = dataAdapter.get_pannel_components()

    assert len(panel_components) == 3


    drill_down_request = '''
    {
        "widgetId": "1af38c2e-80bc-4c5d-9443-61c8e26296f9",
        "global_filter": true,
        "global_time": true,
        "fields": [{
            "id": "ga:date",
            "uuid": "6b2683b9-e444-4dea-9544-d03a391a9d49",
            "fieldId": "ga:date",
            "name": "Date",
            "dataType": "DATETIME"
        },
        {
            "id": "ga:users",
            "uuid": "a8ee2355-ae00-4cc1-a846-441006390f00",
            "fieldId": "ga:users",
            "name": "Users",
            "dataType": "INTEGER"
        }],
        "panelFilterComponents": [],
        "panelTimeComponent": {
            "switch": "1",
            "isChange": true,
            "settings": {
                "code": "past",
                "value": "15",
                "isIncludeToday": false
            },
            "name": "Last 15 days",
            "code": "GLOBAL_TIME"
        }
    }
    '''
    dataAdapter = DataAdaptor(json.loads(data), json.loads(drill_down_request), locale='en_US')
    panel_components = dataAdapter.get_pannel_components()

    assert len(panel_components) == 1
