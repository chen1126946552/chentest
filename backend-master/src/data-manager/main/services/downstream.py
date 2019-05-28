'''
Helpers for making downstream datasource service calls.
'''

from flask import current_app as app


def make_ds_call_url(ds_code, path):
    '''Gets URL to a downstream datasource service for a given ds_code'''

    ds_host_prefix = app.config.get('DATASOURCE_HOSTNAME_PREFIX')
    if not ds_host_prefix:
        raise ValueError(f'Missing config item: DATASOURCE_HOSTNAME_PREFIX')

    ds_service_port = app.config.get('DATASOURCE_SERVICE_PORT')
    if not ds_service_port:
        raise ValueError(f'Missing config item: DATASOURCE_SERVICE_PORT')

    return f'http://{ds_host_prefix}{ds_code}:{ds_service_port}{path}'
