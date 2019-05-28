'''Common apis used for business/or datasoueces?'''

from __future__ import absolute_import

from flask import request, jsonify
from flask_restplus import Resource
from app import api
from services.data_services.calculate import CalculatedDataHandler as CalHandler
from .schemas import cal_field_validating_request_model, cal_field_validating_response_model

ns = api.namespace('common')


# pylint: disable=missing-docstring


@ns.route('/calculated_field_validate')
@ns.doc('Calculated field validating API.')
class CalFieldValidate(Resource):
    """Api for calculated field validating"""

    @ns.expect(cal_field_validating_request_model)
    @ns.marshal_with(cal_field_validating_response_model)
    def post(self):
        payload = request.json
        check_info = CalHandler.check_calf_expression(payload.get('expression'),
                                                      payload.get('keys'))
        if not check_info:
            return jsonify({'ok': False})
        check_info.update({'ok': True})
        return check_info
