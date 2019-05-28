"""All classes/methods/tools to help to adapt to v2 `global components`"""

from utils.system_constant import get_ds_code_by_id, get_ds_info_by_ds_id
from .common import (
    get_v2_widget_list,
    get_v2_connection_config
)


def profiles_data_adapt(panel_id):
    """
    adapt profiles api to v2, for global filter function, frontend will request
    all profiles in a panel before displaying them to be chosen, a profile is supposed
    to be one ds connection config map that some widget(s) in this panel attached
    Args:
        panel_id (string): panel id
    Returns:
        (dict) an dict object that contains two item
             default_profile (dict): the profile attached most widgets in this panel
             profiles (list): all profiles in this panel, sorted according to their names
    """
    profiles = get_ds_conn_configs_in_panel(panel_id)
    if profiles:
        return {
            'default_profile': max(profiles, key=lambda item: item['count']),
            'profiles': profiles
        }
    return {}


def get_ds_conn_configs_in_panel(panel_id):
    """
    get vx ds connection configs in assigned panel
    Args:
        panel_id (string): panel's id
    Returns:
        (list) ds connection configs sorted according to their names
    """
    widget_list = get_v2_widget_list(panel_id).get("widgetList") or []
    ds_conn_configs_map = {}
    for widget in widget_list:
        ds_id = widget.get('dsId')
        #It might be a richtext box
        if not ds_id:
            continue
        ds_code = get_ds_code_by_id(int(ds_id))
        if ds_code:
            ds_connection_id = widget.get("dsConnectionId")
            if ds_connection_id not in ds_conn_configs_map:
                v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
                ds_conn_configs_map[ds_connection_id] = \
                    _profile_result_adapt(v2_ds_connection_config)
            else:
                ds_conn_configs_map[ds_connection_id]['count'] += 1

    return sorted(ds_conn_configs_map.values(), key=lambda v: v['profileName'])


def _profile_result_adapt(ds_conn_config):
    """adapt to v2's frontend"""
    ds_conn_id = ds_conn_config['dsConnectionId']
    ds_id = ds_conn_config['dsId']
    config = ds_conn_config['config']
    ds_name = get_ds_info_by_ds_id(ds_id)['name']
    ds_code = get_ds_code_by_id(ds_id)
    # profile is the last element in the path list
    profile_id = config[1]['id']

    account_name = config[0]['name']
    connection_id = config[0]['id']
    profile_name = config[1]['name']

    return {
        'accountName': account_name,
        'connectionId': connection_id,
        'count': 1,
        'dsCode': ds_code,
        'dsConnectionId': ds_conn_id,
        'dsId': ds_id,
        'dsName': ds_name,
        'id': '|'.join([profile_id, account_name, ds_code]),
        'isSupportCorrelateField': False,
        # profile is the last element in the path list
        'profileId': profile_id,
        'profileName': profile_name,
        'profilePath': ','.join([ds_name, account_name, profile_name])
    }


def global_filters_parse(global_filters):
    """
    when batch fetching data, parse v2 global filters to adapt vx
    Args:
        global_filters (list): v2 global filter list
    Returns:
        (dict) vx global filters map
            key (string): ds connection id
            value (list): vx filters
    """
    vx_global_filters = {}
    for g_f in global_filters:
        ds_id = g_f['settings']['profile']['dsId']
        ds_code = get_ds_code_by_id(ds_id)
        if ds_code:
            profile_id = g_f['settings']['profile']['profileId']
            ds_code_pid = '-'.join([ds_code, profile_id])
            vx_global_filters.setdefault(ds_code_pid, [])
            vx_global_filters[ds_code_pid].append(g_f['settings']['field'])
    return vx_global_filters


def inject_global_filters_to_widget_req_param(widget, _filter):
    """inject global filters into widget data request params"""
    widget['global_filter'] = True
    if widget.get('filters'):
        widget['filters'].append(_filter)
    else:
        widget['filters'] = [_filter]


def global_date_range_parse(gdr):
    """when batch fetching data, parse v2 global date range to adapt vx"""
    if not gdr:
        return {}
    return gdr.get('settings')


def inject_global_date_range_into_widget_req_param(widget, _dr):
    """inject global date range into widget data request params"""
    widget['time'] = _dr
    widget['global_time'] = True
