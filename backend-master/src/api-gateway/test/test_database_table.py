import requests_mock

DOWNSTREAM_BUSINESS_HOST = "http://datadeck-business:9081/api/v1"
DOWNSTREAM_V2_HOST = "https://middlev2.datadeck.com"

common_headers = {'UID': '123', 'SpaceId': '123', 'TraceId':'dummy', 'Token':'test-token'}


def common_mock(mock):
    mock.get(DOWNSTREAM_V2_HOST + "/api/v2/users/signinValidate", json={"success": True})
    mock.get(DOWNSTREAM_V2_HOST + "/api/v2/spaces",
             json={'success': True, 'data': {'weekStart': 'monday'}})
    mock.get(DOWNSTREAM_BUSINESS_HOST + "/datasources",
             json=[
                {'id': '1', 'code': 'redshift-vnext', 'ds_id': 123, 'name': 'Redshift'}
             ])


@requests_mock.Mocker(kw='mock')
def test_add_table_from(test_client, **kwargs):
    common_mock(kwargs['mock'])
    resp = test_client.get('/api/v3/ds/addTable/redshift-vnext/from', headers=common_headers)
    assert resp.status_code == 200
    j = resp.json
    assert j['success'] is True
    assert j['data']['itemList']


@requests_mock.Mocker(kw='mock')
def test_get_connection_databases(test_client, **kwargs):
    common_mock(kwargs['mock'])
    kwargs['mock'].get(DOWNSTREAM_BUSINESS_HOST + "/connections/abc",
                       json={})
    kwargs['mock'].post(DOWNSTREAM_BUSINESS_HOST + "/connections/abc/hierarchy",
                       json={'items': [
                           {'id': '1', 'name': 'Foo'}
                       ]})
    resp = test_client.get('/api/v3/ds/getDataSourceAccountSchema/abc/ptoneRootFolderID::connection', headers=common_headers)
    assert resp.status_code == 200
    j = resp.json
    assert j['success'] is True
    assert j['data'][0]['name'] == 'Foo'


@requests_mock.Mocker(kw='mock')
def test_get_connection_database_tables(test_client, **kwargs):
    common_mock(kwargs['mock'])
    kwargs['mock'].get(DOWNSTREAM_BUSINESS_HOST + "/connections/abc",
                       json={})
    kwargs['mock'].post(DOWNSTREAM_BUSINESS_HOST + "/connections/abc/hierarchy",
                       json={'items': [
                           {'id': '1', 'name': 'Foo'}
                       ]})
    resp = test_client.get('/api/v3/ds/getDataSourceAccountSchema/abc/mydb', headers=common_headers)
    assert resp.status_code == 200
    j = resp.json
    assert j['success'] is True
    assert j['data'][0]['name'] == 'Foo'


@requests_mock.Mocker(kw='mock')
def test_table_preview(test_client, **kwargs):
    common_mock(kwargs['mock'])
    kwargs['mock'].get(DOWNSTREAM_BUSINESS_HOST + "/datasources/redshift-vnext",
                       json={'ds_id': '1000'})
    kwargs['mock'].get(DOWNSTREAM_BUSINESS_HOST + "/connections/abc",
                       json={'ds_code': 'redshift-vnext'})
    kwargs['mock'].post(DOWNSTREAM_BUSINESS_HOST + "/connections/abc/hierarchy",
                       json={'items': [
                           {'id': '1', 'name': 'Foo'}
                       ]})

    kwargs['mock'].post(DOWNSTREAM_BUSINESS_HOST + "/connections/abc/table_preview_data",
                       json={'fields': [
                           {'id': 'f1', 'name': 'Field1', 'type': 'number'}
                       ], 'data': [
                           [1]
                       ]})

    resp = test_client.post('/api/v3/ds/pullRemoteData',
                            json={
                                'instanceId': 'abc',
                                'tableId': 'table1',
                                'dataBaseName': 'db1'
                            },
                            headers=common_headers)
    assert resp.status_code == 200
    j = resp.json
    assert j['success'] is True
    assert j['data']['data'][0][0] == 'f1'
    assert j['data']['data'][1][0] == 1
    assert j['data']['name'] == 'table1'


@requests_mock.Mocker(kw='mock')
def test_save_table_definition(test_client, **kwargs):
    common_mock(kwargs['mock'])
    kwargs['mock'].get(DOWNSTREAM_BUSINESS_HOST + "/datasources/redshift-vnext",
                       json={'ds_id': '1000'})
    kwargs['mock'].get(DOWNSTREAM_BUSINESS_HOST + "/connections/abc",
                       json={'ds_code': 'redshift-vnext'})
    kwargs['mock'].post(DOWNSTREAM_BUSINESS_HOST + "/connections/abc/hierarchy",
                       json={'items': [
                           {'id': '1', 'name': 'Foo'}
                       ]})
    kwargs['mock'].post(DOWNSTREAM_BUSINESS_HOST + "/connections/abc/tables",
                       json={'connection_id': 'abc',
                             'name': 'Table1',
                             'columns': []})

    resp = test_client.post('/api/v3/ds/saveDataSource',
                            json={
                                'connectionId': 'abc',
                                'table': {
                                    'tableName': 'Table1',
                                    'columns': [
                                        {'code': 'c1', 'name': 'Column1', 'columnType': 'NUMBER'}
                                    ]
                                },
                                'dataBaseName': 'db1'
                            },
                            headers=common_headers)
    assert resp.status_code == 200
    j = resp.json
    assert j['success'] is True


@requests_mock.Mocker(kw='mock')
def test_get_table_definition(test_client, **kwargs):
    common_mock(kwargs['mock'])
    kwargs['mock'].get(DOWNSTREAM_BUSINESS_HOST + "/datasources/redshift-vnext",
                       json={'ds_id': '1000'})
    kwargs['mock'].get(DOWNSTREAM_BUSINESS_HOST + "/connections/abc",
                       json={'ds_code': 'redshift-vnext'})
    kwargs['mock'].post(DOWNSTREAM_BUSINESS_HOST + "/connections/abc/hierarchy",
                       json={'items': [
                           {'id': '1', 'name': 'Foo'}
                       ]})
    kwargs['mock'].get(DOWNSTREAM_BUSINESS_HOST + "/connections/abc/tables/1",
                       json={'connection_id': 'abc',
                             'id': '1',
                             'name': 'Table1',
                             'database': 'db1',
                             'columns': []})

    kwargs['mock'].post(DOWNSTREAM_BUSINESS_HOST + "/connections/abc/table_preview_data",
                       json={'fields': [
                           {'id': 'f1', 'name': 'Field1', 'type': 'number'}
                       ], 'data': [
                           [1]
                       ]})

    resp = test_client.get('/api/v3/ds/getDataSourceEditView/abc/1',
                            headers=common_headers)
    assert resp.status_code == 200
    j = resp.json
    assert j['success'] is True
