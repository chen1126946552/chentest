"""Business logic for managing datasources and authorization"""

from __future__ import absolute_import

import json
import logging
from urllib.parse import urlencode

from flask import current_app as flask_app

from app import cache, db
from common.http.utils import ApiError, get_json, post_json, get_headers
from models.datasource import DatasourceAuthModel, DatasourceModel

from .connection_service import add_or_update_connection
from .downstream import make_ds_call_url
from .exceptions import EntityNotFoundError, ServiceError

# pylint: disable=no-member

logger = logging.getLogger(__name__)


def get_all(locale='en_US'):
    """Gets all datasources"""
    datasources = DatasourceModel.query.all()

    # include datasource config
    for datasource in datasources:
        try:
            datasource.config = get_config(datasource.code, locale)
        except ApiError:
            logger.exception('Unable to get ds config for %s', datasource.code)
    return datasources


def add_new_datasource(data):
    """Adds a new datasource"""

    datasource = DatasourceModel(**data)
    db.session.add(datasource)
    db.session.commit()
    return datasource


def _config_item(key):
    value = flask_app.config.get(key)
    if not value:
        raise ServiceError(f'Missing config item: {key}')
    return value


def get_config(code, locale='en_US'):
    """Gets datasource configuration"""
    url = make_ds_call_url(code, '/config')
    if locale:
        url += f'?locale={locale}'
    config = get_json(url)
    return config


def get_by_id(id, locale='en_US', raise_if_missing=False):
    """Gets a datasource by id"""
    model = DatasourceModel.query.filter_by(id=id).first()
    if not model:
        if raise_if_missing:
            raise EntityNotFoundError(f'Datasource not found: id={id}')
        else:
            return None
    model.config = get_config(model.code, locale)
    return model


def get_by_code(code, locale='en_US', raise_if_missing=False):
    """Gets a datasource by code"""
    model = DatasourceModel.query.filter_by(code=code).first()
    if not model:
        if raise_if_missing:
            raise EntityNotFoundError(f'Datasource not found: code={code}')
        else:
            return None
    model.config = get_config(code, locale)
    return model


def _get_callback_url(code):
    return {'__dd_callback_url': _config_item('AUTH_CALLBACK_URL').format(code)}


def _make_auth_context_cache_key(ds_code, state):
    return f'auth.{ds_code}.{state}'


def get_auth_info(code, form_args=None, locale='en_US'):
    """Gets datasource authorization info"""

    config = get_config(code, locale)
    if not config:
        raise ServiceError(f'Unable to find config for {code}')

    if config.get('auth'):
        auth_type = config['auth'].get('type')
        if auth_type not in ['oauth', 'hybrid']:
            raise ServiceError(f'{auth_type} auth is not supported yet')
    else:
        raise ServiceError(f'Auth type is missing in config')

    url = make_ds_call_url(code, '/auth/init')
    # Pass callback url to datasource
    url += '?' + urlencode(_get_callback_url(code))
    if form_args:
        url += '&' + urlencode({'__dd_form_args': form_args})

    auth_info = get_json(url)
    if not auth_info:
        raise ServiceError('Unable to get auth info from datasource service')

    state = auth_info.get('state')
    if not state:
        raise ServiceError('Datasource service did not return auth state')

    auth_context = auth_info.get('context')
    if auth_context:
        # put auth context into cache
        assert isinstance(auth_context, str)
        context_cache_key = _make_auth_context_cache_key(code, state)
        cache.set(context_cache_key, auth_context, timeout=180)
        logger.info('Setting auth context: %s', auth_context)

    redirect_uri = auth_info.get('redirectUri')
    if not redirect_uri:
        raise ServiceError('Unable to get redirect Uri from datasource service')

    return DatasourceAuthModel(type='oauth',
                               oauth_uri=redirect_uri,
                               oauth_state=state)


def process_auth_callback(code, args, headers, locale='en_US'):
    """Processes OAuth token callback"""

    config = get_config(code, locale)
    if not config:
        raise ServiceError(f'Unable to find config for {code}')

    # analyze datasource config to tell how to extract oauth
    # state from callback request
    extract_state_from = 'urlparam'
    state_param_name = 'state'
    callback_descriptor = config.get('auth', {}).get('callbackDescriptor')
    if callback_descriptor:
        extract_state_from = callback_descriptor.get('extractStateFrom') or 'urlparam'
        state_param_name = callback_descriptor.get('stateParamName') or 'state'

    auth_state = None
    if extract_state_from == 'urlparam':
        # get from url parameter
        auth_state = args.get(state_param_name)
    elif extract_state_from == 'header':
        # get from http header
        auth_state = headers.get(state_param_name)
    else:
        raise ServiceError('Unknown value for extractStateFrom configuration: '
                           f'{extract_state_from}')

    auth_context = None
    if auth_state:
        # if we get state, try to load auth context from cache
        context_cache_key = _make_auth_context_cache_key(code, auth_state)
        auth_context = cache.get(context_cache_key)
        logger.info('Got auth context: %s', auth_context)

    url = make_ds_call_url(code, '/auth/callback')

    # Pass callback url to datasource
    callback_args = _get_callback_url(code)
    if args:
        callback_args.update(args)
    if auth_context:
        # pass along auth context to datasource's cadllback
        callback_args['__dd_auth_context'] = auth_context

    url += '?' + urlencode(callback_args)

    logger.info('Processing auth callback: %s', url)
    result = get_json(url)
    if not result:
        raise ServiceError('Unable to get datasource service to process auth callback')

    logger.info('Auth result: %s', result)

    # validate auth result
    if 'token' not in result:
        raise ServiceError('Auth result missing token')

    connection = add_or_update_connection({
        'ds_code': code,
        'auth_type': 'oauth',
        'auth_info': json.dumps(result['token'], ensure_ascii=False),
        'account_id': result['id'],
        'name': result['name'],
    })

    return {
        'id': connection.id,
        'name': connection.name,
        'account_id': connection.account_id,
        'oauth_state': auth_state
    }


def auth_validate(code, body):
    """
    validate form information
    Args:
        code: datasource code
        body: request body containing token in it
    Returns:
    """
    url = make_ds_call_url(code, '/auth/validate')
    req_params = body.copy()
    if 'token' in req_params:
        # deserialize token to json before sending to datasource service
        req_params['token'] = json.loads(req_params['token'])
    result = post_json(url=url, headers=get_headers(), body=req_params)
    if not result or not result.get('status') == 'ok':
        raise ServiceError(f'Validate auth form: %s failed.' % body)
    return result
