# import requests_mock


# @requests_mock.Mocker(kw='mock')
# def test_get_connection_accounts(test_client, **kwargs):
#
#     space_id = 'spaceId001'
#     ds_code = 'googleanalytics-v4'
#     r = test_client.get(f'/api/v1/connections/accounts/{space_id}/{ds_code}')
#     print('Get result: %s', r)
#     assert r.status_code == 200


def test_pass():
    assert True
