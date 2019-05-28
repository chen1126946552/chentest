'''
Endpoints for dealing with OAuth authorization:
    - Checks permission for using a datasource
    - Contacts data-manager to initiate OAuth flow and maintains state for callback correlation
    - Contacts data-manager to complete OAuth callback, and persists the connection

The endpoints are not REST style but it doesn't hurt to use Resource to represent.
'''

from __future__ import absolute_import

import json
from flask import request, redirect
from flask_restplus import Resource
from app import api
from services import auth_service as svc


ns = api.namespace('oauth')

# pylint: disable=missing-docstring


@ns.route('/init/<string:ds_code>')
@ns.doc(('OAuth initialization. This endpoint delivers authorization URL '
         'and a unique state for tracking the process.'))
class OAuthInit(Resource):
    def get(self, ds_code):
        user_id, space_id, socket_id = \
            request.args.get('uid'), request.args.get('spaceId'), request.args.get('socketId')
        assert user_id
        assert space_id
        redis_cache_data = json.dumps(
            {
                "user_id": user_id,
                "space_id": space_id,
                "socket_id": socket_id,
            }
        )
        redirect_uri = svc.auth_init(ds_code, redis_cache_data, request.args.get('form_args'))
        return redirect(redirect_uri, 302)


@ns.route('/callback/<string:ds_code>')
@ns.doc(('OAuth callback. Request parameter should carry authorization code. '
         'This endpoint delegates the code to datasource service to complete the OAuth flow, '
         'and eventually records a created/updated connection.'))
class OAuthCallback(Resource):
    def get(self, ds_code):
        svc.auth_callback(request, ds_code)
        return redirect('https://authv2.datadeck.com/jsp/authenticated.jsp', 302)
