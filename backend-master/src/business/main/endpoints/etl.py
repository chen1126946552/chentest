# pylint: disable=missing-docstring
from __future__ import absolute_import

import json
from http import HTTPStatus
from flask import request
from flask_restplus import Resource


from app import api
from common.service.constants import CommonHeaders
from services import etl_datasource_service

from .schemas import (etl_datasource_get_read_model,
                      etl_datasource_save_read_model)

ns = api.namespace('etl')


@ns.route('/datasources')
@ns.doc('Etl data source operations.')
class EtlDatasourceList(Resource):
    @ns.doc('Save etl datasource')
    @ns.marshal_with(etl_datasource_save_read_model)
    def post(self):
        req_data = request.json
        pt_segments = req_data.get("pteSegments")
        segments = pt_segments if pt_segments else req_data.get("segment")
        convert_data = {
            "id": req_data.get("widgetId"),
            "name": req_data.get("name"),
            "language": request.headers.get(CommonHeaders.LOCALE),
            "timezone": request.headers.get(CommonHeaders.TIMEZONE),
            "fields": json.dumps(req_data.get("fields")) if req_data.get("fields") else None,
            "time": json.dumps(req_data.get("time")) if req_data.get("time") else None,
            "filters": json.dumps(req_data.get("filters")) if req_data.get("filters") else None,
            "segment": json.dumps(segments) if segments else None,
            "sort": json.dumps(req_data.get("sort")) if req_data.get("sort") else None,
            "widget_connection_config_id": req_data.get("dsConnectionId"),
            "space_id": req_data.get("spaceId")
        }
        return etl_datasource_service.insert_or_update(convert_data)


@ns.route('/datasources/<string:datasource_id>')
@ns.doc('Etl data source operations.')
class EtlDatasource(Resource):
    @ns.doc('Gets or update etl datasource')
    @ns.marshal_with(etl_datasource_get_read_model)
    def get(self, datasource_id):
        """Return 204 if not found as legacy code will try it"""
        result = etl_datasource_service.get_by_datasource_id(datasource_id)
        if result:
            return result
        else:
            return '', HTTPStatus.NO_CONTENT
