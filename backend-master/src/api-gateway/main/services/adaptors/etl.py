"""etl adapter"""

from __future__ import absolute_import

import logging
from flask import current_app as app

from services.exception import V2AdaptorError
from common.http.utils import get_json
from utils.system_constant import (
    get_ds_code_by_id,
)
logger = logging.getLogger(__name__)

# pylint: disable=unused-argument


def get_v2_connection_config_by_id(ds_con_id):
    """ get v2 connection config"""
    url = f'{app.config["MIDDLE_URL"]}/api/v1/connections/config/{ds_con_id}'
    resp = get_json(url)
    if not resp or not resp.get("success"):
        raise V2AdaptorError("Get v2 connection config info failed")
    return resp["data"]


def get_etl_datasource(datasource_id):
    """Gets etl widget datasource config"""
    bussiness_url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/etl/datasources/{datasource_id}'
    respon = get_json(bussiness_url, raise_on_error=False)
    return respon


def widget_config_adapt(datasource_id):
    """Etl datasource config"""
    config_data = get_etl_datasource(datasource_id)
    if not config_data:
        return None
    connection_config = get_v2_connection_config_by_id(
        config_data.get("widget_connection_config_id")
    )
    ds_id = int(connection_config.get("dsId"))
    ds_code = get_ds_code_by_id(ds_id)
    return {
        "panelId": None,
        "widgetId": config_data.get("id"),
        "spaceId": config_data.get("space_id"),
        "dsConnectionId": config_data.get("widget_connection_config_id"),
        "name": config_data.get("name"),
        "graphType": "table",
        "sort": config_data.get("sort"),
        "filters": config_data.get("filters"),
        "pteSegments": config_data.get("segment"),
        "segment": config_data.get("segment"),
        "time": config_data.get("time"),
        "fields": config_data.get("fields"),
        "uid": None,
        "isTitleUpdate": None,
        "settings": None,
        "widgetType": "chart",
        "map": None,
        "sourceType": None,
        "isDemo": None,
        "isExample": None,
        "templetId": None,
        "isPreview": None,
        "targetValue": None,
        "toolData": None,
        "layout": None,
        "children": None,
        "disconnectMessage": None,
        "dsInfo": None,
        "description": None,
        "createTime": None,
        "panelUrl": None,
        "widgetTemplateConfig": None,
        "compareWithPreviousPeriod": None,
        "commentCount": None,
        "dsCode": ds_code,
        "dsId": ds_id,
        "spaceName": None,
        "datasetId": None,
        "datasourceId": config_data.get("id"),
        "language": config_data.get("language"),
        "timezone": config_data.get("timezone")
    }
