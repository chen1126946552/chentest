"""All classes/methods/tools to help to adapt to v2 on `CONNECTION`"""

from __future__ import absolute_import

import logging

from flask import current_app as app
from flask import request

from common.http.utils import get_headers, get_json
from services.exception import V2AdaptorError
from utils.system_constant import get_ds_info_by_ds_code

logger = logging.getLogger(__name__)


def get_v2_user_info():
    """Get user info by v2"""
    v2_url = f'{app.config["MIDDLE_URL"]}/api/v2/spaces/users/{request.headers.get("SpaceId")}'
    resp_data = get_json(v2_url, get_headers())
    if resp_data and resp_data.get("success"):
        return resp_data.get("data")
    return []


def connection_result_data_adapt(conns):
    """
    adapt v2 connection list
    Args:
        conns: [list] vx business connections
    Returns: [list] connections to adapt to v2

    """
    space_user_list = get_v2_user_info()

    def parse(connection):
        # get session user
        owner_user_list = list(filter(lambda x: int(x.get("uid")) == int(connection['user_id']),
                                      space_user_list))
        owner_user = owner_user_list[0]
        share_users = [{
            "uid":  connection['user_id'],
            "userEmail": owner_user.get("userEmail"),
            "userName": owner_user.get("userName"),
            "owner": True,
            "role": None,
            "gravatar": owner_user.get("gravatar"),
            "photo": owner_user.get("photo"),
            "photoType": owner_user.get("photoType"),
            "status": owner_user.get("status"),
            "individualShared": None
        }]
        for member in connection.get("share_users"):
            share_user_list = list(filter(lambda x, m=member:
                                          int(x.get("uid")) == int(m.get("user_id")),
                                          space_user_list))

            #TODO: Remove the share user if the user is deleted or removed from current space.
            if not share_user_list:
                continue

            share_user = share_user_list[0]

            share_users.append({
                "uid": member.get("user_id"),
                "userEmail": share_user.get("userEmail"),
                "userName": share_user.get("userName"),
                "owner": False,
                "role": member.get("role"),
                "gravatar": share_user.get("gravatar"),
                "photo": share_user.get("photo"),
                "photoType": share_user.get("photoType"),
                "status": share_user.get("status"),
                "individualShared": None
                })

        ds_info = get_ds_info_by_ds_code(connection['ds_code'])
        auth_type = 'oauth'
        ds_id = None
        if ds_info:
            if ds_info.get('config') and ds_info['config'].get('auth'):
                auth_type = ds_info['config']['auth'].get('type')
            ds_id = ds_info.get('ds_id')
        else:
            logger.error('Unable to get datasource info for %s', connection['ds_code'])
            ds_id = None

        result = {
            # vnext fields
            "id": connection['id'],
            "accountInfo": connection['name'],
            "connectionTime": connection['created_at'],
            "dataSourceCode": connection['ds_code'],
            "instanceId": connection['id'],

            # v2 fields with fake data
            "authType": auth_type,
            "dataSetCount": 0,
            "userName": owner_user.get("userName"),
            "widgetCount": 0,
            "type": connection['ds_code'],
            "isDataSet": False,
            "dataBaseName": None,
            "shareConnection": bool(connection.get("share_connection")),
            "shareUsers": share_users,
            "lastSyncTime": None,
            "dataSyncStatusValue": 0,
            "lastDataSyncErrorMessage": None,
            "isDismiss": False,
            "isShareToAll": str(int(connection.get("share_to_all"))),
            "shareToAllRoleId": None,
            "shareToAllRoleCode":
                connection.get("share_to_all_access_level")
                if bool(connection.get("share_to_all_access_level"))
                else None
        }

        # include tables under the connection
        tables = []
        for table_def in connection.get('tables', []):
            table = {
                'id': table_def['id'],
                'accountInfo': table_def['name'],
                'accountName': connection['name'],
                'connectionId': connection['id'],
                'connectionTime': table_def['created_at'],
                'createTime': table_def['created_at'],
                'creatorId': connection['user_id'],
                'dataBaseName': table_def['database'],
                'dataSetCount': 0,
                'dataSourceCode': connection['ds_code'],
                'dataSyncStatusValue': 0,
                'dataTimezone': None,
                'dsCode': connection['ds_code'],
                'dsId': ds_id,
                'fileId': table_def['name'],
                'folderId': table_def['database'],
                'name': table_def['name'],
                'remotePath': f'{table_def["database"]}@#*{table_def["name"]}',
                'tableId': table_def['name'],
                'shareUsers': [{
                    # TODO: fetch table share users
                    "uid":  connection['user_id'],
                    "userEmail": owner_user.get("userEmail"),
                    "userName": owner_user.get("userName"),
                    "owner": True,
                    "role": None,
                    "gravatar": owner_user.get("gravatar"),
                    "photo": owner_user.get("photo"),
                    "photoType": owner_user.get("photoType"),
                    "status": owner_user.get("status"),
                    "individualShared": None
                }]
            }
            tables.append(table)

        result['tables'] = tables

        return result

    return [parse(c) for c in conns]


def connection_account_data_adapt(conns):
    """
     Assembly account info
    Args:
        conns:

    Returns: connection account list

    """

    def assembly(account_list):
        return {
            "success": True,
            "data": {
                "dataType": 'list',
                "isNeedTranslateI18nCode": False,
                "isOnlyTranslateName": False,
                "value": account_list
            }
        }

    def parse(conn):
        return {
            "displayName": conn["name"],
            "id": conn["id"],
            "instanceId": conn["id"],
            "name": conn["name"],
            "ownerId": conn["user_id"],
            "ownerName": conn["user_id"],
            "uid": conn["user_id"],
        }

    try:
        account_list = []
        if isinstance(conns, list):
            for conn in conns:
                account_list.append(parse(conn))
        else:
            account_list.append(parse(conns))
        return assembly(account_list)

    except Exception as exp:
        raise V2AdaptorError("Adapt connection account to v2 fields failed: %s" % exp)
