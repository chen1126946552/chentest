"""
Form authorization related dispatches
"""

from __future__ import absolute_import

import json
import logging

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request

from common.http.proxy import proxy
from common.http.utils import post_json
from services.downstream import get_datasource_config, get_datasource_info
from utils.system_constant import get_ds_code_list

from .token import verify_token

api = Blueprint('form_auth', __name__)
logger = logging.getLogger(__name__)


@api.route('/api/v3/ds/<string:ds_code>/authForm', methods=['GET'])
@verify_token
def auth_form_dispatch(ds_code):
    """Gets form authorization config"""

    if ds_code in get_ds_code_list():
        ds_info = get_datasource_info(ds_code)
        config = get_datasource_config(ds_code)
        form_items = config['auth']['formItems']
        auth_type = config['auth']['type']
        form_info = {
            'authType': auth_type,
            'datasource': ds_info['code'],
            'dataSourceType': auth_type,
            'description': '',
            'dsId': ds_info['id'],
            'itemList': [
                {
                    'defaultValue': '',
                    'inputType': 'INPUT_TEXT',
                    'name': item['key'],
                    'placeholder': item['placeholder'],
                    'title': item['label'],
                    'validations': ''
                }
                for item in form_items
            ]
        }
        return jsonify({'data': form_info, 'success': True, 'errorCode': None, 'message': None})

    return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')


@api.route('/api/v3/ds/<string:ds_code>/authForm', methods=['POST'])
@verify_token
def auth_form_create_dispatch(ds_code):
    """Form based authentication and connection creation"""

    if ds_code in get_ds_code_list():

        ds_info = get_datasource_info(ds_code)
        config = get_datasource_config(ds_code)
        auth_form_info = request.json
        assert 'name' in auth_form_info

        body = {
            'auth_info': json.dumps(auth_form_info, ensure_ascii=False),
            'user_id': request.headers.get('UID'),
            'space_id': request.headers.get('SpaceId'),
            'ds_code': ds_code,
            'account_id': auth_form_info['name'],
            'name': auth_form_info['name'],
            'auth_type': config['auth']['type']
        }
        connection_url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/'
        conn_result_info = post_json(connection_url, body=body)
        data = {
            'blockself': None,
            'config': request.json,
            'connectionId': conn_result_info['id'],
            'creatorId': '',
            'dataTimezone': None,
            'displayName': None,
            'dsCode': ds_code,
            'dsId': ds_info['id'],
            'fileSize': None,
            'name': auth_form_info['name'],
            'sourceType': 'USER_CREATED',
            'sourceUid': '',
            'spaceId': request.headers.get('SpaceId'),
            'status': '1',
            'uid': request.headers.get('UID'),
            'updateTime': '',
            'userName': ''
        }
        logger.info('Successfully created connection with form auth: %s', auth_form_info)
        return jsonify({"success": True, "data": data, "errorCode": None, "message": None,
                        "params": None, "stackTrace": None})

    return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
