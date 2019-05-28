import re
import requests_mock


DOWNSTREAM_BUSINESS_HOST = "http://datadeck-business:9081/api/v1"
DOWNSTREAM_V2_HOST = "https://middlev2.datadeck.com/"
DOWNSTREAM_DATAMANAGER_HOST = "http://datadeck-data-manager:9082/api/v1"


v2_connections_resp = {
    "data": {
        "ds": [],
        "serviceDsList": []
    },
    "success": True
}

v2_list_resp = {
    "data": [],
    "success": True
}

v2_user_info_resp = {
    "status": "success",
    "message": "",
    "content": {
        "ptId": "3897",
        "userName": "123",
        "weekStart": "monday",
        "locale": "en_US",
        "userEmail": "chen.chen@ptmind.com"
    },
    "dataVersion": None,
    "code": None
}

resp_datasource_info_ga_v4 = {
    'id': '423749823749', 'code': 'googleanalytics-v4', 'name': 'googleanalytics-v4',
    'description': 'googleanalytics-v4', 'api_version': 'v4', 'published': True,
    'config': "{'auth': {'type': 'oauth'}, 'data': {'dateRange': "
              "{'supportDateRangeFieldSelection': False}, 'provideRawData': False, "
              "'supportPaging': True}, 'general': {'author': 'yiming.cao@ptmind.com', "
              "'code': 'googleanalytics-v4', 'id': 1001, 'name': "
              "'Google Analytics (API v4 Beta)', 'schemaVersion': '0.9.0', 'version': 0.9}, "
              "'hierarchy': {'items': {'matchLevels': '*', 'name': 'Profile'}}}"
}

resp_connections = [
    {'id': 'aad1ea87-1576-11e9-9d60-1002b5d9f459',
     'dm_connection_id': 'xxx',
     'user_id': '123',
     'space_id': 's123',
     'ds_code': 'googleanalytics-v4',
     'name': 'googleanalytics-v4',
     'created_at': '123123123'
     }
]

resp_datasources = [
    {'id': '423749823749', 'code': 'googleanalytics-v4',
     'name': 'googleanalytics-v4', 'description': 'googleanalytics-v4',
     'api_version': 'v4', 'published': True, 'ds_id': 1001, 'type': 'api'},
    {'id': '423749823750', 'code': 'redshift',
     'name': 'redshift', 'description': 'redshift',
     'api_version': 'v4', 'published': True, 'ds_id': 1002, 'type': 'db'},

]


@requests_mock.Mocker(kw='mock')
def connections_and_ds_list(test_client, **kwargs):
    matcher0 = re.compile(DOWNSTREAM_V2_HOST + "api/v2/users/signinValidate")
    matcher1 = re.compile(DOWNSTREAM_V2_HOST + "api/v3/ds/connections")
    matcher2 = re.compile(DOWNSTREAM_V2_HOST + "api/v3/ds/list")
    matcher3 = re.compile(DOWNSTREAM_V2_HOST + "users/shareUserInfo")

    # mock token check
    kwargs['mock'].get(matcher0,
                       json={"success": True})

    # mock datasources api
    kwargs['mock'].get(f"{DOWNSTREAM_DATAMANAGER_HOST}/datasources",
                       json=resp_datasources)

    for ds in resp_datasources:
        ds_code = ds['code']
        kwargs['mock'].get(f"{DOWNSTREAM_DATAMANAGER_HOST}/datasources/{ds_code}",
                           json={})

    # mock v2 /connections api
    kwargs['mock'].get(matcher1,
                       json=v2_connections_resp)

    # mock v2 /user api

    # mock v2 /datasources api
    kwargs['mock'].get(matcher2,
                       json=v2_list_resp)

    # mock v2 /user info api
    kwargs['mock'].get(matcher3,
                       json=v2_list_resp)

    # mock business /connections api
    kwargs['mock'].get(f"{DOWNSTREAM_BUSINESS_HOST}/connections",
                       json=resp_connections)

    # mock data-manager /datasources/googleanalytics-v4
    kwargs['mock'].get(f"{DOWNSTREAM_DATAMANAGER_HOST}/datasources/googleanalytics-v4",
                       json=resp_datasource_info_ga_v4)

    kwargs['mock'].get("https://middlev2.datadeck.com/api/v2/users?TraceId=1234567", json={
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

    r_c = test_client.get("/api/v3/ds/connections",
                          headers={
                              "Token": "bingxing.kang@ptmind.com:eeb30f01-4434-4e61-b94a-1ce67c2e2502:prod",
                              "UID": "1001592",
                              "SpaceId": "c7ecdc29-bcd9-404c-80b6-a1a32329b93e",
                              "TraceId": "1234567"
                          })

    r_l = test_client.get("/api/v3/ds/list",
                          headers={
                              "Token": "bingxing.kang@ptmind.com:eeb30f01-4434-4e61-b94a-1ce67c2e2502:prod",
                              "UID": "1001592",
                              "SpaceId": "c7ecdc29-bcd9-404c-80b6-a1a32329b93e",
                              "TraceId": "1234567"
                          })

    assert r_c.status_code == 200, "/connections failed"
    assert r_l.status_code == 200, "/ds-list failed"

    ds_list = r_l.json['data']['ds']
    assert len(ds_list) > 0

    flag = False
    for ds in ds_list:
        if ds['dataSourceCode'] == 'googleanalytics-v4':
            if ds['connectionCount'] > 0:
                flag = True

    assert flag, "cannot find vnext ds ga, Or ga connection number is not right!"
