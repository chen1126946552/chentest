'''
Helpers for making downstream datamanager service calls.
'''

from flask import current_app as app


def make_dm_datasource_url(end_point, ds_code=None, url_args=None):
    """Gets URL to a downstream datasource service for a given ds_code"""
    dm_host = app.config.get('DATA_MANAGER_URL').strip("/")
    if not dm_host:
        raise ValueError(f'Missing config item: DATA_MANAGER_URL')
    if not ds_code:
        url = f'{dm_host}/datasources/{end_point.strip("/")}'
    else:
        url = f'{dm_host}/datasources/{ds_code.strip("/")}/{end_point.strip("/")}'
    if url_args:
        url += '?' + url_args
    return url


def make_dm_connection_url(end_point, conn_id=None):
    """Gets URL to a downstream connection service for a given ds_code"""
    dm_host = app.config.get('DATA_MANAGER_URL').strip("/")
    if not dm_host:
        raise ValueError(f'Missing config item: DATA_MANAGER_URL')
    if not conn_id:
        return f'{dm_host}/connections/{end_point.strip("/")}'
    return f'{dm_host}/connections/{conn_id.strip("/")}/{end_point.strip("/")}'


def make_dm_common_url(end_point):
    """Gets URL to a downstream connection service for a given ds_code"""
    dm_host = app.config.get('DATA_MANAGER_URL').strip("/")
    return f'{dm_host}/common/{end_point.strip("/")}'
