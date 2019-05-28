"""
Dispatch rules for share services
"""
# pylint: disable=unused-argument
from __future__ import absolute_import

import logging

from flask import Blueprint
from flask import current_app as app
from flask import request, jsonify

from utils.system_constant import (
    get_ds_code_list,
)
from common.http.proxy import proxy
from common.http.utils import request_json, get_headers, post_json
from .token import verify_token

api = Blueprint('share', __name__)
logger = logging.getLogger(__name__)

DATA_SOURCE_CODE_KEY = "dataSourceCode"
SHARE_OPERATE_MAP = {
    "remove": "DELETE",
    "add": "POST",
    "update": "PUT"
}
SHARE_TO_USER_ID_KEY = "shareToUserId"


@api.route('/api/v3/ds/share/<string:space_id>/'
           '<string:type>/<string:host_domain>', methods=['POST'])
@verify_token
def ds_share_dispatch(space_id, type, host_domain):
    """Dispatch shared data source connection"""
    req_body = request.json
    ds_code = req_body.get(DATA_SOURCE_CODE_KEY)
    if ds_code in get_ds_code_list():
        url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/share/connection'
        operate_type = req_body.get("shareToAllOperateType")
        method = SHARE_OPERATE_MAP.get(operate_type)
        data = _invite_handler(space_id, host_domain, req_body)
        request_json(method, url, get_headers(), data)
        return jsonify({"success": True, "data": None})
    return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')


def _invite_handler(space_id, host_domain, data):
    """Handle invited users"""
    member_list = data.get("members")
    invite_user_list = []
    for member in member_list:
        if SHARE_TO_USER_ID_KEY not in member:
            invite_user_list.append({
                "spaceId": space_id,
                "userEmail": member.get("userEmail"),
                "role": "member"
            })
    if invite_user_list:
        email_id_dict = _batch_invite_user(space_id, host_domain, invite_user_list)
        for member in member_list:
            if SHARE_TO_USER_ID_KEY not in member:
                member[SHARE_TO_USER_ID_KEY] = email_id_dict.get(member.get("userEmail"))
    return data


def _batch_invite_user(space_id, host_domain, user_list):
    """Batch invite user by v2"""
    url = f'{app.config["MIDDLE_URL"]}/api/v2/spaces/{space_id}/users/invite/batch/{host_domain}'
    data_list = post_json(url, get_headers(), user_list)
    email_id_dict = {}
    if data_list and data_list.get("success"):
        user_list = data_list.get("data")
        for user in user_list:
            uid = user.get("uid")
            email = user.get("userEmail")
            email_id_dict[email] = uid
    return email_id_dict
