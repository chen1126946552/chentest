import requests_mock

@requests_mock.Mocker(kw='mock')
def test_auth_saas(test_client, **kwargs):
    ds_code = 'gav4'
    kwargs['mock'].get(f'http://datadeck-datasource-{ds_code}:9090/config',
                       json={'auth': {'type': 'oauth'}})
    kwargs['mock'].get(f'http://datadeck-datasource-{ds_code}:9090/auth/callback',
                       json={'token': 'dummy', 'id': 'dummy', 'name': 'dummy', 'state': 'dummy'})

    resp = test_client.get(f'/api/v1/datasources/{ds_code}/auth/callback?code=xxx&state=yyy')
    assert resp.json['name'] == 'dummy'
    assert resp.json['id']


@requests_mock.Mocker(kw='mock')
def test_auth_form(test_client, **kwargs):
    ds_code = 'redshiftv4'
    kwargs['mock'].post(f'http://datadeck-datasource-{ds_code}:9090/auth/validate',
                        json={'status': 'ok', 'message': 'Validation succeeded'})

    resp = test_client.post(f'/api/v1/datasources/{ds_code}/auth/validate', json={'token': '213123'})
    assert resp.json['status'] == "ok"
