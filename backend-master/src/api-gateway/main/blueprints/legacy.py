'''Dispatch rules for legacy v1/v2/v3 services'''

from __future__ import absolute_import

import json
import logging
from http import HTTPStatus

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request
from pydatadeck.datasource.operators import FilterOperators

from common.http.proxy import proxy, proxy_raw
from common.http.utils import get_headers, post_json
from common.service.constants import CommonHeaders, DatasourceTypes
from services.adaptors.calculated_field import (calculated_field_candidates_filter,
                                                calculated_field_data_adapt,
                                                calculated_field_editor_data_adapt,
                                                calculated_field_params_parse)
from services.adaptors.common import get_v2_connection_config
from services.adaptors.connection import (connection_account_data_adapt,
                                          connection_result_data_adapt)
from services.adaptors.constant import Constant as V2_CONST
from services.adaptors.data import (make_widget_data,
                                    make_widget_data_filter_selections)
from services.adaptors.datasource import (ds_single_data_adapt,
                                          dslist_result_data_adapt)
from services.adaptors.field import (fields_result_data_adapt,
                                     filter_fields_result_data_adapt)
from services.adaptors.global_filter import profiles_data_adapt
from services.adaptors.segment import segments_result_data_adapt
from services.downstream import (create_calculated_field,
                                 delete_calculated_field,
                                 get_connection_calculated_field,
                                 get_connection_calculated_fields,
                                 get_connection_fields,
                                 get_connection_hierarchy,
                                 get_connection_segments,
                                 get_connection_tables, get_connections,
                                 get_datasource_config_adapted,
                                 get_datasource_info, get_datasources,
                                 get_table_fields, update_calculated_field,
                                 validate_connection_calculated_field)
from services.exception import ServiceError
from services.translate import get_translator
from utils.ds_connection_config_parser import \
    parse as parse_ds_connection_config
from utils.system_constant import (get_ds_code_by_id, get_ds_code_list,
                                   get_ds_info_by_ds_id)

from .token import verify_token

api = Blueprint('legacy', __name__)
logger = logging.getLogger(__name__)

METHODS = ['GET', 'POST', 'PUT', 'DELETE']

PROFILE_ID_FIELD_NAME = 'legacyId'

# Used to filter old panel template for vnext space
MIGRATED_DATASOURCES = {1:'googleanalysis'}
# pylint: disable=unused-argument


@api.route('/api/v2/users/signin', methods=['POST'])
def signin_dispatch():
    """User signin endpoint, no token verification"""
    return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')


@api.route('/api/v3/ds/connection/<string:connection_id>', methods=['DELETE'])
def delete_connection_dispatch(connection_id):
    """Delete single connection"""
    delete_type = request.args.get('type')
    if delete_type == 'datasource-db':
        # deleting a database connection

        # TODO: currently front-end passes in table id directly without its parent
        # connection id, so business layer has to provide a special endpoint just
        # for deleting a table without its containing connection. This should be fixed
        # in the future
        busines_url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/tables/{connection_id}'
    else:
        busines_url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{connection_id}'
    v_resp = proxy(request, busines_url)
    middle_resp = proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    result = True
    if v_resp.status_code != HTTPStatus.OK or middle_resp.status_code != HTTPStatus.OK:
        result = False
    return jsonify({"success": result})


@api.route('/api/v3/ds/list')
@verify_token
def ds_list_dispatch():
    """
    Merges datasource list from legacy v3 service with new vnext datasources.
    """

    ds_list = []
    service_ds_list = []
    result = {'success': True, 'data': {'ds': ds_list, 'serviceDsList': service_ds_list}}

    # get ds list from v3
    old_result = proxy_raw(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    if old_result.status_code == HTTPStatus.OK:
        body = old_result.json()
        if body and 'data' in body:
            if 'ds' in body['data']:
                ds_list.extend(body['data']['ds'])
            if 'serviceDsList' in body['data']:
                service_ds_list.extend(body['data']['serviceDsList'])

    # get vnext connections
    conns = get_connections(user_id=request.headers.get('UID'),
                            space_id=request.headers.get('SpaceId')
                            )

    # count connection number with ds_code
    def get_conn_count(_ds_code):
        return len([conn for conn in conns if conn['ds_code'] == _ds_code])

    # merge datasources from vnext
    vx_datasources = get_datasources()
    if vx_datasources:
        logger.info('Vnext datasources: %s', body)
        vx_ds_list = [
            {
                'name': ds['name'],
                'code': ds['code'],
                'description': ds['description'],
                'connectionCount': get_conn_count(ds['code'])
            } for ds in vx_datasources
        ]
        # adapt to v2
        result_data = dslist_result_data_adapt(vx_ds_list)
        ds_list.extend(result_data)
    return jsonify(result)


@api.route('/api/v3/ds/connections')
@verify_token
def connection_list_dispatch():
    """
     Merges connection list from legacy v3 service with new vnext datasources.
    """
    connection_list = []
    result = {'success': True, 'data': connection_list}

    # get connection list from v3
    old_result = proxy_raw(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    if old_result.status_code == HTTPStatus.OK:
        body = old_result.json()
        if body and 'data' in body:
            connection_list.extend(body['data'])
    conns = get_connections(request.headers.get('UID'), request.headers.get('SpaceId'))
    # adapt result vx to v2
    result_data = connection_result_data_adapt(conns)
    if result_data:
        logger.info('Vnext connections: %s', result_data)
        connection_list.extend(result_data)
    return jsonify(result)


@api.route('/api/v1/datasources/config/common')
@verify_token
def datasource_common_config_dispatch():
    """
    Add missing filter operator (with translation).
    """
    _ = get_translator(request.headers.get('Accept-Language'), 'config')

    v2_result = proxy_raw(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    if v2_result.status_code == HTTPStatus.OK:
        body = v2_result.json()
        if body and 'data' in body:
            data = body['data']

            # add several new filter operators that are not covered by V2

            # simple operations
            string_ops = data.get('filter', {}).get('string', {}).get('select')
            if string_ops:
                string_ops[FilterOperators.IN_LIST] = _('Include')
                string_ops[FilterOperators.NOT_IN_LIST] = _('Does not include')

            # advanced operations
            string_ops = data.get('filter', {}).get('string', {}).get('advance')
            if string_ops:
                string_ops[FilterOperators.STR_CONTAIN] = _('Contains')
                string_ops[FilterOperators.STR_NOT_CONTAIN] = _('Does not contain')
                string_ops[FilterOperators.STR_BEGIN_WITH] = _('Begin with')
                string_ops[FilterOperators.STR_NOT_BEGIN_WITH] = _('Does not begin with')
                string_ops[FilterOperators.STR_END_WITH] = _('End with')
                string_ops[FilterOperators.STR_NOT_END_WITH] = _('Does not end with')

            result = {
                'success': True,
                'data': data,
                'errorCode': None,
                'message': None,
                'params': None,
                'stackTrace': None
            }
            return jsonify(result)
    return jsonify({'success': False})


@api.route('/api/v1/datasources/<string:ds_connection_id>/fields')
@verify_token
def field_list_dispatch(ds_connection_id):
    """
    fields api dispatcher
    Args:
        ds_connection_id [string]:
        key of v2 `ptone_ds_connection_config` table to get
        v2-datasource-connection level config info
    Returns:
    """
    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    ds_id = v2_ds_connection_config.get(V2_CONST.DS_ID)

    if int(ds_id) < V2_CONST.DS_ID_THRESHOLD:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    ds_info = get_ds_info_by_ds_id(ds_id)
    assert ds_info

    parsed = parse_ds_connection_config(v2_ds_connection_config)

    if ds_info['type'] == DatasourceTypes.DB:
        # get fields from database table
        fields = get_table_fields(parsed.connection_id, parsed.table_id)
    else:
        # get fields from a SaaS connection
        fields = get_connection_fields(parsed.connection_id, {'path': parsed.profile_path})

    adapted = fields_result_data_adapt(fields)
    result = {
        'success': True,
        'data': adapted,
        'errorCode': None,
        'message': None,
        'params': None,
        'stackTrace': None
    }
    return jsonify(result)


@api.route('/api/v1/datasources/<string:ds_connection_id>/filter/fields')
@verify_token
def filter_field_list_dispatch(ds_connection_id):
    """
    fields api dispatcher
    Args:
        ds_connection_id [string]:
        key of v2 `ptone_ds_connection_config` table to get
        v2-datasource-connection level config info
    Returns:
    """

    # TODO: this endpoint is for field correlation in filter, which is not a
    # standard feature; should consider removing it

    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    v2_ds_id = v2_ds_connection_config.get(V2_CONST.DS_ID)

    if int(v2_ds_id) < V2_CONST.DS_ID_THRESHOLD:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    # dispatch new data-source, adapt req v2 to vx
    parsed = parse_ds_connection_config(v2_ds_connection_config)
    req_params = {'path': parsed.profile_path}

    # take connection_id as url param sending to business service,
    # do not need to remain in req body
    fields = get_connection_fields(parsed.connection_id, req_params)
    # adapt result vx to v2
    result_data = filter_fields_result_data_adapt(fields)
    result = {
        'success': True,
        'data': result_data
    }
    return jsonify(result)


@api.route('/api/v1/spaces/<string:space_id>/datasources/<string:ds_connection_id>/segments')
@verify_token
def segment_list_dispatch(space_id, ds_connection_id):
    """
    gets segments api dispatcher
    Args:
        ds_connection_id (string):
        key of v2 `ptone_ds_connection_config` table to get
        v2-datasource-connection level config info
    Returns:
    """
    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    v2_ds_id = v2_ds_connection_config.get(V2_CONST.DS_ID)
    ds_code = get_ds_code_by_id(int(v2_ds_id))

    if not ds_code:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    # dispatch new data-source, adapt req v2 to vx
    parsed = parse_ds_connection_config(v2_ds_connection_config)
    req_params = {'path': parsed.profile_path}
    # take connection_id as url param sending to business service,
    # do not need to remain in req body
    segments = get_connection_segments(parsed.connection_id, req_params)
    # adapt result vx to v2
    result_data = segments_result_data_adapt(segments, ds_code)
    result = {
        'success': True,
        'data': result_data,
    }
    return jsonify(result)


@api.route('/api/v1/segments/connection/<string:ds_connection_id>',
           methods=['POST'])
@verify_token
def segment_add_dispatch(ds_connection_id):
    """
    Add segment dispatcher
    Args:
        ds_connection_id:
        v2 ds connection id
    Returns:
    """
    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    v2_ds_id = v2_ds_connection_config.get(V2_CONST.DS_ID)
    ds_code = get_ds_code_by_id(int(v2_ds_id))
    connection_id = _helper_get_conn_from_config(v2_ds_connection_config)
    if ds_code not in get_ds_code_list():
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/' \
          f'connections/{connection_id}/segment?ds_code={ds_code}'
    response_data = post_json(url, headers=get_headers(), body=request.json)
    response_data["segmentId"] = response_data.get("id")
    result = {
        "success": True,
        "data": response_data
    }
    return jsonify(result)


@api.route('/api/v1/segments/<string:segment_id>/'
           'connection/<string:ds_connection_id>',
           methods=METHODS)
@verify_token
def segment_request_dispatch(segment_id, ds_connection_id):
    """
    Single segment object read,update,delete
    Args:
        segment_id: id
        ds_connection_id: ds connection id
    Returns:
    """
    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    v2_ds_id = v2_ds_connection_config.get(V2_CONST.DS_ID)
    ds_code = get_ds_code_by_id(int(v2_ds_id))
    connection_id = _helper_get_conn_from_config(v2_ds_connection_config)
    if ds_code not in get_ds_code_list():
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/' \
          f'connections/{connection_id}/segment?id={segment_id}'
    response = proxy(request, url)
    response_data = response.get_json()
    if response_data and "id" in response_data.keys():
        response_data["segmentId"] = response_data.get("id")
    result = {
        "success": True,
        "data": response_data
    }
    return jsonify(result)


@api.route('/api/v1/datasources/<string:ds_connection_id>/segments/fields')
@verify_token
def segment_field_list_dispatch(ds_connection_id):
    """dispatch segment field list url"""
    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    v2_ds_id = v2_ds_connection_config.get(V2_CONST.DS_ID)
    ds_code = get_ds_code_by_id(int(v2_ds_id))

    if ds_code not in get_ds_code_list():
        result = proxy_raw(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    else:
        parsed = parse_ds_connection_config(v2_ds_connection_config)
        req_params = {'path': parsed.profile_path}
        fields = get_connection_fields(parsed.connection_id, req_params)

        # filter out fields that don't allow segments
        def _filter(node):
            children = node.get('children')
            if children:
                node['children'] = list(filter(None, (_filter(child) for child in children)))
                return node
            else:
                return node if node.get('allowSegment') else None
        fields = list(filter(None, (_filter(field) for field in fields)))

        adapted = fields_result_data_adapt(fields)
        result = {
            'success': True,
            'data': adapted
        }
    return jsonify(result)


@api.route('/api/v1/panels/<string:panel_id>/profiles')
@verify_token
def profile_list_dispatch(panel_id):
    """
     Merges profiles list from legacy v3 service with new vnext datasources.
    """

    default_profile = {}
    profile_list = []

    # get profile list list from v3
    old_result = proxy_raw(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    if old_result.status_code == HTTPStatus.OK:
        body = old_result.json()
        if body and 'data' in body:
            profile_list.extend(body['data'].get('profileList') or [])
            default_profile = body['data'].get('defaultProfile') or {}

    vx_profiles = profiles_data_adapt(panel_id)
    if vx_profiles:
        profile_list.extend(vx_profiles['profiles'])
        if default_profile.get('count', 0) < vx_profiles['default_profile']['count']:
            default_profile = vx_profiles['default_profile']
    profile_ids = []

    def _profile_remove_duplication(profile):
        _ = str(profile['dsId']) + profile['profileId']
        if _ not in profile_ids:
            profile_ids.append(_)
            return True
        return False

    new_profiles = filter(_profile_remove_duplication, profile_list)
    result_data = {
        'defaultProfile': default_profile,
        'profileList': list(new_profiles)
    }
    result = {'success': True, 'data': result_data}

    return jsonify(result)


@api.route('/api/v3/ds/<string:ds_code>/accounts', methods=['GET'])
@verify_token
def connection_account(ds_code):
    """
    get accounts for connection

    Args:
        ds_code: datasource code
    Returns: [list]
    """
    if ds_code in get_ds_code_list():
        user_id = request.headers.get('UID')
        space_id = request.headers.get('SpaceId')
        resp = get_connections(user_id=user_id, space_id=space_id, ds_code=ds_code)
        result = [{
            'accountInfo': connection['name'],
            'authType': 'form',
            'connectionTime': connection['created_at'],
            'dataBaseName': None,
            'dataSetCount': 0,
            'dataSourceCode': connection['ds_code'],
            'dataSyncStatusValue': 0,
            'id': connection['id'],
            'instanceId': connection['id'],
            'isDataSet': False,
            'isDismiss': False,
            'userName': 'Datadeck API',
            'widgetCount': 0
        } for connection in resp]
        return jsonify({'data': result, 'success': True,
                        'errorCode': None, 'message': None,
                        'params': None, 'stackTrace': None})
    return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')


@api.route('/api/v1/widgets/data/preview', methods=METHODS)
def data_preview_dispatch():
    """
    data api dispatch
    Returns:

    """
    req_body = request.json
    ds_connection_id = req_body.get('dsConnectionId')
    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    v2_ds_id = v2_ds_connection_config.get(V2_CONST.DS_ID)
    ds_code = get_ds_code_by_id(int(v2_ds_id))
    if not ds_code:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    req_body['noCache'] = True
    req_body['isEtl'] = request.args.get("isEtl") == "true"
    result = {
        'success': True,
        'data': make_widget_data(req_body,
                                 v2_ds_connection_config,
                                 request.headers.get(CommonHeaders.TIMEZONE),
                                 request.headers.get(CommonHeaders.LOCALE, 'en_US')
                                 )
    }
    return jsonify(result)


@api.route('/api/v1/datasources/<string:space_id>/<string:ds_id>/accounts')
@verify_token
def account_list_dispatch(space_id, ds_id):
    """
    Dispatches access to connection account information
    Args:
        space_id: space id
        ds_id: dataSource dsId

    Returns: account list

    """
    ds_code = get_ds_code_by_id(int(ds_id))
    if not ds_code:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    connection_list = get_connections(space_id=space_id, ds_code=ds_code)
    result = connection_account_data_adapt(connection_list)
    return jsonify(result)


@api.route('/api/v1/datasources/<string:ds_id>/configurations')
@verify_token
def configurations_dispatch(ds_id):
    """
    Dispatches get configurations information
    Args:
         ds_id: dataSource dsId

    Returns: configuration

    """
    ds_code = get_ds_code_by_id(int(ds_id))
    if not ds_code:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    locale = request.headers.get(CommonHeaders.LOCALE)
    adapted_config = get_datasource_config_adapted(ds_code, locale)
    if adapted_config:
        return jsonify({'success': True, 'data': adapted_config})
    else:
        raise ServiceError('Unable to get datasource config')


def _adapt_hierarchy_items(profiles, parent_id_list=None):
    data_item = []
    for item in profiles:
        id_list = []
        if parent_id_list:
            id_list.extend(parent_id_list)
        id_list.append(item["id"])
        child_list = None
        is_leaf = not item["hasChild"]
        if item["hasChild"]:
            child_list = _adapt_hierarchy_items(item["children"], id_list)
        # For legacy v2 ga connection that only have last id which is used by FE to find
        legacy_id = [x if idx == len(id_list) -1 else "" for idx, x in enumerate(id_list)]
        data_item.append(
            {
                "id": json.dumps(id_list),
                PROFILE_ID_FIELD_NAME : json.dumps(legacy_id),
                "name": item["name"],
                "parent": None,
                "extra": None,
                "folderId": None,
                "leaf": is_leaf,
                "child": child_list})
    return data_item


def _adapt_table_items(tables):
    # tables are organized under database nodes, so we
    # first build a sorted list of databases
    databases = list(set(table['database'] for table in tables))
    databases.sort()
    items = [{'id': database,
              'name': database,
              'parent': None,
              'extra': None,
              'folderId': None,
              'leaf': False,
              'child': []} for database in databases]

    # then add tables under corresponding database nodes
    for table in tables:
        database = next((item for item in items if item['name'] == table['database']))
        database['child'].append({'id': json.dumps([table['database'], table['id']]),
                                  'name': table['name'],
                                  'parent': None,
                                  'extra': None,
                                  'folderId': None,
                                  'leaf': True})
    return items


@api.route('/api/v1/commands/recipient', methods=['POST'])
@verify_token
def commands_recipient_dispatch():
    """
    Dispatches commands recipient
    """
    body_data = request.get_json()
    command, params, provider = \
        body_data['id'], body_data['params'], body_data['provider']

    if provider not in get_ds_code_list():
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    if command == 'profile':
        params = body_data.get('params')
        assert params, 'Missing params in request body'

        # get hierarchy from downstream and adapt
        conn_id = params["account.id"]
        result = get_connection_hierarchy(conn_id, [], True)
        return jsonify({
            'success': True,
            'data': {
                'dataType': 'tree',
                'isDisplay': True,
                'isNeedTranslateI18nCode': False,
                'isOnlyTranslateName': False,
                'uniqueField': PROFILE_ID_FIELD_NAME,
                'value': _adapt_hierarchy_items(result['items'])
            }})

    if command == 'table':
        params = body_data.get('params')
        assert params, 'Missing params in request body'

        # get hierarchy from downstream and adapt
        conn_id = params["account.id"]
        tables = get_connection_tables(conn_id)
        return jsonify({
            'success': True,
            'data': {
                'dataType': 'tree',
                'isDisplay': True,
                'isNeedTranslateI18nCode': False,
                'isOnlyTranslateName': False,
                'value': _adapt_table_items(tables)
            }})

    if command == 'dimensionValues':
        ds_connection_id = params.get('dsConnectionId')
        v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
        result = {
            'success': True,
            'data': {
                'dataType': 'list',
                'isDisplay': True,
                'isNeedTranslateI18nCode': False,
                'isOnlyTranslateName': False,
                'value': make_widget_data_filter_selections(params,
                                                            v2_ds_connection_config,
                                                            request.headers.get("Timezone"))
            }
        }
        return jsonify(result)
    raise NotImplementedError("Not handle vx command %s yet" % command)


@api.route('/api/v1/commands/panels/filters/fieldValue', methods=['POST'])
@verify_token
def commands_panels_filter_dispatch():
    """
    Dispatches panel filter commands(for global filter)
    """
    body_data = request.get_json()['command']

    command, params, provider = \
        body_data['id'], body_data['params'], body_data['provider']

    if provider not in get_ds_code_list():
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    if command == 'dimensionValues':
        ds_connection_id = params.get('dsConnectionId')
        v2_ds_connection_config = get_v2_connection_config(ds_connection_id)

        if 'time' not in params:
            # default date range for global filter field selections fetching
            params['time'] = V2_CONST.DEFAULT_GLOBAL_FILTER_DATERANGE_FOR_FIELD_SELECTIONS
        value = make_widget_data_filter_selections(params,
                                                   v2_ds_connection_config,
                                                   request.headers.get("Timezone"))
        result = {
            'success': True,
            'data': {
                'dataType': 'list',
                'isDisplay': True,
                'isNeedTranslateI18nCode': False,
                'isOnlyTranslateName': False,
                'value': value
            }
        }
        return jsonify(result)
    raise NotImplementedError("Not handle vx command %s yet" % command)


@api.route('/api/v2/calculatedFields/fields/datasources/<string:ds_connection_id>')
@verify_token
def calculate_field_candidates_dispatch(ds_connection_id):
    """Dispatches get calculate field candidate field list url"""
    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    ds_id = v2_ds_connection_config.get("dsId")
    ds_code = get_ds_code_by_id(int(ds_id))
    if not ds_code:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    parsed = parse_ds_connection_config(v2_ds_connection_config)
    fields = get_connection_fields(parsed.connection_id,
                                   {'path': parsed.profile_path})
    fields = calculated_field_candidates_filter(fields)

    result = {
        'success': True,
        'data': fields_result_data_adapt(fields)
    }
    return jsonify(result)


@api.route('/api/v2/spaces/<string:space_id>/datasources/'
           '<string:ds_connection_id>/calculatedFields')
@verify_token
def calculate_field_list_dispatch(space_id, ds_connection_id):
    """Dispatches get calculate field list url"""
    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    ds_id = v2_ds_connection_config.get("dsId")
    ds_code = get_ds_code_by_id(int(ds_id))
    if not ds_code:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    connection_id = _helper_get_conn_from_config(v2_ds_connection_config)
    cal_fields = get_connection_calculated_fields(connection_id)
    return jsonify(calculated_field_data_adapt(cal_fields))


# pylint: disable=inconsistent-return-statements
@api.route('/api/v2/calculatedFields', methods=['POST'])
@api.route('/api/v2/calculatedFields/<string:calculated_field_id>',
           methods=['GET', 'PUT', 'DELETE'])
@verify_token
def calculated_field_dispatch(calculated_field_id=None):
    """dispatches calculated field create/delete/update/get urls"""
    if request.method in ['POST', 'PUT']:
        payload = request.json
        ds_connection_id = payload['dsConnectionId']
        v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
        ds_id = v2_ds_connection_config.get("dsId")
        ds_code = get_ds_code_by_id(int(ds_id))
        if not ds_code:
            return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
        connection_id = _helper_get_conn_from_config(v2_ds_connection_config)
        params = calculated_field_params_parse(payload)
        if request.method == 'PUT':
            assert calculated_field_id is not None
            result = update_calculated_field(connection_id, calculated_field_id, params)
        else:
            result = create_calculated_field(connection_id, params)
        return jsonify(calculated_field_data_adapt(result))
    elif request.method == 'DELETE':
        assert calculated_field_id is not None
        cal_field = get_connection_calculated_field(calculated_field_id)
        if not cal_field:
            return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
        delete_calculated_field(calculated_field_id, request.json)
        return "", HTTPStatus.NO_CONTENT
    elif request.method == 'GET':
        assert calculated_field_id is not None
        cal_field = get_connection_calculated_field(calculated_field_id)
        if not cal_field:
            return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
        return jsonify(calculated_field_editor_data_adapt(cal_field))


@api.route('/api/v2/calculatedFields/validate', methods=['POST'])
@verify_token
def calculate_field_validate():
    """Dispatches get calculated field validating url"""
    payload = request.json
    ds_connection_id = payload['dsConnectionId']
    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    ds_id = v2_ds_connection_config.get("dsId")
    ds_code = get_ds_code_by_id(int(ds_id))
    if not ds_code:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    connection_id = _helper_get_conn_from_config(v2_ds_connection_config)

    params_raw = calculated_field_params_parse(payload)
    params = {
        'expression': params_raw['expression'],
        'keys': [f['id'] for f in params_raw['candidates']]
    }
    result = validate_connection_calculated_field(connection_id, params)
    if result.get('ok'):
        return jsonify({
            'success': True,
            'data': True
        })
    return jsonify({
        'success': True,
        'data': False
    })


@api.route('/api/v1/datasources/id/<int:ds_id>')
@verify_token
def get_single_data_source_dispatch(ds_id):
    """Dispatches get single data source url"""
    ds_code = get_ds_code_by_id(ds_id)
    if not ds_code:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    data_source = get_datasource_info(ds_code)

    conn_count = len(get_connections(space_id=request.headers.get("SpaceId"), ds_code=ds_code))
    data_source["connectionCount"] = conn_count
    result = ds_single_data_adapt(data_source)
    return jsonify({"success": True, "data": result})


@api.route('/api/v2/spaces/<string:space_id>/resources/move/'
           '<int:old_uid>/to/<int:new_uid>', methods=['POST'])
@verify_token
def resource_transfer(space_id, old_uid, new_uid):
    """
    Before deleting, you can transfer all data (Dashboards, Folders, Data sources)
    belonging to this member to another member.
    """
    response = proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    if response.status_code == HTTPStatus.NO_CONTENT:
        bussiness_url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/spaces/resources/transfer'
        vnext_resp = proxy(request, bussiness_url)
        if vnext_resp.status_code != HTTPStatus.OK:
            logging.error("Transfer data vNext business service exception.")
            return jsonify({"success": False})
    else:
        logging.error("Transfer data v2 service exception.")
    return response


@api.route('/api/v2/templet/panel', methods=['GET'])
def panel_template_dispatch():
    """
    Filter out panels containing already migrated datasources
    """
    response = proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    templates = response.json['data']
    result = []
    if templates:
        result = [t for t in templates if not
                  any((ds for ds in t['dsInfoList'] if ds['id'] in MIGRATED_DATASOURCES))]

    return jsonify({"success": True, "data": result})


@api.route('/api/v1/<path:path>', methods=METHODS)
@api.route('/api/v2/<path:path>', methods=METHODS)
@api.route('/api/v3/<path:path>', methods=METHODS)
@verify_token
def middle_dispatch(path):
    """Dispatches all other v1/v2/v3 requests unchanged"""
    return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')


@api.route('/api/v3adapter/<path:path>', methods=METHODS)
@verify_token
def authv2_dispatch(path):
    '''Dispatches all v3 adapter requests unchanged'''
    return proxy(request, f'{app.config["AUTH_V2_URL"]}{request.path}')


@api.route('/dataset-service/<path:path>', methods=METHODS)
@api.route('/zuul/<path:path>', methods=METHODS)
@api.route('/datadeck-app-datasource/<path:path>', methods=METHODS)
@api.route('/user-service/<path:path>', methods=METHODS)
@api.route('/business-service/<path:path>', methods=METHODS)
@verify_token
def ds_gateway_dispatch(path):
    '''All other dsgateway dispatches, unchanged'''
    return proxy(request, f'{app.config["DS_GATEWAY_URL"]}{request.path}')


def _helper_get_conn_from_config(v2_ds_connection_config):
    """get vx business connection id from ds connection config storing in v2 database"""
    return v2_ds_connection_config["config"][0].get("id")
