# pylint: disable=missing-docstring
from __future__ import absolute_import

from flask import request
from flask_restplus import Resource
from app import api
from utils import resource_type, constant
from services import access_rule_service
from services.connection_service import Connection as csvc

from .schemas import (share_connection_expect_model,)


ns = api.namespace('share')


@ns.route('/connection')
@ns.doc('Share connection operations.')
class ShareConnection(Resource):

    @ns.expect(share_connection_expect_model)
    @ns.doc('Share a connection')
    def post(self):
        _share_data_process(access_rule_service.create)

    @ns.expect(share_connection_expect_model)
    @ns.doc('Remove from Shared list')
    def delete(self):
        _share_data_process(access_rule_service.delete_by_all)

    @ns.expect(share_connection_expect_model)
    @ns.doc('Update access rule level')
    def put(self):
        _share_data_process(access_rule_service.update_access_level)


def _share_data_process(handler_func):
    req_data = request.json

    member_list = req_data.get("members")
    resource_id = req_data.get("cid")
    conn = csvc.get_by_id(resource_id)

    owner_id = getattr(conn, "user_id")
    space_id = req_data.get("spaceId")
    is_share_to_all = req_data.get("isShareToAll")
    for member in member_list:
        data = {
            "resource_id": resource_id,
            "resource_type": resource_type.CONNECTION,
            "space_id": space_id,
            "user_id": member.get("shareToUserId"),
            "owner_id": owner_id,
            "group_id": None,
            "access_level": member.get("roleCode")
        }
        handler_func(**data)
    if is_share_to_all == '1':
        data = {
            "resource_id": resource_id,
            "resource_type": resource_type.CONNECTION,
            "space_id": space_id,
            "user_id": None,
            "owner_id": owner_id,
            "group_id": constant.ALL_SPACE_USERS_GROUP_ID,
            "access_level": req_data.get("shareToAllRoleCode")
        }
        handler_func(**data)
    elif is_share_to_all == '0':
        data = {
            "resource_id": resource_id,
            "resource_type": resource_type.CONNECTION,
            "space_id": space_id,
            "owner_id": owner_id,
            "group_id": constant.ALL_SPACE_USERS_GROUP_ID
        }
        handler_func(**data)
