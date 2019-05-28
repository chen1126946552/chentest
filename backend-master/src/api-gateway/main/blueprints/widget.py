"""
Dispatch rules for widget services
"""

from __future__ import absolute_import

import logging
from copy import deepcopy

from flask import Blueprint
from flask import current_app as app
from flask import jsonify

# from app import executor
from common.http.proxy import proxy
from common.service.constants import CommonHeaders
from common.http.utils import ApiError
from common.http.executor import request_proxy as request
from common.service.constants import GraphType
from services.adaptors.common import (get_v2_connection_config,
                                      get_v2_widget_list,
                                      get_v2_widget,
                                      get_v2_slack_widget)
from services.adaptors.data import (make_widget_data,
                                    widget_data_websocket_adapt)
from services.adaptors.field import get_fields_id_name_map
from services.adaptors.segment import get_segments_id_name_map
from services.adaptors.global_filter import (global_date_range_parse,
                                             global_filters_parse,
                                             inject_global_date_range_into_widget_req_param,
                                             inject_global_filters_to_widget_req_param)
from services.downstream import (get_datasource_config_adapted,
                                 ws_push_json,
                                 get_connection_fields,
                                 get_connection_segments)
from services.exception import ServiceError
from utils.system_constant import get_ds_code_by_id, get_ds_code_list
from utils.ds_connection_config_parser import parse
from .token import verify_token

api = Blueprint('widget', __name__)
logger = logging.getLogger(__name__)

COMMON_REQUEST_ERROR_CODE = 'MSG_BAD_REQUEST'


# pylint: disable=unused-argument


@api.route('/api/v1/widgets/<string:ds_cid>/datasources/configurations')
@verify_token
def widget_ds_connection_configurations_dispatch(ds_cid):
    """
    Dispatch and process the data source connection configuration
    """
    ds_connection_config = get_v2_connection_config(ds_cid)
    ds_id = ds_connection_config.get("dsId")
    ds_code = get_ds_code_by_id(int(ds_id))
    if ds_code not in get_ds_code_list():
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')

    locale = request.headers.get(CommonHeaders.LOCALE)
    adapted_config = get_datasource_config_adapted(ds_code, locale)
    if adapted_config:
        return jsonify({'success': True, 'data': adapted_config})
    else:
        raise ServiceError('Unable to get datasource config')


@api.route('/api/v1/widgets/batchWidgetData/<string:panel_id>/<string:websocket_id>',
           methods=['POST'])
@verify_token
def widget_batch_fetch_data_dispatch(panel_id, websocket_id):
    """
    Dispatch widget fetch data
    """
    # pylint: disable=too-many-locals
    locale = request.headers.get('Accept-Language', 'en_US')
    widget_list = get_v2_widget_list(panel_id).get("widgetList")
    is_exists_v2_ds = False
    if widget_list:
        for widget in widget_list:
            if _is_vnext_widget(widget):
                _push_widget_data_by_websocket(widget, locale, websocket_id)
                # executor.submit(_push_widget_data_by_websocket, widget, locale, websocket_id)
            else:
                is_exists_v2_ds = True
    if is_exists_v2_ds:
        proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    return jsonify({"success": True, "data": 1})


@api.route('/api/v1/widgets/<string:widget_id>/data',
           methods=['POST'])
@verify_token
def widget_get_data_async(widget_id):
    """Single widget fetch data by websocket"""
    websocket_id = request.args.get("sign")
    locale = request.headers.get('Accept-Language', 'en_US')
    widget = get_v2_widget(widget_id)
    w_id = widget.get('widgetId')
    if _is_vnext_widget(widget) and widget_id == w_id:
        i18n_widget_params(widget, locale)
        widget_fetch_data(widget, websocket_id)
        return jsonify({"success": True, "data": 1})
    else:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')


@api.route('/api/slack/v1/widgets/<string:widget_id>', methods=['GET'])
def slack_data_dispatch(widget_id):
    """
    get widget data and some extra information for internal service slack/notification/alert
    """
    user_id = request.headers.get('userId')
    token = request.headers.get('token')
    slack_widget = get_v2_slack_widget(widget_id, user_id, token)

    widget = slack_widget.get('widgetParams', {})
    user_info = slack_widget.get('userInfo', {})
    global_filters = slack_widget.get('globalFilters', [])
    setting = slack_widget.get('setting')

    w_id = widget.get('widgetId')
    if _is_vnext_widget(widget) and widget_id == w_id:
        i18n_widget_params(widget, user_info.get('lang'))
        widget_data = widget_fetch_data(widget, None, False,
                                        params={'global_filters': global_filters,
                                                'week_start_day': user_info.get('weekStartAt'),
                                                'locale': user_info.get('lang'),
                                                'timezone': user_info.get('timezone')
                                                })
        return jsonify(
            {"success": True, "data": {'data': widget_data,
                                       'setting': setting,
                                       'userInfo': user_info}
             }
        )
    else:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')


@api.route('/api/v2/widgets/<string:widget_id>/data',
           methods=['POST'])
@verify_token
def widget_get_data_sync(widget_id):
    """Single widget fetch data"""
    locale = request.headers.get('Accept-Language', 'en_US')
    widget = get_v2_widget(widget_id)
    w_id = widget.get('widgetId')
    if _is_vnext_widget(widget) and widget_id == w_id:
        i18n_widget_params(widget, locale)
        data = widget_fetch_data(widget, None, False)
        return jsonify({"success": True, "data": data})
    else:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')


@api.route('/api/v1/widgets/<string:widget_id>/data/temp',
           methods=['POST'])
@verify_token
def temp_widget_get_data_dispatch(widget_id):
    """Single temp widget fetch data"""
    req_params = request.json
    widget = req_params['widget']
    ds_code = widget['dsCode']
    if ds_code not in get_ds_code_list():
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    else:
        data = widget_fetch_data(widget, None, False)
        return jsonify({"success": True, "data": data})


@api.route('/api/v1/widgets/<string:widget_id>/data/export',
           methods=['POST'])
@verify_token
def widget_export_data_dispatch(widget_id):
    """Single temp widget fetch data"""
    widget = get_v2_widget(widget_id)
    ds_code = widget['dsCode']
    if ds_code not in get_ds_code_list():
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    else:
        graph_type = GraphType(widget['graphType'])
        # If not highchart, use table instead.
        if not graph_type.is_highchart():
            widget['graphType'] = 'table'
        original_data = widget_fetch_data(widget, None, False)
        data = widget_export_data(widget, original_data)
        return jsonify({"success": True, "data": data})


def _push_widget_data_by_websocket(widget, locale, websocket_id):
    i18n_widget_params(widget, locale)
    widget_fetch_data(widget, websocket_id)

def _get_header_field(fields, metrics_amounts_map):
    """
    Get header fields with dimension and legend first
    Use metrics_amounts_map to get metrics to include comparsion fields
    """
    result = []
    dimension = next((f for f in fields if f['type'] == 'xAxis'), None)
    if dimension:
        result.append(dimension)

    legend = next((f for f in fields if f['type'] == 'legend'), None)
    if legend:
        result.append(legend)

    result.extend([{'name': f['showName'], 'uuid': f['key'], 'type': 'yAxis'}
                   for f in metrics_amounts_map.values()])

    return result


def _find_field_index(fields, key):
    return [i for i, f in enumerate(fields) if f['uuid'] == key][0]


# pylint: disable=too-many-locals
def widget_export_data(widget, original_data):
    """Convert widget data for csv export"""
    graph_type = GraphType(widget['graphType'])

    if not graph_type.is_highchart():
        return original_data

    header_fields = _get_header_field(widget['fields'], original_data['metricsAmountsMap'])

    if graph_type.is_map():
        map_type = widget['map']['mapType']
        map_field_name = 'Country' if map_type == 'world' else 'Region'
        map_key = original_data['data'][0]['dimensionsKey']
        header_fields.insert(0, {'name': map_field_name, 'uuid': map_key, 'type': 'xAxis'})

    column_count = len(header_fields)
    has_dimension = any([f for f in header_fields if f['type'] == 'xAxis'])
    has_legend = any([f for f in header_fields if f['type'] == 'legend'])
    dimension_map = {}
    data = []

    for serie in original_data['data']:
        if has_legend:
            legend_value = serie['dimensionsId']
        metric_index = _find_field_index(header_fields, serie['metricsKey'])
        for row in serie['rows']:
            if not has_dimension and not has_legend:
                if not data:
                    data = [[None] * column_count]
                data[0][metric_index] = row[1]
            else:
                if has_dimension and has_legend:
                    key = (row[0], legend_value)
                elif has_legend:
                    key = legend_value
                else:
                    key = row[0]

                existing_row = dimension_map.get(key)
                if existing_row:
                    existing_row[metric_index] = row[1]
                else:
                    new_row = [None] * column_count
                    if has_dimension and has_legend:
                        new_row[0:2] = key
                    else:
                        new_row[0] = key
                    new_row[metric_index] = row[1]
                    data.append(new_row)
                    dimension_map[key] = new_row

    header_names = [f['alias'] if f.get('alias') else f['name'] for f in header_fields]
    data.insert(0, header_names)

    dimension_key = ','.join([f['uuid'] for f in header_fields if f['type'] in ['legend', 'xAxis']])
    metric_key = ','.join([f['uuid'] for f in header_fields
                           if f['type'] not in ['legend', 'xAxis']])

    variable_data = original_data['data'][0]
    variable_data['rows'] = data
    variable_data['dimensionsKey'] = dimension_key
    variable_data['metricsKey'] = metric_key

    original_data['data'] = [variable_data]
    return original_data


def widget_fetch_data(widget, websocket_id, is_async=True, params=None):
    """
        Widget data push
    Args:
        widget: Panel id
        websocket_id: websocket id
        is_async: is async push data
    Returns:
    """
    no_cache = request.args.get('no-cache') == 'true'

    if params is None:
        params = {}

    if request.method == 'POST':
        req_params = request.json
        global_filters = global_filters_parse(req_params.get('panelFilterComponents') or [])
        global_date_range = global_date_range_parse(req_params.get('panelTimeComponent') or {})
        drill_down_filters = req_params.get('drillDownFilterComponents') or []
    elif params:
        global_filters = global_filters_parse(params.get('global_filters') or [])
        global_date_range = global_date_range_parse(params.get('global_date_range') or {})
        drill_down_filters = params.get('drill_down_filters') or []
    else:
        global_filters = {}
        global_date_range = {}
        drill_down_filters = []

    ds_connection_id = widget.get("dsConnectionId")
    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    # inject global filters
    global_filter_key = widget['dsCode'] + '-' + v2_ds_connection_config['config'][-1]['id']
    current_ds_conn_g_filters = global_filters.get(global_filter_key)
    if current_ds_conn_g_filters:
        for g_f in current_ds_conn_g_filters:
            inject_global_filters_to_widget_req_param(widget, g_f)
    # inject global date range
    if global_date_range:
        inject_global_date_range_into_widget_req_param(widget, global_date_range)

    if drill_down_filters:
        for f in drill_down_filters:
            inject_global_filters_to_widget_req_param(widget, f)

    req_body = deepcopy(widget)
    req_body.update({
        'noCache': no_cache,
        'panelFilterComponents': global_filters,
        'panelTimeComponent': global_date_range
    })
    try:
        data = make_widget_data(req_body, v2_ds_connection_config,
                                params.get('timezone') or request.headers.get(
                                    CommonHeaders.TIMEZONE),
                                params.get('locale') or request.headers.get(CommonHeaders.LOCALE),
                                week_start_day=params.get('week_start_day'))
    except ApiError as err:
        data = {
            'status': 'failed',
            'errorCode': err.error_code,
            'debugMessage': err.debug_message,
            'errorMsg': err.message,
            'widgetId': widget.get('widgetId')
        }
        logger.exception('Widget fetch data api error.')
    except ServiceError as err:
        data = {
            'status': 'failed',
            'errorCode': err.error_code,
            'errorMsg': err.message,
            'widgetId': widget.get('widgetId')
        }
        logger.exception('Widget fetch data api error.')
    except Exception as err:  # pylint: disable=broad-except
        data = {
            'status': 'failed',
            'errorCode': COMMON_REQUEST_ERROR_CODE,
            'debugMessage': str(err),
            'widgetId': widget.get('widgetId')
        }
        logger.exception('Widget fetch data error.')
    if not is_async:
        return data

    ws_data = widget_data_websocket_adapt(data, websocket_id)
    ws_push_json(websocket_id, ws_data)
    return None


@api.route('/api/v1/widgets/<string:widget_id>', methods=['GET'])
@verify_token
def widget_dispatch(widget_id):
    """widget params get api"""
    locale = request.headers.get('Accept-Language')
    if not locale:
        locale = 'en_US'
        logger.warning("Cannot get locale info from request headers")
    widget_params = get_v2_widget(widget_id)
    if _is_vnext_widget(widget_params):
        i18n_widget_params(widget_params, locale)
    return jsonify({
        "success": True,
        "data": widget_params
    })


def _get_connection_and_path(widget_params):
    """get business connection and profile path for a widget"""
    ds_id = widget_params.get('dsId')
    ds_code = get_ds_code_by_id(ds_id)
    if not ds_code:
        logger.warning("%s is not a vnext datasource, cannot get it's connection path", ds_id)
        return None
    ds_connection_id = widget_params.get('dsConnectionId')
    v2_connection_config = get_v2_connection_config(ds_connection_id)
    parsed = parse(v2_connection_config)
    path = parsed.profile_path
    business_conn_id = parsed.connection_id
    return {'connection_id': business_conn_id, 'profile_path': path}


def _get_fields_for_widget(widget_params, locale):
    """get fields for a widget"""
    fields = []
    connection_path = _get_connection_and_path(widget_params)
    if not connection_path:
        return fields
    business_conn_id = connection_path['connection_id']
    path = connection_path['profile_path']
    try:
        fields = get_connection_fields(business_conn_id, req_params={'path': path},
                                       headers={'Accept-Language': locale})
    except ApiError as api_e:
        if api_e.error_code == 'ENTITY_NOT_FOUND':
            return fields
        else:
            raise
    return fields


def _get_segments_for_widgets(widget_params, locale):
    """get segments for a widget"""
    connection_path = _get_connection_and_path(widget_params)
    if not connection_path:
        return []
    business_conn_id = connection_path['connection_id']
    path = connection_path['profile_path']

    return get_connection_segments(business_conn_id, req_params={'path': path},
                                   headers={'Accept-Language': locale})


def i18n_widget_params(widget_params, locale):
    """
    globalization for saved widget params
    Args:
        widget_params(dict): widget params
        locale(string): current request's language set

    Returns(no-return):
        replace field's name in widget params with its i18n name in place

    """
    fields = _get_fields_for_widget(widget_params, locale)
    if not fields:
        logger.warning("Can not get locale fields back.")
        return
    id_name_map = get_fields_id_name_map(fields)
    _widget_fields_name_replace(widget_params, id_name_map)
    if widget_params.get('drillDownWidgets'):
        drill_down_widgets = widget_params['drillDownWidgets']
        for drd_widget in drill_down_widgets:
            _widget_fields_name_replace(drd_widget, id_name_map)

    if widget_params.get('segment'):
        segments = _get_segments_for_widgets(widget_params, locale)
        if not segments:
            logger.warning("Can not get locale segments back.")
        id_name_map_for_seg = get_segments_id_name_map(segments)
        _widget_segment_name_replace(widget_params, id_name_map_for_seg)


def _widget_fields_name_replace(widget_params, id_name_map):
    """
    replace field's name in widget params with its i18n name in place
    Args:
        widget_params(dict): widget params
        id_name_map(dict): field_id: field_i18n_name

    Returns(no-return):
    """
    i18n_fields_in_metric_dimension = widget_params['fields'] or []
    i18n_fields_in_filter = widget_params['filters'] or []

    if widget_params.get('compareWithPreviousPeriod'):
        i18n_fields_in_cwp = widget_params['compareWithPreviousPeriod'].get('compareFields') or []
    else:
        i18n_fields_in_cwp = []

    i18n_all_fields = i18n_fields_in_metric_dimension \
                      + i18n_fields_in_filter \
                      + i18n_fields_in_cwp
    for field in i18n_all_fields:
        field['name'] = id_name_map.get(field['id'], field['name'])


def _widget_segment_name_replace(widget_params, id_name_map):
    """
    replace segment's name in widget params with its i18n name in place
    Args:
        widget_params(dict): widget params
        id_name_map(dict): segment_id: segment_i18n_name

    Returns(no-return):
    """
    segment = widget_params.get('segment')
    if segment:
        segment['name'] = id_name_map.get(segment['id'], segment['name'])


@api.route('/api/v1/panels/<string:panel_id>/widgetList', methods=['GET'])
@verify_token
def widget_list_dispatch(panel_id):
    """widget list api dispatch"""
    locale = request.headers.get('Accept-Language')
    if not locale:
        locale = 'en_US'
        logger.warning("Cannot get locale info from request headers")
    widget_list_resp = get_v2_widget_list(panel_id)
    for widget_param in widget_list_resp.get('widgetList') or []:
        if _is_vnext_widget(widget_param):
            i18n_widget_params(widget_param, locale)

    return jsonify({
        "success": True,
        "data": widget_list_resp
    })


def _is_vnext_widget(widget_param):
    """
    check if widget is under vnext datasource(can find ds_code in vnext cache)
    Args:
        widget_param(dict): widget params

    Returns(boolean): if a vnext widget

    """
    return bool(get_ds_code_by_id(int(widget_param.get('dsId') or -1)))
