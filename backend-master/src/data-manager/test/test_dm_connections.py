import requests_mock
import json
from uuid import uuid1
from app import create_app, db
from models.connection import ConnectionModel


def test_connection_creation(test_client):

    connection = {
        'name':'dummy',
        'ds_code':'mysql',
        'account_id': 'abc',
        'auth_info': '''{
            "ip":"123",
            "user":"234",
            "password": "567"
            }''',
        'auth_type': 'oauth'
        }

    r = test_client.post(f'api/v1/connections', json=connection)

    print('Get result', r)

    assert r.status_code == 200


@requests_mock.Mocker(kw='mock')
def test_connection_get_data(test_client, **kwargs):
    ds_code = 'gav4'
    connection_id = 'test_connection_get_data'
    kwargs['mock'].get(f'http://datadeck-datasource-{ds_code}:9090/config',
                       json={'auth': {'type': 'oauth'}})
    kwargs['mock'].get(f'http://datadeck-datasource-{ds_code}:9090/auth/callback', json={'token':'dummy', 'id':'dummy', 'name': 'dummy', 'state':'dummy'})
    connection = test_client.get(f'/api/v1/datasources/{ds_code}/auth/callback?code=xxx&state=yyy')
    connection_id = connection.json['id']


def _get_connection(ds_code):
    connection_id = str(uuid1())
    db.session.add(ConnectionModel
        (
        id = connection_id,
        name='dummy',
        ds_code = ds_code,
        account_id = 'dummy',
        auth_type='oauth',
        auth_info= '{"token" : "dummy"}'
        )
    )
    db.session.commit()
    db.session.flush()
    return connection_id


def test_connection_delete(test_client):
    ds_code = 'gav4'
    connection_id = _get_connection(ds_code)

    new_connection = test_client.get(f'/api/v1/connections/{connection_id}')
    print ('New Connection:', new_connection.json)

    assert new_connection.json['id'] == connection_id

    r = test_client.delete(f'/api/v1/connections/{connection_id}')

    connection = ConnectionModel.query.filter_by(id=connection_id).first()

    assert not connection

    deleted_connection = ConnectionModel.query.with_deleted().filter_by(id=connection_id).first()

    assert deleted_connection


@requests_mock.Mocker(kw='mock')
def test_connection_hierarchy(test_client, **kwargs):
    ds_code = 'gav4'
    connection_id = _get_connection(ds_code)
    data_response = '''
    {
        "items": [{
            "id": "string",
            "name": "string",
            "hasChild": false,
            "children": [null]
        }]
    }
    '''
    data_request = '''
        {
            "path": [],
            "expandAll": true
        }

    '''

    kwargs['mock'].post(f'http://datadeck-datasource-{ds_code}:9090/hierarchy', json=json.loads(data_response))

    hierarchy = test_client.post(f'/api/v1/connections/{connection_id}/hierarchy', json=json.loads(data_request))

    print ('hierarchy', hierarchy)

    assert hierarchy.json['items']


@requests_mock.Mocker(kw='mock')
def test_connection_field(test_client, **kwargs):
    ds_code = 'gav4'
    connection_id = _get_connection('gav4')

    data_response = '''
    {
        "items": [{
            "id": "abc",
            "name": "string",
            "type": "string",
            "children": [null]
        }]
    }
    '''
    data_request = '''
        {
            "path": ["112670961","UA-112670961-1", "168055156"]
        }

    '''
    kwargs['mock'].post(f'http://datadeck-datasource-{ds_code}:9090/fields', json=json.loads(data_response))

    fields = test_client.post(f'/api/v1/connections/{connection_id}/fields', json=json.loads(data_request))

    assert fields.json[0]['id'] == 'abc'


@requests_mock.Mocker(kw='mock')
def test_connection_segment(test_client, **kwargs):
    ds_code = 'gav4'
    connection_id = _get_connection('gav4')

    data_response = '''
    {
        "tokenUpdate": {"access_token": "abc"},
        "items": [{
            "id": "abc",
            "name": "segment"
        }]
    }
    '''
    data_request = '''
        {
            "path": ["112670961","UA-112670961-1", "168055156"]
        }

    '''
    kwargs['mock'].post(f'http://datadeck-datasource-{ds_code}:9090/segments', json=json.loads(data_response))

    segment = test_client.post(f'/api/v1/connections/{connection_id}/segments', json=json.loads(data_request))

    assert segment.json[0]['id'] == 'abc'

    connection = ConnectionModel.query.filter_by(id=connection_id).first()

    update_token = json.loads(connection.auth_info)

    assert update_token['access_token'] == 'abc'
