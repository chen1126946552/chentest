"""
Special controller endpoints for direct table access.
"""

from flask_restplus import Resource

from app import api
from services.connection_service import Table as table_svc
from .schemas import connection_table_read_model

ns = api.namespace('tables')

# pylint: disable=missing-docstring

@ns.route('/<string:table_id>')
@ns.doc('Operations for a single table. This is special resource '
        'for accessing table without parent connection information '
        'and should be deprecated long term.')
class Table(Resource):
    @ns.doc('Deletes a single table.')
    @ns.marshal_with(connection_table_read_model)
    def delete(self, table_id):
        return table_svc.delete(None, table_id, raise_if_not_found=True)
