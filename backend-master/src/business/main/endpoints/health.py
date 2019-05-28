'''Health check endpoints'''

from __future__ import absolute_import

from flask_restplus import Resource
from app import api

ns = api.namespace('health')

# pylint: disable=missing-docstring


@ns.route('/')
@ns.doc('Health status')
class Health(Resource):
    def get(self):
        return {'status': 'good'}
