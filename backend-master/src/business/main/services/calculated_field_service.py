"""Business logic for managing calculated field"""
from __future__ import absolute_import
import logging
import json

from datetime import datetime
from app import db
from common.http.utils import post_json
from models.connection import ConnectionCalFieldModel
from exception import EntityNotFoundError, EntityCreatingOrUpdatingError
from .downstream import make_dm_common_url
from .connection_service import Connection as con_svc

logger = logging.getLogger(__name__)


# pylint: disable=no-member,expression-not-assigned


def get_all(connection_id):
    """
    Gets all calculated fields under a connection.
    """

    return ConnectionCalFieldModel.query.filter_by(
        connection=connection_id
    ).all()


def add_or_update_field(conn_id, params, _id=None):
    """
    Creates a new/ update an exist calculated field under a connection.
    """
    data = dict()
    logger.info('Creating or updating calculated field: %s', params)

    connection = con_svc.get_by_id(conn_id)
    data.update(
        {'connection': conn_id, 'space_id': connection.space_id}
    )

    # todo how to decide the properties of the calculated
    # todo field as a field depending on its candidate fields
    # todo, other datasource may have other types, for now, only number for `type` field

    candidates = params['candidates']
    _types = {c['type'] for c in candidates}

    assert len(_types) == 1, 'Candidates must have the same type'
    data['data_type'] = list(_types)[0]

    validate_params = {
        'expression': params['expression'],
        'keys': [candidate['id'] for candidate in candidates]
    }

    analytics = validate(validate_params)

    if not analytics.get('ok'):
        raise EntityCreatingOrUpdatingError('Calculated is invalid: %s' % data)

    data['function_contain'] = analytics['function_contain']
    data['group_function_contain'] = analytics['group_function_contain']

    data['expression'] = params['expression']
    data['name'] = params['name']
    data['candidates'] = json.dumps(params['candidates'], ensure_ascii=False)

    if _id:
        return update_by_id(_id, data, raise_if_missing=True)
    return create(data)


def create(data):
    """Creates a new calculated field"""
    if data.get('filter_ops'):
        filter_ops = json.dumps(data['filter_ops'])
        if filter_ops:
            data['allow_filter'] = True
    else:
        data['filter_ops'] = None

    if data.get('aggregation_ops'):
        aggr_ops = json.dumps(data['aggregation_ops'])
        if aggr_ops:
            data['allow_aggregation'] = True
    else:
        data['aggregation_ops'] = None

    assert data['data_type'] in ['number', 'string', 'date'], \
        "data type in req body is invalid: %s" % data['type']

    cal_field = ConnectionCalFieldModel(**data)
    db.session.add(cal_field)
    db.session.commit()

    return cal_field


def update_by_id(_id, data, raise_if_missing=True):
    """Updates an existing calculated field"""

    cal_field = get_by_id(_id, raise_if_missing=raise_if_missing)
    for k, v in data.items():
        setattr(cal_field, k, v)
    cal_field.last_update_at = datetime.now()
    db.session.commit()
    return cal_field


def get_by_id(_id, raise_if_missing=True):
    """Gets a calculated field by id"""

    cal_field = ConnectionCalFieldModel.get_by_id(_id)
    if raise_if_missing and not cal_field:
        raise EntityNotFoundError(f'Calculated field not found: {_id}')
    return cal_field


def get_by_id_with_deleted(_id):
    """Gets a calculated field by id. including soft deleted records"""
    return ConnectionCalFieldModel.get_by_id(_id, with_deleted=True)


def delete_by_id(_id):
    """Deletes a calculated field by id"""
    return ConnectionCalFieldModel.delete_by_id(_id)


def validate(params):
    """check a calculated field if is valid"""
    url = make_dm_common_url(end_point='calculated_field_validate')
    return post_json(url=url, body=params)
