import re
import requests_mock

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

    # mock token check
    kwargs['mock'].get(matcher0,
                       json={"success": True})
    # mock datasources api
    kwargs['mock'].get(f"{DOWNSTREAM_BUSINESS_HOST}/datasources",
                       json=resp_datasources)

    kwargs['mock'].get(f"{DOWNSTREAM_V2_HOST}/api/v1/connections/config/{ds_connection_id}",
                       json={
                           "success": True, "message": None, "stackTrace": None,
                           "data": {
                               "dsConnectionId": "40382bb1-e5e1-4979-bc65-d47623d6c824",
                               "config": [
                                   {"id": 'bc123',
                                    "name": "bingxing.kang@ptmind.com",
                                    "type": "account", "index": 0},

                                   {
                                       "index": 1,
                                       "requestParams":
                                           {"id": "profile",
                                            "params": {
                                                "account.name": "bingxing.kang@ptmind.com",
                                                "account.id": "2b319713-ec09-4f57-a3ba-c0b01050df76"
                                            },
                                            "provider": "googleanalysis"
                                            },
                                       "type": "profile",
                                       "id": '["account1", "profile1"]',
                                       "name": "全部网站数据"
                                   }
                               ],
                               "dsId": 1001,
                               "uid": None,
                               "spaceId": "c9d1953a-6c97-4288-8ec2-208d2c236b76"
                           },
                           "errorCode": None,
                           "params": None
                       })

    kwargs['mock'].post(f"{DOWNSTREAM_BUSINESS_HOST}/connections/bc123/fields", json=[
        {
            "id": "folder1",
            "name": "First Folder",
            "children": [
                {
                    "id": "field1",
                    "name": "First Field",
                    "type": "STRING",
                    "allowFilter": True,
                    "filterOps": [
                        "in_list",
                        "not_in_list",
                        "str_contain",
                        "str_not_contain"
                    ]
                },
                {
                    "id": "field2",
                    "name": "Second Field",
                    "type": "NUMBER",
                    "allowAggregation": True,
                    "aggOps": [
                        "min",
                        "max",
                        "sum",
                        "average"
                    ]
                }
            ]
        }
    ])

    kwargs['mock'].post(f"{DOWNSTREAM_BUSINESS_HOST}/connections/bc123/segments", json=[
        {
            "id": "seg1234",
            "name": "New Users"
        }
    ])

    resp = test_client.get(f'/api/v1/datasources/{ds_connection_id}/fields', headers={
        "Token": "bingxing.kang@ptmind.com:eeb30f01-4434-4e61-b94a-1ce67c2e2502:prod",
        "UID": "1001592",
        "SpaceId": "c7ecdc29-bcd9-404c-80b6-a1a32329b93e",
        "TraceId": "1234567"
    })

    resp2 = test_client.get(f'/api/v1/spaces/12312313/datasources/{ds_connection_id}/segments', headers={
        "Token": "bingxing.kang@ptmind.com:eeb30f01-4434-4e61-b94a-1ce67c2e2502:prod",
        "UID": "1001592",
        "SpaceId": "c7ecdc29-bcd9-404c-80b6-a1a32329b93e",
        "TraceId": "1234567"
    })

    assert resp.status_code == 200
    j = resp.json
    assert j['success']
    assert j['data']['child'][0]['child'][0]['name'] == 'First Field'

    assert resp2.status_code == 200
    j2 = resp2.json
    assert len(j2['data'][0]) == 3, 'fields in segment not right, just 3 name-id-type'
