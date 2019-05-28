'''REST resources for datasources'''

from __future__ import absolute_import

from http import HTTPStatus

from flask import abort, request
from flask_restplus import Resource

from app import api
from common.service.constants import CommonHeaders
from services import datasource_service as svc

from .schemas import *  # pylint: disable=wildcard-import,unused-wildcard-import

# pylint: disable=missing-docstring

ns = api.namespace('datasources')


@ns.route('/')
@ns.doc('Datasource list operations.')
class DatasourceList(Resource):
    @ns.marshal_list_with(datasource_read_model)
    def get(self):
        locale = request.headers.get(CommonHeaders.LOCALE)
        return svc.get_all(locale)

    @ns.marshal_with(datasource_read_model, code=201, description='Datasource created')
    @ns.expect(datasource_create_model)
    def post(self):
        payload = request.json
        datasource = svc.add_new_datasource(payload)
        return datasource


@ns.route('/<string:ds_code>')
@ns.doc('Single datasource operations.')
@ns.param('ds_code', 'Datasource code')
class Datasource(Resource):
    @ns.marshal_with(datasource_read_model)
    def get(self, ds_code):
        locale = request.headers.get(CommonHeaders.LOCALE)
        return svc.get_by_code(ds_code, locale)


@ns.route('/<string:ds_code>/auth')
@ns.doc('Datasource authorization operations.')
@ns.param('ds_code', 'Datasource code')
class DatasourceAuth(Resource):
    @ns.marshal_with(datasource_auth_model)
    def get(self, ds_code):
        locale = request.headers.get(CommonHeaders.LOCALE)
        return svc.get_auth_info(ds_code, request.args.get('form_args'), locale)


@ns.route('/<string:ds_code>/auth/callback')
@ns.doc('Datasource authorization callback operations.')
@ns.param('ds_code', 'Datasource code')
class DatasourceAuthCallback(Resource):
    @ns.marshal_with(datasource_auth_callback_model)
    def get(self, ds_code):
        locale = request.headers.get(CommonHeaders.LOCALE)
        result = svc.process_auth_callback(ds_code,
                                           {k: v for k, v in request.args.items()},
                                           request.headers,
                                           locale)
        if not result:
            abort(HTTPStatus.UNAUTHORIZED, 'Unable to complete authorization')
        return result


@ns.route('/<string:ds_code>/auth/validate')
@ns.doc('Datasource authorization(form) operations.')
@ns.param('ds_code', 'Datasource code')
class DatasourceAuthForm(Resource):
    @ns.marshal_with(datasource_auth_validate_model)
    def post(self, ds_code):
        body = request.json
        result = svc.auth_validate(ds_code, body)
        if not result:
            abort(HTTPStatus.UNAUTHORIZED, 'Unable to complete authorization')
        return result
