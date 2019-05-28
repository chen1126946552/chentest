import os
import sys
import requests_mock
import json
import yaml

from services import data_service
sys.path.append(os.path.join(os.path.dirname(__file__), '../main'))
DATA_MANAGER_DS_HOST = "http://datadeck-data-manager:9082/api/v1/datasources"
DATA_MANAGER_DM_HOST = "http://datadeck-data-manager:9082/api/v1/connections/"


@requests_mock.Mocker(kw='mock')
def test_create_connection(test_client, **kwargs):
    """test connection adapt to v2"""

    ds_code = 'red-shift'
    # mock to skip 'validation process' in create process
    kwargs['mock'].post(f"{DATA_MANAGER_DS_HOST}/{ds_code}/auth/validate",
                        json={
                            'status': 'ok',
                            'message': 'you passed'
                        })
    # return dm-connection 123456
    kwargs['mock'].post(DATA_MANAGER_DM_HOST,
                        json={
                            "id": "123456",
                            'name': "new dm conn",
                            'ds_code': ds_code,
                            'auth_info': "{'instance_token': '123'}",
                            'account_id': "new dm1"
                        })
    resp_create_business_conn1 = test_client.post(f'/api/v1/connections',
                            json={
                              "account_id": "123",
                              "auth_type": "form",
                              "name": "123",
                              "ds_code": ds_code,
                              "auth_info": "{'token': '123'}",

                              "user_id": "u123",
                              "space_id": "s123"
                            })
    j1 = resp_create_business_conn1.json
    # return dm-connection 654321
    kwargs['mock'].post(DATA_MANAGER_DM_HOST,
                        json={
                            "id": "654321",
                            'name': "new dm conn",
                            'ds_code': ds_code,
                            'auth_info': "{'instance_token': '123'}",
                            'account_id': "new dm2"
                        })
    resp_create_business_conn2 = test_client.post(f'/api/v1/connections',
                            json={
                              "account_id": "123",
                              "auth_type": "form",
                              "name": "123",
                              "ds_code": ds_code,
                              "auth_info": "{'token': '123'}",

                              "user_id": "u123",
                              "space_id": "s123"
                            })
    j2 = resp_create_business_conn2.json

    kwargs['mock'].get("http://local.middle.com:7090/api/v2/users?TraceId=1234567", json={
        "success": True,
        "message": None,
        "stackTrace": None,
        "data": {
            "setting": {
                "gravatar": "0",
                "photo": "hi amigo.jpg",
                "photoType": "custom"
            },
            "userInfo": {
                "ptId": "123456",
                "userEmail": "bingxing@ptmind",
                "userName": "bingxing",

            }
        }
    })
    resp = test_client.get(f'/api/v1/connections', headers={"UID": "u123", "spaceId": "s123", "TraceId": "1234567"})
    j3 = resp.json

    assert len(j3) == 2, 'create two connections failed'


@requests_mock.Mocker(kw='mock')
def test_get_map_data(test_client, **kwargs):

    with open(os.path.join(os.path.dirname(__file__), 'googleanalytics-v4.yml'), 'r') as f:
        config = yaml.load(f)

    kwargs['mock'].get(DATA_MANAGER_DS_HOST + '/googleanalytics-v4',
                       json = {
                           'code': 'googleanalytics-v4',
                           'name': 'GA-V4',
                           'config': config
                       })

    ds_code = 'googleanalytics-v4'
    request_body = '''
    {
	"weekStartOn": "monday",
	"timezone": "Asia/Hong_Kong",
	"path": ["112670961",
	"UA-112670961-1",
	"168055156"],
	"locale": "en_US",
	"graphType": "map",
	"map": {
		"mapType": "country",
		"geographyField": "52",
		"mapCode": "United States"
	},
	"paging": {
		"size": 10000
	},
	"fields": [{
		"id": "ga:users",
		"type": "number",
		"uuid": "4e635f12-fa29-4ebb-8f9f-450c9e03f951"
	}],
	"calculatedFields": [],
	"seq": ["4e635f12-fa29-4ebb-8f9f-450c9e03f951"],
	"filters": [{
		"field": {
			"id": "ga:userType",
			"type": "string",
			"groupBy": true,
			"uuid": "c073f66a-a979-4552-8388-5b56fd263965"
		},
		"operator": "equal",
		"values": ["New Visitor"]
	}],
	"segment": {

	},
	"sort": {

	},
	"dateRange": {
		"field": null,
		"code": "past",
		"value": 30,
		"isIncludeToday": false
	},
	"compareWithPrevious": {

	},
	"noCache": true
    }
    '''

    request = json.loads(request_body)

    data_service._add_new_map_field(request, ds_code)

    assert len(request['fields']) == 2
    assert request['fields'][0]['id'] == 'ga:region'

    assert len(request['filters']) == 2
    country_filter = request['filters'][1]

    assert country_filter['values'][0] == 'United States'
    assert country_filter['field']['id'] == 'ga:country'