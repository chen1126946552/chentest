"""
 All COMMON classes/methods/tools to help to adapt v2 service and old frontend design
 in business level WOULD BE FOUND HERE.
"""
from uuid import uuid1
from flask import current_app as app
from flask import g
from common.http.utils import get_json, get_headers
from services.exception import V2AdaptorError


def get_v2_host():
    """return v2(middle) host without scheme"""
    v2_host = app.config.get('MIDDLE_URL').strip("/")
    if not v2_host:
        raise ValueError(f'Missing config item: MIDDLE_URL')
    return v2_host.replace("https://", '').replace("http://", '')


def _make_v2_headers():
    """get flask thread request headers, and fix then to adapt to v2 apis"""
    headers = get_headers()
    # need change host in headers to skip v2 domain check
    host = get_v2_host()
    headers.update({"Host": host})
    if "Spaceid" not in headers and "space_id" in g:
        headers["Spaceid"] = g.space_id

    # to adapt to v2's headers rule
    # need change custom header fields to handle flask header case change problem
    if 'uid'.capitalize() in headers:
        headers['UID'] = headers['uid'.capitalize()]
    if 'spaceid'.capitalize() in headers:
        headers['SpaceId'] = headers['spaceid'.capitalize()]
    if 'traceid'.capitalize() in headers:
        headers['TraceId'] = headers['traceid'.capitalize()]
    return headers


def make_v2_call_url(end_point, add_trace_id=False):
    """Gets URL to a downstream datasource service for a given ds_code"""
    v2_host = app.config.get('MIDDLE_URL').strip("/")
    if not v2_host:
        raise ValueError(f'Missing config item: V2_MIDDLE_URL')
    if not add_trace_id:
        return f'{v2_host}/{end_point.strip("/")}'
    return f'{v2_host}/{end_point.strip("/")}?traceId={add_trace_id}'


def get_current_space_id():
    """Get current request's space_id"""
    headers = _make_v2_headers()
    return headers.get('SpaceId')


def get_current_user_id():
    """Get current request's user_id"""
    headers = _make_v2_headers()
    return headers.get('UID')


def get_current_v2_user_info():
    """ get v2 user info with token info in current request lifecycle"""
    headers = _make_v2_headers()
    url = make_v2_call_url(f'api/v2/users', add_trace_id=headers.get("TraceId") or uuid1())
    resp = get_json(url, headers)
    if not resp or not resp.get("success"):
        raise V2AdaptorError("Get v2 user info failed")
    return resp["data"]


def get_current_v2_space_info():
    """ get v2 space info with token info in current request lifecycle"""
    headers = _make_v2_headers()
    url = make_v2_call_url(f'api/v2/spaces/{headers.get("SpaceId")}',
                           add_trace_id=headers.get("TraceId") or uuid1())
    resp = get_json(url, headers)
    if not resp or not resp.get("success"):
        raise V2AdaptorError("Get v2 space info failed")
    return resp["data"]


def get_v2_connection_config(ds_con_id):
    """ get v2 connection config"""
    headers = _make_v2_headers()
    url = make_v2_call_url(f'api/v1/connections/config/{ds_con_id}',
                           add_trace_id=headers.get("TraceId") or uuid1())
    resp = get_json(url, headers=headers)
    if not resp or not resp.get("success"):
        raise V2AdaptorError("Get v2 connection config info failed")
    return resp["data"]


def get_v2_widget_list(panel_id):
    """get v2 widget list by panel id"""
    headers = _make_v2_headers()
    url = make_v2_call_url(f'api/v1/panels/{panel_id}/widgetList',
                           add_trace_id=headers.get("TraceId") or uuid1())
    resp = get_json(url, headers=headers)
    if not resp or not resp.get("success"):
        raise V2AdaptorError("Get v2 connection config info failed")
    return resp["data"]


def get_v2_widget(widget_id):
    """get v2 widget by widget id"""
    headers = _make_v2_headers()
    url = make_v2_call_url(f'api/v1/widgets/{widget_id}',
                           add_trace_id=headers.get("TraceId") or uuid1())
    resp = get_json(url, headers=headers)
    if not resp or not resp.get("success"):
        raise V2AdaptorError("Get v2 widget failed: %s" % resp.get('message'))
    return resp["data"]


def get_v2_slack_widget(widget_id, user_id, token):
    """get v2 widget for special situation which the request is not from frontend,
    is from internal service with out user's token but a super token"""
    headers = {'userId': user_id, 'token': token}
    url = make_v2_call_url(f'api/slack/v1/widgets/{widget_id}/params')
    resp = get_json(url, headers=headers)
    if not resp or not resp.get("success"):
        raise V2AdaptorError("Get v2 widget failed: %s" % resp.get('message'))
    return resp["data"]
