"""All classes/methods/tools to help to adapt to v2 `preview`"""

import uuid


def adapt_preview_data(uid,
                       connection_id,
                       table,
                       ds_id,
                       preview_data):
    """
    Adapts vnext data table preview data to v2.

    Args:
        uid (str): UID.
        connection_id (str): Connection id.
        table (dict): Table object.
        ds_id (int): Datasource ID.
        preview_data (dict): Preview data payload.

    Returns:
        dict: Adapted data.
    """

    database = table['database']
    table_id = table['id']
    table_name = table['name']

    # 'columns' are table columns defined by user when
    # a table is saved.
    #
    # When this function is called at preview time (before
    # table is saved, 'columsn' is None; otherwise it
    # contains definitions provided by user.
    #
    # The adaptation code deals with both cases: when 'columns'
    # are available, type and formatting options are got from it,
    # otherwise it's got from fields of the preview_data (which
    # determines the default type of columns).

    columns = table.get('columns')

    rows = preview_data['data']
    rows.insert(0, [fld['id'] for fld in preview_data['fields']])
    data = {
        'data': preview_data['data'],
        'table': _adapt_table_structure(table_id, table_name, columns, preview_data['fields']),
        'tableId': table_name,
        'timezone': None,
        'colSum': len(preview_data['data']),
        'connectionId': connection_id,
        'createTime': None,
        'creatorId': None,
        'dataBaseName': database,
        'dsId': ds_id,
        'lastModifiedDate': None,
        'lastUpdateTime': None,
        'name': table_name,
        'operateType': '',
        'remotePath': '',
        'remoteStatus': '1',
        'rowCount': None,
        'sourceId': '',
        'uid': uid,
        'updateFrequency': None,
        'updateHour': None,
        'updateStatus': None,
        'updateTime': None
    }
    return data


def _adapt_table_structure(table_id, table_name, table_columns, data_columns):

    if not table_columns:
        # populate dummy table columns for easier processing
        table_columns = [{}] * len(data_columns)

    assert len(table_columns) == len(data_columns)

    def _get_custom_name(table_column, data_column):    # pylint: disable=unused-argument
        return table_column.get('customName')

    def _get_column_type(table_column, data_column):
        if table_column:
            return table_column.get('dataType').upper()
        return data_column['type'].upper()

    def _get_data_format(table_column, data_column):
        if table_column:
            return table_column.get('formatOptions', {}).get('dateFormat', '')
        return 'yyyy-MM-dd' if data_column['type'] == 'date' else ''

    def _get_date_front(table_column, data_column):
        if table_column:
            return table_column.get('formatOptions', {}).get('dateStartsWith', None)
        return 'year' if data_column['type'] == 'date' else None

    def _get_data_format_type(table_column, data_column):   # pylint: disable=unused-argument
        if table_column:
            currency_symbol = table_column.get('formatOptions', {}).get('currencySymbol')
            if currency_symbol:
                return f'{currency_symbol}###'
        return ''

    return {
        'code': table_name,
        'colSum': str(len(data_columns)),
        'columnCount': len(data_columns),
        'columns': [
            {
                'code': data_column['name'],
                'columnType': _get_column_type(table_column, data_column),
                'customDateColumn': False,
                'customName': _get_custom_name(table_column, data_column),
                'dataType': None,

                'dataFormat': _get_data_format(table_column, data_column),
                'dataFormatType': _get_data_format_type(table_column, data_column),
                'dateFront': _get_date_front(table_column, data_column),

                'display': table_column.get('include', True),
                'id': str(uuid.uuid1()),
                'index': index,
                'isCustom': None,
                'name': data_column['name'],
                'ordinalPosition': 0,
                'primaryKey': False,
                'remarks': None,
                'separator': None,

                # TODO: check if this is needed
                'type': 'metrics' if data_column['type'] == 'number' else 'dimension'
            }
            for index, (table_column, data_column) in enumerate(zip(table_columns, data_columns))],
        'headIndex': 0,
        'headMode': 'assign',
        'headType': 'row',
        'id': table_id,
        'ignoreCol': [],
        'ignoreColEnd': None,
        'ignoreColStart': None,
        'ignoreRow': [],
        'ignoreRowEnd': 0,
        'ignoreRowStart': 1,
        'rowSum': None,
        'tableName': table_name,
        'tableType': None
    }
