"""
REST resources for data connections. All operations are scoped under a user and a space,
specified in UID and SpaceId request headers.

Connections are organized with the following hierarchy:
    connection
        |_ sheet
        |_ table
        |_ file
            |_ sheet

The hierarchy covers:
    - SaaS connection: connection only
    - File upload: connection/sheet
    - Network drive: connection/file/sheet
    - Database: connection/table
    - Other dataset, e.g. Zapier: connection only

Data may be fetchable from any level of the hierarchy.
"""
# pylint: disable=missing-docstring

from __future__ import absolute_import

import json

from flask import request, jsonify
from flask_restplus import Resource

from app import api
from services.connection_service import Connection as csvc
from services.connection_service import Segment as segment_service
from services.connection_service import Table as table_svc
from services import calculated_field_service as calf_svc
from services import data_service as dsvc
from utils.decorator import header_check

# pylint: disable=wildcard-import,unused-wildcard-import
from .schemas import *

ns = api.namespace('connections')

header_check_fields = ('UID', 'SpaceId', )


@ns.route('/')
@ns.doc('Connection list operations.')
class ConnectionList(Resource):
    @ns.doc('Gets all data connections, including accounts and files.')
    @ns.marshal_list_with(connection_read_model)
    @header_check(header_check_fields)
    def get(self):
        space_id = request.args.get("space_id")
        if not space_id:
            space_id = request.headers.get('SpaceId')
        user_id = request.headers.get('UID')
        ds_code = request.args.get("ds_code")
        if ds_code:
            connection_list = csvc.get_by_space_id_and_ds_code_uid(space_id, ds_code, user_id)
        else:
            connection_list = csvc.get_all(user_id, space_id)
        return csvc.get_connection_with_share_info(connection_list, user_id, space_id)

    @ns.expect(connection_create_model)
    @ns.marshal_with(connection_read_model)
    @ns.doc('Creates a new data connection.')
    def post(self):
        """
        create a connection at business level
        """
        data = request.json
        return csvc.create(data)


@ns.route('/<string:conn_id>')
@ns.doc('Single connection operations.')
class Connection(Resource):
    @ns.doc('Gets a single data connection.')
    @ns.marshal_with(connection_read_model)
    def get(self, conn_id):
        return csvc.get_by_id(conn_id, True)

    @ns.doc('Updates a single data connection.')
    @ns.expect(connection_read_model)
    @ns.marshal_with(connection_read_model)
    def put(self, conn_id):
        data = request.json
        return csvc.update_by_id(conn_id, data, True)

    @ns.doc('Deletes a single data connection.')
    @ns.marshal_with(connection_read_model)
    def delete(self, conn_id):
        return csvc.delete_by_id(conn_id, True)


@ns.route('/<string:conn_id>/hierarchy')
@ns.doc('Connection account hierarchy.')
class ConnectionHierarchy(Resource):
    @ns.doc('Gets the hierarchy information for the connection')
    @ns.marshal_with(hierarchy_read_model)
    def post(self, conn_id):
        data = request.json
        return csvc.get_hierarchy_info(conn_id, data)


@ns.route('/<string:conn_id>/fields')
class ConnectionFields(Resource):
    @ns.doc("Gets connection fields")
    @ns.marshal_list_with(field_model)
    def post(self, conn_id):
        req_data = request.json
        return csvc.get_fields(conn_id, req_data)


@ns.route('/<string:conn_id>/calculated_fields')
@ns.doc('Calculated fields list operations.')
class ConnectionCalFieldList(Resource):
    @ns.marshal_list_with(calculated_field_response_model)
    def get(self, conn_id):
        return calf_svc.get_all(conn_id)

    @ns.marshal_list_with(calculated_field_response_model)
    @ns.expect(calculated_field_request_model)
    def post(self, conn_id):
        payload = request.json
        return calf_svc.add_or_update_field(conn_id, payload)


# pylint: disable=unused-argument
@ns.route('/<string:conn_id>/calculated_fields/<string:field_id>')
@ns.doc('Calculated field operations.')
class ConnectionCalField(Resource):
    @ns.marshal_with(calculated_field_response_model)
    def get(self, conn_id, field_id):
        return calf_svc.get_by_id(field_id, raise_if_missing=True)

    @ns.marshal_with(calculated_field_response_model)
    def delete(self, conn_id, field_id):
        return calf_svc.delete_by_id(field_id)

    @ns.marshal_with(calculated_field_response_model)
    @ns.expect(calculated_field_request_model)
    def put(self, conn_id, field_id):
        payload = request.json
        return calf_svc.add_or_update_field(conn_id, payload, _id=field_id)


@ns.route('/<string:conn_id>/segments')
class ConnectionSegments(Resource):
    @ns.doc("Gets connection segments")
    @ns.marshal_with(segment_model)
    def post(self, conn_id):
        req_data = request.json
        return csvc.get_segments(conn_id, req_data)


@ns.route('/<string:conn_id>/data')
@ns.doc('Connection data fetching.')
class ConnectionData(Resource):
    @ns.doc('Gets connection data')
    @ns.marshal_with(data_response_model)
    def post(self, conn_id):
        req_data = request.json
        return dsvc.get_data(conn_id, req_data=req_data)


@ns.route('/<string:conn_id>/table_preview_data')
@ns.doc('Table preview data fetching.')
class TablePreviewData(Resource):
    @ns.doc('Gets table preview data')
    @ns.marshal_with(table_preview_data_response_model)
    def post(self, conn_id):
        req_data = request.json
        return dsvc.get_table_preview_data(conn_id, req_data)


@ns.route('/<string:conn_id>/files')
@ns.doc(('Operations for files under a connection, e.g., a Google Drive account. '
         'Use / or /conn_id endpoints instead for toplevel files.'))
class FileList(Resource):
    @ns.doc('Gets a single file under a connection.')
    def get(self, conn_id):
        pass

    @ns.doc('Creates a new file under a connection.')
    def post(self, conn_id):
        pass


@ns.route('/<string:conn_id>/sheets')
@ns.route('/<string:conn_id>/files/<string:file_id>/sheets')
@ns.doc('Operations for sheets under a file.')
class SheetList(Resource):
    @ns.doc('Gets sheets under a file. For toplevel file, file_id is not provided.')
    def get(self, conn_id, file_id):
        pass

    @ns.doc('Creates a new sheet under a file. For toplevel file, file_id is not provided.')
    def post(self, conn_id, file_id):
        pass


@ns.route('/<string:conn_id>/sheets/<string:sheet_id>')
@ns.route('/<string:conn_id>/files/<string:file_id>/sheets/<string:sheet_id>')
@ns.doc('Operations for a single sheet.')
class Sheet(Resource):
    @ns.doc('Gets a single sheet. For sheet under toplevel file, file_id is not provided.')
    def get(self, conn_id, file_id, sheet_id):
        # TODO: implementation
        pass

    @ns.doc('Updates a single sheet. For sheet under toplevel file, file_id is not provided.')
    def put(self, conn_id, file_id, sheet_id):
        # TODO: implementation
        pass

    @ns.doc('Deletes a single sheet. For sheet under toplevel file, file_id is not provided.')
    def delete(self, conn_id, field_id, sheet_id):
        # TODO: implementation
        pass


@ns.route('/<string:conn_id>/sheets/<string:sheet_id>/data')
@ns.route('/<string:conn_id>/files/<string:file_id>/sheets/<string:sheet_id>/data')
@ns.doc('Sheet data fetching.')
class SheetData(Resource):
    def post(self, conn_id, file_id, sheet_id):
        # TODO: implementation
        pass


@ns.route('/<string:connection_id>/tables')
@ns.doc('Operations for tables under a connection (usually database).')
class TableList(Resource):
    @ns.doc('Gets tables under a connection.')
    @ns.marshal_list_with(connection_table_read_model)
    def get(self, connection_id):
        return table_svc.get_all(connection_id)

    @ns.doc('Creates a new table under a connection.')
    @ns.expect(connection_table_create_model)
    @ns.marshal_with(connection_table_read_model)
    def post(self, connection_id):
        data = request.json
        return table_svc.create(connection_id, data)


@ns.route('/<string:conn_id>/tables/<string:table_id>')
@ns.doc('Operations for a single table.')
class Table(Resource):
    @ns.doc('Gets a single table under a connection.')
    @ns.marshal_with(connection_table_read_model)
    def get(self, conn_id, table_id):
        return table_svc.get_by_id(conn_id, table_id, raise_if_not_found=True)

    @ns.doc('Updates a single table under a connection.')
    @ns.marshal_with(connection_table_read_model)
    def put(self, conn_id, table_id):
        return table_svc.update_by_id(conn_id, table_id, request.json, raise_if_not_found=True)

    @ns.doc('Deletes a single table under a connection.')
    @ns.marshal_with(connection_table_read_model)
    def delete(self, conn_id, table_id):
        return table_svc.delete(conn_id, table_id, raise_if_not_found=True)


@ns.route('/<string:conn_id>/tables/<string:table_id>/fields')
@ns.doc('Operations for table fields.')
class TableFields(Resource):
    @ns.doc('Gets fields of a table.')
    @ns.marshal_list_with(field_model)
    def get(self, conn_id, table_id):
        return table_svc.get_fields(conn_id, table_id, raise_if_not_found=True)


@ns.route('/<string:conn_id>/tables/<string:table_id>/data')
@ns.doc('Table data fetching.')
class TableData(Resource):
    @ns.doc('Gets data from a database table.')
    @ns.marshal_with(data_response_model)
    def post(self, conn_id, table_id):
        return table_svc.get_data(conn_id, table_id, request.json, raise_if_not_found=True)


# pylint: disable=unused-argument
@ns.route('/<string:conn_id>/segment')
@ns.doc('Single Segment operations.')
class Segment(Resource):
    @ns.marshal_with(custom_segment_read_model)
    @ns.expect(custom_segment_create_expect_model)
    @ns.doc('Creates a new segment.')
    def post(self, conn_id):
        """
        create a segment
        """
        body_data = request.json
        data = {
            "user_id": request.headers.get('UID'),
            "space_id": body_data.get("spaceId"),
            "ds_code": request.args.get('ds_code'),
            "connection_id": conn_id,
            "name": body_data.get("name"),
            "scope": body_data.get("scope"),
            "operation": body_data.get("operation"),
            "conditions": json.dumps(body_data.get("conditions")),
            "modifier_id": None
        }
        return segment_service.insert(data)

    @ns.marshal_with(custom_segment_read_model)
    @ns.doc('Get single segment object.')
    def get(self, conn_id):
        """
        Get a segment
        """
        segment_id = request.args.get("id")
        return segment_service.get_by_id(segment_id)

    @ns.doc('Delete single segment object.')
    def delete(self, conn_id):
        """
        Delete a segment
        """
        segment_id = request.args.get("id")
        segment_service.delete_by_id(segment_id)

    @ns.marshal_with(custom_segment_read_model)
    @ns.expect(custom_segment_update_expect_model)
    @ns.doc('Update single segment object.')
    def put(self, conn_id):
        """
        update a segment
        """
        body_data = request.json
        data = {
            "id": body_data.get("id"),
            "name": body_data.get("name"),
            "scope": body_data.get("scope"),
            "operation": body_data.get("operation"),
            "conditions": json.dumps(body_data.get("conditions")),
            "modifier_id": request.headers.get('UID')
        }
        return segment_service.update(data)


@ns.route('/<string:conn_id>/segments/custom')
@ns.doc('Segment list operations.')
class SegmentList(Resource):
    @ns.marshal_with(custom_segment_read_model)
    @ns.doc('Gets segment list.')
    def get(self, conn_id):
        """
        Gets segment list
        """
        return segment_service.get_by_cid(conn_id)


@ns.route('/<string:conn_id>/calculated_fields/validate', methods=['POST'])
class ConnectionCalFieldValidate(Resource):
    @ns.doc('Check calculated field validation')
    @ns.expect(calculated_field_request_model)
    def post(self, conn_id):
        return jsonify(calf_svc.validate(request.json))
