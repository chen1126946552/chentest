import os
import sys
import requests_mock
sys.path.append(os.path.join(os.path.dirname(__file__), '../main'))

DATA_MANAGER_DS_HOST = "http://datadeck-data-manager:9082/api/v1/datasources"
DATA_MANAGER_DM_HOST = "http://datadeck-data-manager:9082/api/v1/connections/"


@requests_mock.Mocker(kw='mock')
def test_connection_create(test_client, **kwargs):
    """form auth(connection create) process"""
    ds_code = 'red-shift'
    kwargs['mock'].post(DATA_MANAGER_DM_HOST,
                        json={
                            "id": "123456",
                            'name': "new dm conn",
                            'ds_code': ds_code,
                            'auth_info': "{'instance_token': '123'}",
                            'account_id': 'some-account'
                        })

    kwargs['mock'].post(f"{DATA_MANAGER_DS_HOST}/{ds_code}/auth/validate",
                        json={
                            'status': 'ok',
                            'message': 'you passed'
                        })

    resp = test_client.post(f'/api/v1/connections',
                            json={
                              "account_id": "123",
                              "auth_type": "form",
                              "name": "123",
                              "ds_code": ds_code,
                              "auth_info": "{'token': '123'}",

                              "user_id": "123",
                              "space_id": "s123"
                            })

    assert resp.status_code == 200
    assert resp.json["user_id"] == "123"
    assert resp.json["space_id"] == "s123"
    assert resp.json["id"]


@requests_mock.Mocker(kw='mock')
def test_oauth_saas_process(test_client, **kwargs):
    """saas auth(connection create) process"""
    ds_code = "test"

    url0 = f"{DATA_MANAGER_DS_HOST}/{ds_code}/auth"
    kwargs['mock'].get(url0, json={"oauth_uri": "http://www.google.com", "oauth_state": "s"})

    url1 = f"{DATA_MANAGER_DS_HOST}/{ds_code}/auth/callback?uid=uxyz&spaceId=sxyz"
    kwargs['mock'].get(url1,
                        json={"id": "id", "name": "name", "oauth_state": "s"})



