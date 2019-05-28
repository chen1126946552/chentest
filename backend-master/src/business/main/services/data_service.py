"""business data service"""

from copy import deepcopy
from uuid import uuid1

from common.http.utils import get_headers, get_json, post_json
from common.service.constants import GraphType
from exception import EntityNotFoundError
from .calculated_field_service import get_by_id_with_deleted as get_calculated_field
from .connection_service import Connection as csvc
from .downstream import make_dm_connection_url, make_dm_datasource_url


# pylint: disable=missing-docstring


def get_datasource_list():
    """Gets datasource list from data manager"""
    url = make_dm_datasource_url('/')
    return get_json(url, headers=get_headers())


def get_data(conn_id, req_data):
    """
    Gets data from data-manager
    Args:
        conn_id(string): business connection_id
        req_data(dict): request body
    Returns(dict): connection data

    """
    conn = csvc.get_by_id(conn_id, raise_if_not_found=True)
    assert conn.dm_connection_id
    url = make_dm_connection_url(f'{conn.dm_connection_id}/data')
    body = _downstream_get_data_req_body_make(conn.ds_code, req_data)
    return post_json(url=url,
                     headers=get_headers(),
                     body=body)


def _downstream_get_data_req_body_make(ds_code, req_params):
    """helper method to make downstream req body"""
    body = deepcopy(req_params)
    fields, cal_fields, seq = [], [], []

    for field in body.get('fields', []):
        seq.append(field['uuid'])
        cal_field = get_calculated_field(field['id'])
        if cal_field:
            if cal_field.is_deleted:
                raise EntityNotFoundError("Can not find calculated field: %s" % cal_field.display)
            field.update(_make_calculated_field_params(cal_field))
            cal_fields.append(field)
        else:
            fields.append(field)
    body.update({
        'fields': fields,
        'calculatedFields': cal_fields,
        'seq': seq
    })

    graph_type_str = body.get('graphType')
    if graph_type_str and GraphType(graph_type_str).is_map():
        _add_new_map_field(body, ds_code)

    return body


def _make_calculated_field_params(calf):
    return {
        'isCal': True,
        'id': calf.id,
        'expression': calf.expression,
        'type': calf.data_type,
        'keys': calf.keys,
        'fields': calf.fields,
        'allow_filter': calf.allow_filter,
        'filter_ops': calf.filter_options,
        'allow_aggregation': calf.allow_aggregation,
        'aggregation_ops': calf.aggr_options,
    }


def _add_new_map_field(data, ds_code):
    field_id = str(uuid1())
    data['seq'].insert(0, field_id)
    map_config = _get_map_config(ds_code)
    map_info = data['map']
    map_field = {'type': 'string', 'uuid': field_id, 'groupBy': True}
    if map_info['mapType'] == 'world':
        assert map_config.get('country_field')
        map_field.update({'id': map_config['country_field']})
    else:
        assert map_config.get('region_field')
        map_field.update({'id': map_config['region_field']})
        country_filter = _create_new_filter(map_info['mapCode'], map_config)
        data['filters'].append(country_filter)

    data['fields'].insert(0, map_field)


def _get_map_config(ds_code):
    result = {}
    config = get_ds_config_by_code(ds_code)
    geolocation = config.get('data', {}).get('geolocation')
    if geolocation:
        country_field = geolocation.get('countryField', {}).get('id')
        if country_field:
            result['country_field'] = country_field
        region_field = geolocation.get('regionField', {}).get('id')
        if region_field:
            result['region_field'] = region_field
    return result


def _create_new_filter(country_code, map_config):
    field = {'id': map_config.get('country_field'),
             'type':'string', 'groupBy': True, 'uuid': str(uuid1())}
    return {'field':field, 'operator':'equal', 'values': [country_code]}


def get_table_preview_data(conn_id, req_data):
    """
    Gets table preview data from data-manager
    Args:
        conn_id(string): business connection_id
        req_data(dict): request body
    Returns(dict): connection data

    """
    conn = csvc.get_by_id(conn_id, raise_if_not_found=True)
    assert conn.dm_connection_id
    url = make_dm_connection_url(f'{conn.dm_connection_id}/table_preview_data')
    return post_json(url=url,
                     headers=get_headers(),
                     body=req_data)


def get_ds_info_by_code(ds_code):
    """
    Gets datasource information by its code.
    """

    url = make_dm_datasource_url(f'{ds_code}')
    return get_json(url, headers=get_headers())


def get_ds_config_by_code(ds_code):
    """
    Gets datasource information by its code.
    """
    ds_info = get_ds_info_by_code(ds_code)
    if not ds_info:
        return None
    return ds_info.get('config')
