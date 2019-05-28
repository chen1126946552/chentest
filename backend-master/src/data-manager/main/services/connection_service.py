"""Business logic for managing data connections"""

from __future__ import absolute_import

import json
import logging
import services.datasource_service as datasource_service
from app import cache, db
from common.http.utils import post_json
from models.connection import ConnectionModel

from .common import Constant, Fields
from .data_services.data import get_data as _get_data, get_data_raw
from .downstream import make_ds_call_url
from .exceptions import EntityNotFoundError, ServiceError

logger = logging.getLogger(__name__)

# pylint: disable=no-member,expression-not-assigned


def get_all():
    """Gets all connections"""
    return ConnectionModel.query.all()


def add_or_update_connection(data):
    """
    Adds a new connection or updates an existing one.
    """

    connection = ConnectionModel(**data)
    auth_type = connection.auth_type

    if auth_type == 'oauth':
        # A oauth connection is identified its account id and ds_code.
        # If a matching record with combination of (account_id, ds_code)
        # is found, the connection is updated, otherwise a new connection
        # is created.

        existing = ConnectionModel.query.filter_by(
            account_id=connection.account_id,
            ds_code=connection.ds_code).first()
        if existing:
            logger.info('Updating existing connection: %s', existing)
            existing.auth_info = connection.auth_info
            db.session.commit()
            return existing

    # create a new connection
    logger.info('Creating new connection: %s', connection)
    db.session.add(connection)
    db.session.commit()
    return connection


def update_connection(id, data, raise_if_missing=False):
    """Updates an existing connection"""

    connection = get_by_id(id, raise_if_missing=raise_if_missing)
    for k, v in data.items():
        setattr(connection, k, v)
    db.session.commit()
    return connection


def get_by_id(id, raise_if_missing=False):
    """Gets a connection by id"""

    connection = ConnectionModel.query.filter_by(id=id).first()
    if raise_if_missing and not connection:
        raise EntityNotFoundError(f'Connection not found: {id}')
    return connection


def delete_by_id(id, raise_if_missing=True):
    """Deletes a connection by id"""

    connection = get_by_id(id, raise_if_missing=raise_if_missing)
    connection.delete()
    return connection


def _token_update(connection, result):
    """ Update access token if exist

    Args:
        connection (ConnectionModel): connection instance
        result (dict): reponse body
    """

    if result.get('tokenUpdate'):
        connection.auth_info = json.dumps(result['tokenUpdate'], ensure_ascii=False)
        db.session.commit()


@cache.memoize(timeout=Constant.Cache.Timeout.inert)
def get_fields(id, data_request, locale):
    """Gets fields under a connection, (optionally) a profile and a report"""

    connection = get_by_id(id, raise_if_missing=True)
    body = {
        'token': json.loads(connection.auth_info),
        'locale': locale
    }

    body.update(data_request)

    url = make_ds_call_url(connection.ds_code, '/fields')
    result = post_json(url, body=body)
    if not result:
        raise ServiceError((f'Unable to get fields for {connection.ds_code}: {id}, '
                            f'data_request'))
    # set default values
    _set_fields_default_values(result['items'])

    _token_update(connection, result)
    return result['items']


def _set_fields_default_values(items):
    """
    set default values to fields
    Args:
        items: fields list in recursive structure
    Returns:

    """
    if items:
        if isinstance(items, list):
            [_set_fields_default_values(item) for item in items]
        elif isinstance(items, dict) and items.get('children'):
            [_set_fields_default_values(_) for _ in items.get('children')]
        else:
            [items.setdefault(k, v) for k, v in Fields.field_default_value.items()]


def _skip_cache_check(*args, **kwargs):
    """a decorator used to skip caching"""
    data_request = kwargs.get('data_request')
    if not data_request:
        for arg in args:
            if isinstance(arg, dict):
                if arg.get('noCache'):
                    return True
    else:
        if isinstance(data_request, dict):
            return data_request.get('noCache')
    return False


# pylint: disable=unused-argument
def _data_dynamic_cache_timeout(result, _id, *args, **kwargs):
    """
    helper method, dynamic cache timeout generate depend on data result
    Args:
        result: data result return by `get_data`
        _id (str): connection id, first arg from `get_data`
        *args/**kwargs: other positional or keyword params
    Returns(int): cache timeout
    """
    if result and result.get('immutable'):
        return Constant.Cache.Timeout.immutable
    connection = get_by_id(_id, raise_if_missing=True)
    cache_policy = datasource_service.get_config(connection.ds_code)['data'].get(
        'cachePolicy', 'normal')
    return getattr(Constant.Cache.Timeout, cache_policy, Constant.Cache.Timeout.default)


@cache.memoize_simple(timeout=_data_dynamic_cache_timeout, unless=_skip_cache_check)
def get_data(_id, data_request, locale):
    '''Get data from a connection based on the data_request'''
    connection = get_by_id(_id, raise_if_missing=True)
    token = json.loads(connection.auth_info)
    body = {'token': token, 'locale': locale}
    body.update(data_request)
    result = _get_data(connection.ds_code, body)
    if not result:
        raise ServiceError(f'Unable to get data for {connection.ds_code}: {data_request}')
    _token_update(connection, result)
    return result


def get_table_preview_data(id, request, locale):
    """
    Gets database table preview data.

    Args:
        id (str): Connection id.
        request (dict): Request parameters dict.

    Returns:
        dict: Preview data result.
    """

    tz_offset = request.get('timezoneOffset', 0)
    data_request = {
        'paging': {'size': 200},
        'path': request.get('path', []),
        'timezoneOffset': tz_offset
    }

    connection = get_by_id(id, raise_if_missing=True)
    if connection.auth_info:
        data_request['token'] = json.loads(connection.auth_info)
    fields = get_fields(id, data_request, None)
    data_request['fields'] = [{'id': field['id']} for field in fields]
    data_request['locale'] = locale
    result = get_data_raw(connection.ds_code, data_request)

    result.pop('summaryValues', None)
    result['fields'] = fields
    return result


@cache.memoize(timeout=Constant.Cache.Timeout.inert)
def get_hierarchy(id, data_request, locale):
    """
    navigates through internal hierarchy of the datasource

    Args:
        id (str): connection Id
        data_request (dict): request body

    Returns:
        dict: HierarchyResonpose
    """
    connection = get_by_id(id, raise_if_missing=True)
    url = make_ds_call_url(connection.ds_code, '/hierarchy')

    hierarchy_body = {
        'token': json.loads(connection.auth_info),
        'locale': locale
        }

    hierarchy_body.update(data_request)

    result = post_json(url, body=hierarchy_body)

    if not result:
        raise ServiceError(f'Unable to get hierarchy for {connection.ds_code}: {data_request}')

    _token_update(connection, result)

    return result


@cache.memoize(timeout=Constant.Cache.Timeout.inert)
def get_segment(id, data_request, locale):
    """
    navigates through internal hierarchy of the datasource

    Args:
        id (str): connection Id
        data_request (dict): request body

    Returns:
        list: segment list
    """
    connection = get_by_id(id, raise_if_missing=True)
    url = make_ds_call_url(connection.ds_code, '/segments')

    body = {
        'token': json.loads(connection.auth_info),
        'locale': locale
        }

    body.update(data_request)

    result = post_json(url, body=body)

    if not result:
        raise ServiceError(f'Unable to get segment for {connection.ds_code}: {data_request}')

    _token_update(connection, result)

    return result['items']
