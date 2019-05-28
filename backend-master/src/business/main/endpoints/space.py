# pylint: disable=missing-docstring
from __future__ import absolute_import

from flask import request
from flask_restplus import Resource
from app import api
from services import space_service
from .schemas import transfer_data_expect_model

ns = api.namespace('spaces')


@ns.route('/resources/transfer')
@ns.doc('Transfer all data (Dashboards, Folders, Data sources) '
        'belonging to this member to another member.')
class ResourcesTransfer(Resource):
    @ns.doc('Transfer all data (Dashboards, Folders, Data sources) '
            'belonging to this member to another member.')
    @ns.expect(transfer_data_expect_model)
    def post(self):
        req_data = request.json
        old_uid = int(req_data.get("oldUid"))
        new_uid = int(req_data.get("newUid"))
        space_id = req_data.get("spaceId")
        space_service.transfer_resources(old_uid, new_uid, space_id)
