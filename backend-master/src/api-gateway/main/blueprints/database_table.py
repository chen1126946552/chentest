'''Dispatch rules for database related endpoints'''

from __future__ import absolute_import

import logging
from copy import deepcopy

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request

from common.http.proxy import proxy
from common.http.utils import ApiError
from common.uncategorized.datetime_util import DateTime
from services.adaptors.preview import adapt_preview_data
from services.downstream import (create_connection_table,
                                 get_connection_hierarchy, get_connection_info,
                                 get_connection_table, get_datasource_info,
                                 get_table_preview_data,
                                 update_connection_table)
from utils.system_constant import get_ds_code_list, get_ds_id_by_code

from .token import verify_token

api = Blueprint('datatable', __name__)
logger = logging.getLogger(__name__)

# Constant database table configuration for adapting to V2 data format
DB_TABLE_SELECT_CONFIG = {
    "itemList": [
        {
            "keys": {
                "label": "name",
                "value": "id"
            },
            "name": "dataBaseName",
            "inputType": "SELECT_LIST",
            "placeholder": "Please select a database",
            "title": "Database name",
            "ajax": {
                "method": "get",
                "name": "getDataBaseNameList",
                "params": {
                    "url": {
                        "connectionId": {
                            "name": "connection"
                        }
                    }
                },
                "url": "/api/v3/ds/getDataSourceAccountSchema"
                       "/{connectionId}/ptoneRootFolderID::connection"
            },
            "validations": {
                "required": [
                    "Please select a table"
                ]
            }
        },
        {
            "keys": {
                "label": "name",
                "value": "id"
            },
            "defaultValue": "",
            "name": "tableId",
            "inputType": "SELECT_LIST",
            "placeholder": "Please select a table",
            "title": "Table",
            "ajax": {
                "method": "get",
                "name": "getTableList",
                "params": {
                    "url": {
                        "connectionId": {
                            "name": "connection"
                        },
                        "dataBaseName":{
                            "name": "dataBaseName"
                        }
                    }
                },
                "url": "/api/v3/ds/getDataSourceAccountSchema/{connectionId}/{dataBaseName}"
            },
            "validations": {
                "required": [
                    "Please select a table"
                ]
            }
        }
    ]
}


# pylint: disable=unused-argument

@api.route('/api/v3/ds/addTable/<string:ds_code>/from')
@verify_token
def add_table_from(ds_code):
    """Configuration for initiating data table connection"""

    if ds_code in get_ds_code_list():
        return jsonify({'success': True, 'data': DB_TABLE_SELECT_CONFIG})

    return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')


@api.route('/api/v3/ds/getDataSourceAccountSchema/<string:connection_id>'
           '/ptoneRootFolderID::connection')
@verify_token
def get_connection_databases(connection_id):
    """Gets databases under an connection"""

    try:
        get_connection_info(connection_id)
    except ApiError:
        # connection not found in vnext, dispatch to middle
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    result = get_connection_hierarchy(connection_id, [])
    items = result['items']
    return jsonify({'success': True,
                    'data': [
                        {
                            'id': item['id'],
                            'name': item['name'],
                            'directory': item.get('hasChild', False)
                        }
                        for item in items]})


@api.route('/api/v3/ds/getDataSourceAccountSchema/'
           '<string:connection_id>/<string:database>')
@verify_token
def get_connection_database_tables(connection_id, database):
    """Gets tables under a database of a connection"""

    try:
        get_connection_info(connection_id)
    except ApiError:
        # connection not found in vnext, dispatch to middle
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    result = get_connection_hierarchy(connection_id, [database], False)
    return jsonify({'success': True, 'data': result['items']})


@api.route('/api/v3/ds/pullRemoteData', methods=['POST'])
@verify_token
def table_preview():
    """Gets preview data for a database table"""

    req_body = request.json
    instance_id = req_body.get('instanceId')

    assert instance_id, 'Missing instanceId in request body'

    try:
        conn_info = get_connection_info(instance_id)
    except ApiError:
        # connection not found in vnext, dispatch to middle
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    uid = request.headers.get('UID')
    ds_code = conn_info['ds_code']
    ds_info = get_datasource_info(ds_code)
    ds_id = ds_info['ds_id']

    table_name = req_body.get('tableId')
    assert table_name, 'Missing tableId in request body'

    database = req_body['dataBaseName']
    assert database, 'Missing dataBaseName in request body'

    path = [database, table_name]
    tz_offset = DateTime.get_offset(request.headers.get('Timezone'))

    # get preview data from downstream
    downstream_req = {'path': path, 'timezoneOffset': tz_offset}
    result = get_table_preview_data(instance_id, downstream_req)

    # Adapt to v2 format and return.
    #
    # At this point we don't have a table entity yet, so synthesize
    # one and set id as None.

    table = {'id': None, 'database': database, 'name': table_name}
    adapted = adapt_preview_data(uid=uid,
                                 connection_id=instance_id,
                                 table=table,
                                 ds_id=ds_id,
                                 preview_data=result)
    return jsonify({'success': True, 'data': adapted})


@api.route('/api/v3/ds/saveDataSource', methods=['POST'])
@verify_token
def save_table_definition():
    """
    Saves table definition with column information.
    """

    req_body = request.json

    conn_id = req_body.get('connectionId')
    assert conn_id, 'Missing connectionId in request body'

    try:
        # connection not found in vnext, dispatch to middle
        get_connection_info(conn_id)
    except ApiError:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    table = req_body.get('table')
    assert table, 'Missing table in request body'

    database = req_body.get('dataBaseName')
    assert database, 'Missing dataBaseName in request body'

    # build downstream table creation request
    columns = []
    req_params = {
        'name': table['tableName'],
        'database': database,
        'columns': columns
    }

    def make_format_options(column_def):

        # Convert v2 formatting fields to vnext format options dic
        #   - dataType: column data type (can be one coerced by user)
        #   - dateFormat: date type format string
        #   - dateStartsWith: which component starts first in date string,
        #       'year|month|day'
        #   - currencySymbol: currency symbol for currency type
        #   - customName: custom name given to the column

        options = {}

        if column_def['columnType'] == 'NUMBER':
            options['dataType'] = 'number'
        elif column_def['columnType'] in ['DATE', 'DATETIME', 'TIMESTAMP']:
            options['dataType'] = 'date'
            if column_def.get('dataFormat'):
                options['dateFormat'] = column_def['dataFormat']
            if column_def.get('dateFront'):
                options['dateStartsWith'] = column_def['dateFront']
        elif column_def['columnType'] == 'TIME':  # TODO: deal with time type
            options['dataType'] = 'number'
        elif column_def['columnType'] == 'CURRENCY':
            options['dataType'] = 'number'
            if column_def.get('dataFormatType'):
                options['currencySymbol'] = column_def['dataFormatType'][0]
        elif column_def['columnType'] == 'PERCENT':
            options['dataType'] = 'number'
            options['percentage'] = True
        elif column_def['columnType'] == 'STRING':
            options['dataType'] = 'string'

        return options

    column_defs = table.get('columns', [])
    for column_def in column_defs:
        column = {
            'code': column_def['code'],
            'name': column_def.get('customName', None) or column_def['code'],
            'dataType': column_def['columnType'].lower(),
            'include': column_def.get('display', True),
            'formatOptions': make_format_options(column_def)
        }
        columns.append(column)

    # make downstream call to create/update table
    table_id = table.get('id')
    if table_id:
        resp = update_connection_table(conn_id, table_id, req_params)
    else:
        resp = create_connection_table(conn_id, req_params)
    logger.info('Table creation result: %s', resp)

    # extend original request body with columns and return
    result = deepcopy(req_body)
    result['data'] = [c['code'] for c in column_defs]
    return jsonify({'success': True, 'data': result})


@api.route('/api/v3/ds/getDataSourceEditView/<string:connection_id>/<string:table_id>')
@verify_token
def get_table_definition(connection_id, table_id):
    """
    Get table definition with column information.
    """

    try:
        conn_info = get_connection_info(connection_id)
    except ApiError:
        # connection not found in vnext, dispatch to middle
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    table = get_connection_table(connection_id, table_id)

    # get preview data from downstream
    path = [table['database'], table['name']]
    tz_offset = DateTime.get_offset(request.headers.get('Timezone'))
    downstream_req = {'path': path, 'timezoneOffset': tz_offset}
    result = get_table_preview_data(connection_id, downstream_req)

    # adapt to v2 format and return
    uid = request.headers.get('UID')
    ds_id = get_ds_id_by_code(conn_info['ds_code'])
    adapted = adapt_preview_data(uid=uid,
                                 connection_id=connection_id,
                                 table=table,
                                 ds_id=ds_id,
                                 preview_data=result)
    return jsonify({'success': True, 'data': adapted})
