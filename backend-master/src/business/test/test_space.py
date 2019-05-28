import os
import sys
from app import db
from models.connection import Connection as ConnectionModel
from models.access_rule import AccessRule as AccessRuleModel

sys.path.append(os.path.join(os.path.dirname(__file__), '../main'))


SPACE_ID = '2d1f8a20-3902-4a57-9eff-0ebbdd9941f5'
SHARE_CONNECTION_DATA_1 = {
    "spaceId": SPACE_ID,
    "cid": "5c66708846d7280f05c4bb36",
    "dataSourceCode": "uploadfile",
    "accountInfo": "datatime.xls-Sheet2",
    "members": [
        {
            "roleCode": "read",
            "roleId": "7",
            "shareToUserId": "888",
            "userEmail": "chen@ptthink.com"
        }
    ],
    "shareNote": None,
    "shareToAllOperateType": "add"
}

SHARE_CONNECTION_DATA_2 = {
    "spaceId": SPACE_ID,
    "cid": "5c66708846d7280f05c4bb36",
    "dataSourceCode": "uploadfile",
    "accountInfo": "datatime.xls-Sheet2",
    "members": [
        {
            "roleCode": "read",
            "roleId": "7",
            "shareToUserId": "999",
            "userEmail": "chen_2@ptthink.com"
        }
    ],
    "shareNote": None,
    "shareToAllOperateType": "add"
}
CONN_DATA = {
    'user_id': 777,
    'space_id': SPACE_ID,
    'dm_connection_id': '1f8be97a-30d0-11e9-b092-02acbe9b2cb2',
    'name': 'test',
    'ds_code': 'googleanalytics-v4',
    'id': '5c66708846d7280f05c4bb36',
    'ds_account_id': 'ds_account:id'
}


def create_connection():
    conn = ConnectionModel(**CONN_DATA)
    db.session.add(conn)
    db.session.commit()


def test_connection_transfer(test_client):
    create_connection()
    test_client.post(f'/api/v1/share/connection', json=SHARE_CONNECTION_DATA_1)
    test_client.post(f'/api/v1/share/connection', json=SHARE_CONNECTION_DATA_2)
    test_client.post(f'/api/v1/spaces/resources/transfer', json={
                                                      "oldUid": '888',
                                                      "newUid": '999',
                                                      "spaceId": SPACE_ID
                                                  })
    acc_list = AccessRuleModel.query.filter_by(space_id=SPACE_ID, is_deleted=False).all()
    for acc in acc_list:
        if acc.user_id == 888:
            assert False
    assert True

