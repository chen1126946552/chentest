'''
Endpoints for getting datasources available for the user and space in context.
Forwards requests to data-mananger and filters by user/space visibility.
'''

from __future__ import absolute_import

from flask_restplus import Resource
from app import api
from services import data_service as svc


ns = api.namespace('datasources')

# pylint: disable=missing-docstring


@ns.route('/')
@ns.doc('Datasource list operations.')
class DatasourceList(Resource):
    def get(self):
        return svc.get_datasource_list()


@ns.route('/<string:ds_code>')
@ns.doc('Single datasource operations.')
class Datasource(Resource):
    def get(self, ds_code):
        return svc.get_ds_info_by_code(ds_code)
