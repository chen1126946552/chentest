import os
import re
import sys
import requests_mock

sys.path.append(os.path.join(os.path.dirname(__file__), '../main'))

SAVE_ETL_DATASOURCE_SAMPLE_DATA = {
    "widgetId": None,
    "spaceId":"f5c85a45-acf3-41bd-8586-ffaf087a0831",
    "dsConnectionId": "a39ec199-b999-4ec0-83bc-b2942eef5834",
    "name": "t1",
    "fields": [
        {
            "id": "ga:sessionCount",
            "uuid": "be2f56aa-dae8-48f3-8cec-74fbd6f3efbf",
            "fieldId": "2",
            "name": "会话次数",
            "dataType": "STRING",
            "calculateType": None,
            "dataFormat": None,
            "validateStatus": "1",
            "extra": {
                "allowFilter": 1,
                "containGroupFunction": False,
                "allowScope": 0,
                "allowSegment": 1,
                "skipExistCheck": None,
                "code": "ga:sessionCount",
                "type": "dimension",
                "allowGroup": True,
                "defaultScope": None
            },
            "columnType": None,
            "labelName": None,
            "granularity": None,
            "type": "category"
        },
        {
            "id": "ga:users",
            "uuid": "99306602-991b-40b6-875d-895b8cc13fd2",
            "fieldId": "1",
            "name": "用户数",
            "dataType": "INTEGER",
            "calculateType": None,
            "dataFormat": None,
            "validateStatus": "1",
            "extra": {
                "allowFilter": False,
                "containGroupFunction": False,
                "allowScope": None,
                "allowSegment": 0,
                "skipExistCheck": None,
                "code": "ga:users",
                "type": "metrics",
                "allowGroup": None,
                "defaultScope": None
            },
            "columnType": None,
            "labelName": None,
            "granularity": None,
            "type": "yAxis"
        }
    ],
    "sort": {
        "uuid": "99306602-991b-40b6-875d-895b8cc13fd2",
        "order": "desc"
    },
    "filters": None,
    "pteSegments": None,
    "segment": None,
    "time": {
        "field": None,
        "code": "past",
        "value": "300",
        "isIncludeToday": False
    }
}


def create_etl_datasource(test_client):
    resp = test_client.post(f'/api/v1/etl/datasources', json=SAVE_ETL_DATASOURCE_SAMPLE_DATA)
    return resp.get_json()


def get_by_id(test_client, datasource_id):
    resp = test_client.get(f'/api/v1/etl/datasources/{datasource_id}')
    return resp.get_json()


def custom_matcher(request):
    if "/dataset-service/etl/syncTableInfo/" in request.path_url:
        resp = request.Response()
        resp.status_code = 200
        return resp
    return None


@requests_mock.Mocker(kw='mock')
def test_create_and_get(test_client, **kwargs):
    matcher = re.compile('http://dsgateway.datadeck.com:8020/dataset-service/etl/syncTableInfo/')
    kwargs["mock"].post(matcher, json={"success": True})

    create_result = create_etl_datasource(test_client)
    if not all([create_result, create_result.get("id")]):
        assert False
    restult = get_by_id(test_client, create_result.get("id"))
    if not restult.get("id"):
        assert False
    assert True
