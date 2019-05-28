'''Dispatching rules for OAuth related requests'''

from __future__ import absolute_import

from urllib.parse import urlencode

from flask import Blueprint
from flask import current_app as app
from flask import request

from common.http.proxy import proxy
from utils.system_constant import get_ds_code_list

api = Blueprint('datasource', __name__)


@api.route('/api/v3adapter/connect/<string:ds_code>')
@api.route('/api/v4/business/oauth/init/<string:ds_code>')
@api.route('/connect/<string:ds_code>')
def ds_auth_init_dispatch(ds_code):
    '''
    Dispatches datasource oauth init request, to old dsgateway and
    vnext endpoint respectively
    '''

    if ds_code not in get_ds_code_list():
        return proxy(request, f'{app.config["AUTH_V2_URL"]}{request.path}')

    downstream = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/oauth/init/{ds_code}'

    # formArgs parameter is for hybrid authorization: user fills
    # in a form first, and then the form values (in form of url
    # encoded json) will be passed to standard oauth flow as arguments
    form_args = request.args.get('formArgs')
    if form_args:
        downstream += '?' + urlencode({'form_args': form_args})

    return proxy(request, downstream)


@api.route('/datadeck-app-datasource/<string:ds_code>/auth/tokenCallback')
@api.route('/api/v4/business/oauth/callback/<string:ds_code>')
def ds_auth_callback_dispatch(ds_code):
    '''
    Dispatches datasource oauth callback request, to old dsgateway
    and vnext endpoint respectively
    '''

    if ds_code not in get_ds_code_list():
        return proxy(request, f'{app.config["DS_GATEWAY_URL"]}{request.path}')

    downstream = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/oauth/callback/{ds_code}'
    return proxy(request, downstream)
