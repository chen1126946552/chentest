'''REST resources for data connections'''

from __future__ import absolute_import

from flask import request
from flask_restplus import Resource

from app import api
from common.service.constants import CommonHeaders
from services import connection_service as svc
from services import table_service as table_svc

from .schemas import *  # pylint: disable=wildcard-import,unused-wildcard-import

ns = api.namespace('connections')

# pylint: disable=missing-docstring


@ns.route('/')
@ns.doc('Connection list operations.')
class ConnectionList(Resource):
    @ns.marshal_list_with(connection_read_model)
    def get(self):
        connections = svc.get_all()
        return connections

    @ns.marshal_with(connection_read_model, code=201)
    @ns.expect(connection_create_model)
    def post(self):
        payload = request.json
        connection = svc.add_or_update_connection(payload)
        return connection


@ns.route('/<string:conn_id>')
@ns.doc('Single connection operations.')
class Connection(Resource):
    @ns.marshal_with(connection_read_model)
    def get(self, conn_id):
        connection = svc.get_by_id(conn_id, raise_if_missing=True)
        return connection

    @ns.expect(connection_create_model)
    @ns.marshal_with(connection_read_model)
    def put(self, conn_id):
        payload = request.json
        connection = svc.update_connection(conn_id, payload, raise_if_missing=True)
        return connection

    @ns.marshal_with(connection_read_model)
    def delete(self, conn_id):
        connection = svc.delete_by_id(conn_id, raise_if_missing=True)
        return connection


@ns.route('/<string:conn_id>/fields')
class ConnectionFields(Resource):
    @ns.expect(meta_request_model)
    @ns.marshal_list_with(field_model)
    def post(self, conn_id):
        locale = request.headers.get(CommonHeaders.LOCALE)
        return svc.get_fields(conn_id,
                              request.json,
                              locale=locale)


@ns.route('/<string:conn_id>/data')
class ConnectionData(Resource):
    @ns.expect(data_request_model)
    @ns.marshal_with(data_response_model)
    def post(self, conn_id):
        locale = request.headers.get(CommonHeaders.LOCALE)
        return svc.get_data(conn_id, request.json, locale)


@ns.route('/<string:conn_id>/table_preview_data')
class ConnectionTablePreviewData(Resource):
    @ns.expect(table_preview_data_request_model)
    @ns.marshal_with(table_preview_data_response_model)
    def post(self, conn_id):
        locale = request.headers.get(CommonHeaders)
        return svc.get_table_preview_data(conn_id, request.json, locale)


@ns.route('/<string:conn_id>/hierarchy')
class ConnectionHierarchy(Resource):
    @ns.expect(hierarchy_request_model)
    @ns.marshal_with(hierarchy_response_model)
    def post(self, conn_id):
        locale = request.headers.get(CommonHeaders.LOCALE)
        return svc.get_hierarchy(conn_id, request.json, locale)


@ns.route('/<string:conn_id>/segments')
class ConnectionSegment(Resource):
    @ns.expect(meta_request_model)
    @ns.marshal_list_with(segment_model)
    def post(self, conn_id):
        locale = request.headers.get(CommonHeaders.LOCALE)
        return svc.get_segment(conn_id, request.json, locale)


@ns.route('/<string:conn_id>/tables')
@ns.doc('Table list operations.')
class ConnectionTableList(Resource):

    @ns.marshal_list_with(connection_table_read_model)
    def get(self, conn_id):
        return table_svc.get_all(conn_id)

    @ns.expect(connection_table_create_model)
    @ns.marshal_with(connection_table_read_model)
    def post(self, conn_id):
        req = request.json
        return table_svc.create_table(conn_id, req)


@ns.route('/<string:conn_id>/tables/<string:table_id>')
@ns.doc('Single connection table operations.')
class ConnectionTable(Resource):
    @ns.marshal_with(connection_table_read_model)
    def get(self, conn_id, table_id):
        connection = table_svc.get_by_id(conn_id, table_id, raise_if_missing=True)
        return connection

    @ns.expect(connection_table_read_model)
    @ns.marshal_with(connection_table_read_model)
    def put(self, conn_id, table_id):
        payload = request.json
        connection = table_svc.update_table(conn_id, table_id, payload, raise_if_missing=True)
        return connection

    @ns.marshal_with(connection_table_read_model)
    def delete(self, conn_id, table_id):
        connection = table_svc.delete_by_id(conn_id, table_id, raise_if_missing=True)
        return connection


@ns.route('/<string:conn_id>/tables/<string:table_id>/fields')
@ns.doc('Table fields operations.')
class ConnectionTableFields(Resource):
    @ns.marshal_list_with(field_model)
    @ns.doc('Gets fields under a table.')
    def get(self, conn_id, table_id):
        columns = table_svc.get_columns(conn_id, table_id, raise_if_missing=True)
        return [
            {
                'id': column['code'],
                'name': column['name'],
                'type': column['dataType'],
                'allowFilter': True,
                'allowGroupby': True,
                'allowAggregation': True
            } for column in columns if column.get('include')
        ]


@ns.route('/<string:conn_id>/tables/<string:table_id>/data')
@ns.doc('Table data operations.')
class ConnectionTableData(Resource):
    @ns.expect(data_request_model)
    @ns.marshal_with(data_response_model)
    @ns.doc('Gets data from a table.')
    def post(self, conn_id, table_id):
        locale = request.headers.get(CommonHeaders.LOCALE)
        return table_svc.get_data(conn_id, table_id, request.json, locale)
