"""Business logic for managing db table"""
from __future__ import absolute_import

import json
import logging

from app import db
from models.connection import ConnectionTableModel

from . import connection_service
from .exceptions import EntityNotFoundError

logger = logging.getLogger(__name__)

# pylint: disable=no-member,expression-not-assigned


def get_all(connection_id):
    """
    Gets all tables under a connection.
    """

    return ConnectionTableModel.query.filter_by(
        connection_id=connection_id
    ).all()


def _add_columns(table, columns):
    table.columns = json.dumps(columns, ensure_ascii=False)


def create_table(connection_id, request_params):
    """
    Creates a new table under a connection.
    """

    logger.info('Creating table: %s', request_params['name'])

    table = ConnectionTableModel()
    table.connection_id = connection_id
    table.name = request_params['name']
    table.database = request_params['database']
    db.session.add(table)

    columns = request_params['columns']
    _add_columns(table, columns)

    db.session.commit()

    return table


def update_table(connection_id, table_id, request_params, raise_if_missing=False):
    """
    Updates an existing table.
    """

    table = get_by_id(connection_id, table_id, raise_if_missing=raise_if_missing)
    table.name = request_params['name']
    columns = request_params['columns']
    _add_columns(table, columns)

    db.session.commit()

    return table


def get_by_id(connection_id, table_id, raise_if_missing=False):
    """Gets a table by id"""

    table = ConnectionTableModel.query.filter_by(connection_id=connection_id, id=table_id).first()

    if raise_if_missing and not table:
        raise EntityNotFoundError(f'table not found: {table_id}')
    return table


def get_columns(connection_id, table_id, raise_if_missing=False):
    """
    Gets columns defined in a table.
    """
    table = get_by_id(connection_id, table_id, raise_if_missing=raise_if_missing)
    return table.columns_populated


def get_data(connection_id, table_id, request_params, locale, raise_if_missing=False):
    """
    Gets data from a table.
    """

    table = get_by_id(connection_id, table_id, raise_if_missing=raise_if_missing)
    if not table:
        return None

    # augment fields passed in with column typing and formatting information got
    # from table entity, so that when fetching data, such additional settings can
    # take effect

    fields = request_params['fields']
    column_mapping = {column['code']: column for column in table.columns_populated}
    for field in fields:
        fid = field['id']
        column = column_mapping.get(fid)
        if column:
            options = column.get('formatOptions')
            if options:
                data_type = options.pop('dataType', None)
                if data_type:
                    # prefer type defined in table column
                    field['type'] = data_type
                field['formatOptions'] = options

    return connection_service.get_data(connection_id, request_params, locale)


def delete_by_id(connection_id, table_id, raise_if_missing=False):
    """Deletes a table by id"""

    table = ConnectionTableModel.query.filter_by(connection_id=connection_id, id=table_id).first()

    if raise_if_missing and not table:
        raise EntityNotFoundError(f'table not found: {table_id}')

    table.delete()
    db.session.commit()

    return table
