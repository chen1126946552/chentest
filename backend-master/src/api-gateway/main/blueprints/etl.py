"""Dispatch etl services"""

from __future__ import absolute_import

import logging
from http import HTTPStatus

from flask import Blueprint, g
from flask import current_app as app
from flask import jsonify, request

from services.adaptors.constant import Constant as V2_CONST
from services.adaptors.common import get_v2_connection_config
from services.adaptors.data import (
    make_widget_data,
)
from services.adaptors.etl import (
    widget_config_adapt,
    get_v2_connection_config_by_id,
)
from common.http.proxy import proxy
from utils.system_constant import (
    get_ds_code_by_id,
    DataType,
    DatePeriod,
    Func,
)

from .token import verify_token

api = Blueprint('etl', __name__)
logger = logging.getLogger(__name__)

# pylint: disable=unused-argument

CALCULATED_FIELD_TYPE = ["yAxis", "leftYAxis", "rightYAxis"]
AGGREGATE_FUNC = ["SUM", "MAX", "MIN", "AVERAGE", "AVG", "COUNTA",
                  "COUNTUNIQUE", "D_COUNT", "STDEV", "VAR"]
NUMBER_TYPE_LIST = ["NUMBER", "DOUBLE", "FLOAT", "INTEGER", "LONG",
                    "PERCENT", "CURRENCY", "DURATION"]
DEFAULT_DATE_FORMAT = "yyyy-MM-dd'T'HH:mm:ss.SSSX"
ETL_FETCH_DATA_LIMITS = 100000


@api.route('/api/v3/ds/etl/dataset/datasource', methods=['POST'])
@verify_token
def etl_save_datasource_dispatch():
    """save etl datasource dispatch"""
    req_body = request.json
    ds_connection_id = req_body.get('dsConnectionId')
    v2_ds_connection_config = get_v2_connection_config(ds_connection_id)
    v2_ds_id = v2_ds_connection_config.get(V2_CONST.DS_ID)
    ds_code = get_ds_code_by_id(int(v2_ds_id))
    if not ds_code:
        return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    bussiness_url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/etl/datasources'
    respon = proxy(request, bussiness_url)
    result = {"success": False}
    if respon.status_code == HTTPStatus.OK:
        result = {"success": True, "data": {"datasourceId": respon.get_json().get("id")}}
    return jsonify(result)


@api.route('/api/v3/ds/etl/dataset/datasource/column/list', methods=['POST'])
@verify_token
def etl_column_list_dispatch():
    """etl column list dispatch"""
    datasource_id_list = request.json
    vnext_column_list = _get_column_name_list_by_datasource_id(datasource_id_list)
    v2_column_list = _get_v2_column_name_list()
    # Merge v2 to vNext results
    for vnext_column_dict in vnext_column_list:
        datasource_id = vnext_column_dict.get("dataSourceId")
        column_name_list = vnext_column_dict.get("columnNameList")
        if not column_name_list:
            for v2_column_dict in v2_column_list:
                v2_datasource_id = v2_column_dict.get("dataSourceId")
                if datasource_id == v2_datasource_id:
                    v2_column_name_list = v2_column_dict.get("columnNameList")
                    vnext_column_dict["columnNameList"] = v2_column_name_list
    return jsonify({"success": True, "data": vnext_column_list})


@api.route('/api/v3/ds/etl/dataset/datasource/<string:datasource_id>', methods=['GET'])
@verify_token
def etl_get_datasource_dispatch(datasource_id):
    """get etl datasource dispatch"""
    result_data = widget_config_adapt(datasource_id)
    if result_data:
        result = {"success": True, "data": result_data}
        return jsonify(result)
    return proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')


@api.route('/api/v1/etl/datasource/<string:datasource_id>/data', methods=['GET'])
def etl_get_data(datasource_id):
    """get etl data"""
    widget_datasource = widget_config_adapt(datasource_id)
    if widget_datasource:
        g.space_id = widget_datasource.get("spaceId")
        ds_connection_id = widget_datasource.get("dsConnectionId")
        language = widget_datasource.get("language")
        timezone = widget_datasource.get("timezone")
        v2_ds_connection_config = get_v2_connection_config_by_id(ds_connection_id)
        widget_datasource['data_size'] = ETL_FETCH_DATA_LIMITS
        widget_datasource['isEtl'] = True
        widget_data = make_widget_data(widget=widget_datasource,
                                       v2_ds_connection_config=v2_ds_connection_config,
                                       timezone=timezone,
                                       locale=language,
                                       is_covert_date_tz=False)
        result = _parse_to_etl_datasource_table_data(widget_data, widget_datasource)
        return jsonify({"success": True, "data": result})
    return "", 204


def _get_v2_column_name_list():
    response = proxy(request, f'{app.config["MIDDLE_URL"]}{request.path}')
    if response.status_code == HTTPStatus.OK and response.get_json():
        return response.get_json().get("data")
    return None


def _parse_to_etl_datasource_table_data(widget_data, widget_datasource):
    """Parse the resulting data into the structure required by the dataset"""
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-nested-blocks
    etl_datasource_table = {}
    column_list = _get_etl_datasource_column_list(widget_datasource)
    etl_datasource_table["columnList"] = column_list
    rows_list = widget_data.get("data")
    if all([widget_datasource, rows_list]):
        data_list = []
        for row in rows_list:
            row_dict = {}
            for index, cell in enumerate(row):
                column = column_list[index]
                column_id = column.get("columnId")
                row_dict[column_id] = cell
            data_list.append(row_dict)
        etl_datasource_table["dataList"] = data_list
    return etl_datasource_table


def _get_column_name_list_by_datasource_id(datasource_id_list):
    datasource_column_list = []
    for datasource_id in datasource_id_list:
        column_list = _get_etl_datasource_column_list_by_id(datasource_id)
        name_list = []
        if column_list:
            for column in column_list:
                name_list.append(column.get("name"))
        datasource_column_list.append({
            "dataSourceId": datasource_id,
            "columnNameList": name_list
        })
    return datasource_column_list


def _get_etl_datasource_column_list_by_id(datasource_id):
    widget_datasource = widget_config_adapt(datasource_id)
    if widget_datasource:
        return _get_etl_datasource_column_list(widget_datasource)
    return None


def _get_etl_datasource_column_list(widget_datasource):
    column_list = []
    field_list = widget_datasource.get("fields")
    timezone = widget_datasource.get("timezone")
    is_support_time_group = True  # TODO get value by data source config

    group_field_list = []
    calculated_field_list = []
    for field in field_list:
        field_type = field.get("type")
        if field_type in CALCULATED_FIELD_TYPE:
            calculated_field_list.append(field)
        else:
            group_field_list.append(field)
    column_index = 0
    for field in group_field_list:
        column = _buid_etl_datasource_column(field, timezone, False, is_support_time_group)
        column_index += 1
        column["ordinalPosition"] = column_index
        column_list.append(column)
    for field in calculated_field_list:
        column = _buid_etl_datasource_column(field, timezone, True, is_support_time_group)
        column_index += 1
        column["ordinalPosition"] = column_index
        column_list.append(column)
    _fix_column_name_duplicate(column_list)
    return column_list


def _fix_column_name_duplicate(column_list):
    """Fix duplicate column names """
    column_name_list = []
    column_name_index_dict = {}
    for column in column_list:
        name = column.get("name")
        if name in column_name_list:
            index = column_name_index_dict.get(name, 0) + 1
            column_name_index_dict[name] = index
            name = f"{name}({index})"
        else:
            column_name_index_dict[name] = 1
        column["name"] = name
        column["columnId"] = name
        column_name_list.append(name)


def _buid_etl_datasource_column(field, timezone,
                                is_calculated_field, is_supper_time_group):
    """column information required to construct the dataset"""
    etl_datasource_column = {}
    column_name = _get_field_show_name(field)
    column_uuid = field.get("uuid")
    data_type = field.get("dataType")
    data_format = field.get("dataFormat")
    calculate_type = field.get("calculateType")
    data_type_upper = data_type.upper()
    if calculate_type and calculate_type.upper() in AGGREGATE_FUNC:
        data_type = DataType.NUMBER
        data_format = None
    if data_type_upper not in NUMBER_TYPE_LIST and is_calculated_field:
        data_type = DataType.NUMBER
        data_format = None
    if data_type_upper in [DataType.DATE, DataType.DATETIME]:
        etl_datasource_column["dataType"] = DataType.TIMESTAMP
    else:
        etl_datasource_column["dataType"] = data_type

    if data_type_upper in [DataType.TIMESTAMP,
                           DataType.DATETIME,
                           DataType.DATE
                           ] and is_supper_time_group:
        date_period = field.get("granularity").get("value") if field.get("granularity") else None
        if not date_period:
            date_period = DatePeriod.DAY
        data_format = DatePeriod.get_format_by_period(date_period)
    etl_datasource_column["columnType"] = data_type
    etl_datasource_column["timezone"] = timezone

    if data_type_upper in [DataType.DATE, DataType.TIMESTAMP, DataType.TIMESTAMP]:
        etl_datasource_column["dataFormat"] = DEFAULT_DATE_FORMAT
    elif data_type_upper == DataType.PERCENT:
        etl_datasource_column["dataFormat"] = "%"
    else:
        etl_datasource_column["dataFormat"] = data_format

    # Modify the data type to the type required by the dataset
    column_data_type = etl_datasource_column.get("dataType").upper()
    if DataType.TIMESTAMP == column_data_type:
        etl_datasource_column["dataType"] = DataType.TIMESTAMP
        etl_datasource_column["dataFormat"] = DEFAULT_DATE_FORMAT
    elif column_data_type in NUMBER_TYPE_LIST:
        etl_datasource_column["dataType"] = DataType.DOUBLE
    else:
        etl_datasource_column["dataType"] = DataType.TEXT
    etl_datasource_column["columnId"] = column_name
    etl_datasource_column["name"] = column_name
    etl_datasource_column["uuid"] = column_uuid
    return etl_datasource_column


def _get_field_show_name(field):
    """Gets the name that the metric dimension displays """
    alias = field.get("alias")
    if alias:
        return alias
    show_name = field["name"]
    calculate_type = field.get("calculateType").upper() if field.get("calculateType") else None
    if calculate_type == Func.FUNC_COUNTA:
        return "#" + show_name
    return show_name
