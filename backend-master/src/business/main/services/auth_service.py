"""Business auth service"""

import json
import logging
import time
from urllib.parse import urlencode

from requests import RequestException

from app import cache
from common.http.proxy import proxy
from common.http.utils import get_json
from exception import OauthServiceError
from utils.source_type import UserConnection

from .connection_service import Connection
from .downstream import make_dm_datasource_url
from .websocket_service import ws_push_json

logger = logging.getLogger(__name__)


def auth_init(ds_code, redis_cache_data, form_args=None):
    """
    initialize oauth process
    :param ds_code: data source code
    :param redis_cache_data: user-space-info caching to create a connection
    :return:
    """

    args = None
    if form_args:
        args = urlencode({'form_args': form_args})

    url = make_dm_datasource_url('/auth', ds_code=ds_code, url_args=args)
    resp = get_json(url)
    if not resp or not all((resp.get('oauth_uri'), resp.get('oauth_state'))):
        raise OauthServiceError("Downstream call to dm auth/init, "
                                "return invalid response: %s" % resp)
    oauth_state = resp['oauth_state']
    cache.set(oauth_state, redis_cache_data, timeout=180)
    logger.info(
        "Auth[%s] init, oauth_state: %s, redis_cache_data:%s",
        ds_code, oauth_state, redis_cache_data)
    return resp['oauth_uri']


def auth_callback(request, ds_code):
    """
    callback from third party datasource when oauth process finished
    :param request: the request object from datasource
    :param ds_code: datasouce ds_code
    :return:
    """
    url = make_dm_datasource_url('/auth/callback', ds_code=ds_code)
    try:
        data = proxy(request, url).json
    except RequestException:
        raise OauthServiceError("Downstream call to dm auth/back failed.")
    data['ds_code'] = ds_code

    if 'oauth_state' not in data:
        raise OauthServiceError("Downstream call to dm didn't return oauth_state.")

    redis_cache_data = cache.get(data['oauth_state'])
    if not redis_cache_data:
        raise OauthServiceError("Can not read auth callback params in redis.")
    cache_dic = json.loads(redis_cache_data)
    data.update(cache_dic)

    fields = _connection_fields_parse(data)
    conn = Connection.insert_or_recover(fields)

    _callback_send_websocket(cache_dic.get('socket_id'), conn.id, data)


def _callback_send_websocket(socket_id, connection_id, user_connection):
    """callback done send web-socket to frontend"""
    data = {
        'connectionId': connection_id,
        'uid': user_connection.get('user_id'),
        'creatorId': user_connection.get('user_id'),
        'sourceUid': user_connection.get('user_id'),
        'dsCode': user_connection.get('ds_code'),
        'name': user_connection.get('name'),
        'spaceId': user_connection.get('space_id'),
        'status': '1',
        'updateTime': int(round(time.time()*1000)),
        'config': {
            'instanceId': connection_id
        },
        'sourceType': UserConnection.USER_CREATED
    }

    result_dict = {
        'account': data.get('name'),
        'connectionId': connection_id,
        'instanceId': connection_id,
        'connectionInfo': data
    }

    json_view = {
        'content': result_dict,
        'status': 'success'
    }

    res = ws_push_json(socket_id, json_view)
    logger.info("Websocket push data result:%s , message: %s", res, json_view)


def _connection_fields_parse(data):
    """helper method to parse data with connection fields"""
    return {
        'user_id': data.get('user_id'),
        'space_id': data.get('space_id'),
        'dm_connection_id': data.get('id'),
        'name': data.get('name'),
        'ds_code': data.get('ds_code'),
        'ds_account_id': data.get('account_id')
    }
