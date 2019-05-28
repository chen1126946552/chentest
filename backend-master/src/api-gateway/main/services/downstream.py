"""Downstream call to business|data-manager|data-sources to get vnext resources"""

import logging

from flask import current_app as app

from common.http.utils import (delete_json, get_headers, get_json, post_json,
                               put_json)
from services.adaptors.datasource_config import ds_config_adapt

logger = logging.getLogger(__name__)


def get_connections(user_id=None, space_id=None, ds_code=None):
    """
    Gets vnext connections.

    Vnext connection result need v2's user-info to adapt.
    Headers with token need to be passed on to use to send
    direct request to v2
    Args:
        user_id: User's id
        space_id: User's space id
        ds_code: DataSource ds codet
    Returns:
        connections list
    """
    headers = get_headers()
    if user_id:
        headers["UID"] = user_id
    if space_id:
        headers["SpaceId"] = space_id
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections'
    if ds_code:
        url += f'?ds_code={ds_code}&space_id={space_id}'
    connections = get_json(url, headers=headers)

    # include tables under each connection
    # TODO: consider batch operation
    for conn in connections:
        tables_url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{conn["id"]}/tables'
        tables = get_json(tables_url)
        conn['tables'] = tables

    return connections


def get_connection_info(conn_id):
    """
    Gets business connection info.

    Args:
        conn_id: [string] business connection id

    Returns: business connection info
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{conn_id}'
    return get_json(url)


def get_connection_fields(conn_id, req_params, headers=None):
    """
    Gets business connection fields.

    Args:
        conn_id: [string] business connection id
        req_params: [dict] path
        headers: [dict] custom headers, need contain locale info

    Returns: [list] vnext fields
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{conn_id}/fields'
    return post_json(url, headers=headers or get_headers(), body=req_params)


def get_table_fields(conn_id, table_id):
    """
    Gets table fields from business.

    Args:
        conn_id [str]: business connection id
        table_id [str]: table id

    Returns: [list] vnext fields
    """
    url = (f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/'
           f'{conn_id}/tables/{table_id}/fields')
    return get_json(url, headers=get_headers())


def get_connection_segments(conn_id, req_params, headers=None):
    """
    Gets business connection segments.

    Args:
        conn_id: [string] business connection id
        req_params: [dict] path
        headers: [dict] custom headers, need contain locale info

    Returns: [list] vnext fields
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{conn_id}/segments'
    return post_json(url, headers=headers or get_headers(), body=req_params)


def get_connection_hierarchy(connection_id, path, expand_all=False):
    """
    Gets connection hierarchy.

    Args:
        connection_id: business connection id
        path: parent path under which to fetch hierarchy
        expand_all: indicates if all descendents should be fetched
            recursively
    Returns:{'items':[]}
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{connection_id}/hierarchy'
    return post_json(url, headers=get_headers(),
                     body={'path': path, 'expandAll': expand_all})


def get_connection_tables(connection_id):
    """
    Gets all tables under a connection.

    Args:
        connection_id: business connection id

    Returns: table definition list
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{connection_id}/tables'
    return get_json(url, get_headers())


def get_connection_table(connection_id, table_id):
    """
    Gets a table under a connection.

    Args:
        connection_id: business connection id
        table_id: business table id

    Returns: table definition
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{connection_id}/tables/{table_id}'
    return get_json(url, get_headers())


def create_connection_table(connection_id, req_params):
    """
    Creates a table under a connection.

    Args:
        connection_id: business connection id
        req_params: table definition

    Returns:{'items':[]}
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{connection_id}/tables'
    return post_json(url, body=req_params)


def update_connection_table(connection_id, table_id, req_params):
    """
    Updates a table under a connection.

    Args:
        connection_id: business connection id
        table_id: business table id
        req_params: table definition

    Returns:{'items':[]}
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{connection_id}/tables/{table_id}'
    return put_json(url, body=req_params)


def get_custom_connection_segments(conn_id):
    """
    Gets custom segments under a connection.

    Args:
        conn_id(string): business connection id
    Returns:
        (list) custom segments
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{conn_id}/segments/custom'
    return get_json(url)


def get_connection_data(conn_id, req_params):
    """
    Gets data from a connection.

    Args:
        conn_id(string): business connection id
        req_params(dict): request body

    Returns(dict): vx data

    """
    headers = get_headers()
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{conn_id}/data'
    return post_json(url, headers=headers, body=req_params)


def get_table_data(conn_id, table_id, req_params):
    """
    Gets data from a database table.

    Args:
        conn_id (str): business connection id
        table_id (str): table id
        req_params(dict): request body

    Returns(dict): vx data

    """
    headers = get_headers()
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{conn_id}/tables/{table_id}/data'
    return post_json(url, headers=headers, body=req_params)


def get_datasources():
    """
    Gets all vnext datasources.

    Returns:
        datasource list
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/datasources'
    return get_json(url, headers=get_headers())


def get_table_preview_data(connection_id, req_params):
    """
    Gets preview data of a database table.

    Args:
        connection_id (str): connection id
        req_params (dict): request params

    Returns:
        dict: preview data
    """

    url = (f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/'
           f'{connection_id}/table_preview_data')
    return post_json(url, body=req_params)


def get_datasource_info(ds_code):
    """
    Downstream call to business with ds_code to get datasource information.

    Args:
        ds_code (str): datasource code

    Returns:
        dict: datasource info
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/datasources/{ds_code}'
    return get_json(url, headers=get_headers())


def get_datasource_config(ds_code):
    """
    Downstream call to business with ds_code to get config string
    then parse config string to a dict.

    Args:
        ds_code (str): datasource code

    Returns:
        dict: datasource config
    """
    ds_info = get_datasource_info(ds_code)
    if not ds_info:
        return None
    return ds_info.get("config")


def get_datasource_config_adapted(ds_code, locale='en_US'):
    """
    Downstream call to business for getting datasource config
    and adapt it to V2 format.

    Args:
        ds_code (str): datasource code

    Returns:
        dict: datasource config in V2 format
    """

    config = get_datasource_config(ds_code)
    return ds_config_adapt(ds_code, config, locale)


def ws_push_json(socked_id, json_data):
    """
    Pushs data to websocket based on socketId.

    Args:
        socked_id (str): connection socket id
        json_data (dict): data to push

    Returns:
        dict: push result
    """
    v2_websocket_url = f'{app.config["MIDDLE_URL"]}/api/v1/public/websocket/push/{socked_id}'
    return post_json(v2_websocket_url, body=json_data)


def get_connection_calculated_fields(conn_id):
    """
    Gets business connection calculated fields.

    Args:
        conn_id: [string] business connection id
    Returns: [list] vnext cal fields
    """
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{conn_id}/calculated_fields'
    return get_json(url)


def validate_connection_calculated_field(conn_id, req_params):
    """check if calculate field is valid"""
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/' \
          f'connections/{conn_id}/calculated_fields/validate'
    return post_json(url, body=req_params)


def get_connection_calculated_field(field_id, conn_id='all'):
    """try to get calculated field by id in vnext business"""
    try:
        url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/' \
              f'connections/{conn_id}/calculated_fields/{field_id}'
        return get_json(url)
    except Exception:  # pylint: disable=broad-except
        logger.warning("Can not find calculated field in vnext: %s", field_id)
        return None


def create_calculated_field(conn_id, req_param):
    """add a calculated field"""
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{conn_id}/calculated_fields'
    return post_json(url, body=req_param)


def update_calculated_field(conn_id, field_id, req_param):
    """modify a calculated field by id"""
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/' \
          f'connections/{conn_id}/calculated_fields/{field_id}'
    return put_json(url, body=req_param)


def delete_calculated_field(field_id, req_param):
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/all/calculated_fields/{field_id}'
    return delete_json(url, body=req_param)
