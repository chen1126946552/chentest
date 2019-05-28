"""All classes/methods/tools to help to adapt to v2 on `widget data`"""

import copy
import logging
import time
import numbers
from uuid import uuid1

import pandas as pd
import numpy as np

from common.service.constants import DatasourceTypes, GraphType
from common.uncategorized.datetime_util import DateTime
from common.uncategorized.dict_query import DictQuery
from services.downstream import (get_connection_data,
                                 get_custom_connection_segments,
                                 get_table_data, )
from services.exception import ServiceError, ErrorCode
from services.translate import get_translator
from utils.ds_connection_config_parser import \
    parse as parse_ds_connection_config
from utils.system_constant import DataType, DataFormat, get_ds_info_by_ds_id
from .common import get_current_v2_space_info
from .constant import Fields, SpecialCases

logger = logging.getLogger(__name__)

# pylint: disable=invalid-name,too-many-instance-attributes,missing-docstring,too-many-lines

DATE_GRANULARITY_FORMAT_MAP = {
    'iso8601': '%Y-%m-%dT%H:%M:%S:000Z',
    'second': '%Y-%m-%d %H:%M:%S',
    'minute': '%Y-%m-%d %H:%M',
    'hour': '%Y-%m-%d %H',
    'day': '%Y-%m-%d',
    'month': '%Y-%m',
    'year': '%Y'
}

DEFAULT_DATA_FETCHING_PAGE_SIZE = 10000
ZERO_TIME_ZONE = 'UTC'
OTHERS_CATEGORY_NAME = 'Others'


# pylint: disable=too-many-arguments
def make_widget_data(widget, v2_ds_connection_config, timezone, locale, week_start_day=None,
                     is_covert_date_tz=True):
    """
    Construct the data format required by the widget
    Args:
        widget(dict): widget vo
        v2_ds_connection_config(dict): ds connection config
        timezone(string): User's account time zone
        locale (string): e.g. en_US
        week_start_day (string): e.g monday
        is_covert_date_tz (bool): Whether the date needs to be converted

    Returns:
        widget data result
    """
    is_etl = widget.get("isEtl", False)
    if is_etl:
        etl_widget_req_parameters_process(widget)
    parsed = parse_ds_connection_config(v2_ds_connection_config)
    ds_info = get_ds_info_by_ds_id(parsed.ds_id)
    assert ds_info

    req_params = widget_data_req_param_parse(widget, ds_info, parsed, timezone, locale,
                                             week_start_day)

    if ds_info['type'] == DatasourceTypes.DB:
        # request is for data of a database table
        data = get_table_data(parsed.connection_id, parsed.table_id, req_params)
    else:
        # request is for data of a connection
        data = get_connection_data(parsed.connection_id, req_params)
    if not is_covert_date_tz:
        return data
    # convert date columns from timestamp to formatted string
    convert_date(data, timezone=ZERO_TIME_ZONE if is_etl else timezone)
    if not is_etl:
        data_format(data)
    return widget_data_result_adapt(data, widget, locale)


def etl_widget_req_parameters_process(widget_vo):
    """If the request is ETL, format the date type to ISO8601"""
    field_list = widget_vo.get("fields")
    if field_list:
        for field in field_list:
            if field.get("dataType").upper() in [DataType.TIMESTAMP,
                                                 DataType.DATE,
                                                 DataType.DATETIME]:
                field["dataFormat"] = "iso8601"


def _fix_widget_parameters(widget):
    field = widget.get('field')
    if not field.get('uuid'):
        field['uuid'] = str(uuid1())


def make_widget_data_filter_selections(widget, v2_ds_connection_config, timezone):
    """
    Construct the data format required by selections in filter
    Args:
        widget(dict): variant widget vo (only contains field and time info)
        v2_ds_connection_config(dict): ds connection config
        timezone(string): User's account time zone

    Returns:

    """
    _fix_widget_parameters(widget)
    parsed = parse_ds_connection_config(v2_ds_connection_config)

    filter_field = copy.deepcopy(widget['field'])
    # set filter field to `category` to get dimension selections from datasource
    filter_field['type'] = "category"
    raw_widget = {
        'time': widget.get('time', {}),
        'fields': [filter_field]
    }

    ds_info = get_ds_info_by_ds_id(parsed.ds_id)
    assert ds_info

    req_param = widget_data_req_param_parse(raw_widget, ds_info, parsed, timezone)
    data = get_connection_data(parsed.connection_id, req_param)
    convert_date(data, timezone=timezone)
    return [
        {
            'id': item[0],
            'name': item[0],
            'extra': None
        } for item in data['data']
    ]


def data_format(data):
    """Format the data according to the field type"""
    percentage_field_ids = []
    column_ids = []
    for field in data['header']:
        field_id = field.get("uuid")
        data_format_str = field.get("dataFormat")
        column_ids.append(field_id)
        if data_format_str == DataFormat.PERCENTAGE:
            percentage_field_ids.append(field_id)

    # Determines whether formatting is required and, if so, initializes DataFrame
    is_reset_data = False
    if any([percentage_field_ids]):
        data_frame = pd.DataFrame(data["data"], columns=column_ids)
        is_reset_data = True
    for f_id in percentage_field_ids:
        data_frame[f_id] = data_frame[f_id] * 100
    if is_reset_data:
        for column_name, _type in data_frame.dtypes.to_dict().items():
            if _type.name == 'float64':
                data_frame[column_name] = data_frame[column_name].apply(lambda x: round(x, 2))
        data["data"] = data_frame.where(data_frame.notnull(), None).values.tolist()


def widget_data_websocket_adapt(data, socket_id):
    """
    Build webSocket type data
    Args:
        data: dm data
        socket_id: webSocket connection id

    Returns:
    """
    return {
        "type": "WidgetData",
        "data": {
            "content": data,
            "status": "success"
        },
        "socketId": socket_id
    }


# pylint: disable=too-many-arguments
def widget_data_req_param_parse(req_param, ds_info, ds_connection_config,
                                timezone=None, locale='en_US', week_start_on=None):
    """
    data req parse
    Args:
        req_param(dict): request body
        ds_info(dict): datasource info
        ds_connection_config(dict): vx-ds-config
        timezone(string):
        locale (string): default is en_US
        week_start_on (string): the start day of week in user's space setting
    Returns(dict): data req adapt to vx:

    """
    return DataParser(req_param, ds_info, ds_connection_config, timezone, locale,
                      week_start_on).collect()


def widget_data_result_adapt(data, req_param, locale='en_US'):
    """
    data result adapt
    Args:
        data(dict): data result
        req_param(dict): data req body
        locale (string): default is en_US
    Returns(dict): data result adapt to v2

    """
    return DataAdaptor(data, req_param, locale).collect()


def convert_date(data, timezone):
    """Converts date type data from timestamp to date string
    Args:
        data ({obj}): data result from business level
        timezone (string): timezone e.g Asia/Shanghai
    """

    def _get_data_format_by_granularity(granularity):
        return DATE_GRANULARITY_FORMAT_MAP.get(granularity, '%Y-%m-%d %H:%M:%S')

    date_fields = {idx: _get_data_format_by_granularity(field.get('dataFormat')) for
                   idx, field in enumerate(data['header']) if field.get('type') == 'date'}
    if date_fields:
        for row in data['data']:
            for idx, date_format in date_fields.items():
                if row[idx] is not None:
                    row[idx] = DateTime(tz=timezone, ts=int(row[idx])).format(date_format)


class DataParser:
    """
    Parsing data request
    """

    #
    def __init__(self,  # pylint: disable=too-many-arguments
                 data,
                 ds_info,
                 ds_connection_config,
                 timezone=None,
                 locale=None,
                 week_start_on=None):
        self.data = data
        self.timezone = timezone
        self.locale = locale
        self.week_start_on = week_start_on or get_current_v2_space_info()['weekStart']
        self.ds_info = ds_info

        if ds_info['type'] == DatasourceTypes.DB:
            # database table query path consists of db name and table name
            self.path = [ds_connection_config.database_name, ds_connection_config.table_name]
        else:
            self.path = ds_connection_config.profile_path

        self.connection_id = ds_connection_config.connection_id

        # used to fill in req data result
        self.parsing_funcs = (
            self.paging,
            self.fields,
            self.filters,
            self.segment,
            self.sort,
            self.date_range,
            self.compare_with_previous_period,
            self.using_cache_check
        )

    def collect(self):
        """data req params for vx"""
        raw_result = {
            'weekStartOn': self.week_start_on,
            'timezone': self.timezone,
            'path': self.path,
            'locale': self.locale,
            'graphType': self.data.get('graphType'),
            'map': self.data.get('map'),
            'dsInfo': self.ds_info
        }
        for func in self.parsing_funcs:
            raw_result.update(func())
        return raw_result

    def using_cache_check(self):
        return {'noCache': bool(self.data.get('noCache', False))}

    def paging(self):
        """paging parse"""
        size = self.data.get('data_size', DEFAULT_DATA_FETCHING_PAGE_SIZE)
        return {'paging': {'size': size}}

    def fields(self):
        """fields parse"""
        v2_fields = self.data.get('fields') or []
        return {
            'fields': self._fields_parse(v2_fields)
        }

    def _field_parse(self, v2_field):
        """calculated field not handled yet"""

        graph_type = self.data.get('graphType', '').lower()

        vx = dict()
        vx['id'] = v2_field['id']
        vx['type'] = Fields.NameMapping.type_map.get(v2_field['dataType'])
        vx['dataFormat'] = v2_field.get('dataFormat', None)
        vx['groupBy'] = v2_field.get('type') not in ['yAxis', 'leftYAxis', 'rightYAxis']

        v2_granularity = v2_field.get('granularity')
        g_val = v2_granularity
        if isinstance(v2_granularity, dict):
            g_val = v2_granularity.get('value')

        vx['granularity'] = Fields.NameMapping.granularity_map.get(g_val)
        # aggregate computing
        vx['agg'] = Fields.NameMapping.agg_map.get(v2_field.get('calculateType'))
        # analysis computing
        anal_type = Fields.NameMapping.field_analysis_function_map.get(
            v2_field.get('analysisFunctionType'))
        vx['anal'] = anal_type
        if graph_type in [GraphType.NUMBER.value, GraphType.PROGRESSBAR.value, GraphType.MAP.value,
                          GraphType.FUNNELBYMETRICS, GraphType.FUNNELBYCATEGORY.value,
                          GraphType.BUBBLE.value]:
            vx['anal'] = None
        else:
            if anal_type in ('proportion', 'growth_rate'):
                vx['dataFormat'] = 'percentage'
        # if a calculated field
        vx['isCal'] = bool(v2_field.get('isCalculate'))
        vx['uuid'] = v2_field['uuid']
        return {k: v for k, v in vx.items() if v}

    def _fields_parse(self, fields):
        """field parse helper method"""
        return [self._field_parse(v2) for v2 in fields]

    def filters(self):
        """filters parse"""
        v2_filters = self.data.get('filters') or []

        def _filter(_field, _values, _operator):
            # frontend date piker's format is '%Y/%m/%d' smallest granularity is 'day' for now
            result = {
                'field': _field,
                'operator': _operator,
                'values': _values
            }
            if _field.get('type') == 'date':
                granularity = _field.get('dataFormat')
                if granularity in ['hour', 'minute', 'second']:
                    # Other granularity is treated by day format
                    _field['dataFormat'] = DATE_GRANULARITY_FORMAT_MAP.get('day')
                else:
                    _field['dataFormat'] = DATE_GRANULARITY_FORMAT_MAP.get(granularity)
                if granularity == 'year':
                    values_formatted = [v.split('/')[0] for v in _values]
                elif granularity == 'month':
                    values_formatted = ['-'.join(v.split('/')[:2]) for v in _values]
                elif granularity == 'day':
                    values_formatted = ['-'.join(v.split('/')[:3]) for v in _values]
                else:
                    # Other granularity is treated by day
                    values_formatted = ['-'.join(v.split('/')[:3]) for v in _values]
                result.update({'values': values_formatted})
            return result

        f_list = []
        for v2 in v2_filters:
            values = v2['setting']['items'][0].get('value')
            field = self._fields_parse([v2])[0]
            operator = v2['setting']['items'][0]['code']

            if operator == 'between' and len(values) > 1:
                val_list_1 = values[:1]
                val_list_2 = values[1:2]
                if values[0] > values[1]:
                    val_list_1 = values[1:2]
                    val_list_2 = values[:1]
                field_copy = copy.deepcopy(field)
                ge_filer = _filter(field, val_list_1, 'ge')
                le_filter = _filter(field_copy, val_list_2, 'le')
                f_list.extend([ge_filer, le_filter])
            else:
                f_list.append(_filter(field, values, operator))

        return {'filters': [i for i in f_list if i]}

    def segment(self):
        """segment parse"""
        v2_segment = self.data.get('segment')
        vx_segment = {}
        if v2_segment:
            if v2_segment.get('id') is None:
                logger.error("Segment id is missing: %s", v2_segment)
            elif v2_segment.get('type'):
                # ga builtin segment
                vx_segment = {'segmentId': v2_segment['id']}
            else:
                # custom segments in datadeck
                custom_segment = self._get_custom_segment(v2_segment['id'])
                if not custom_segment:
                    raise ServiceError(error_code=ErrorCode.SEGMENT_NOT_EXIST, locale=self.locale)
                conditions = custom_segment['conditions']
                filters = [self._parse_custom_segment_condition(c) for c in conditions]
                vx_segment = {
                    'scope': SpecialCases.ga_scope_mapping.get(custom_segment['scope'].lower()),
                    'filters': filters,
                    'exclude': custom_segment['operation'] == 'exclude'
                }
        return {'segment': vx_segment}

    def _get_custom_segment(self, seg_id):
        """ """
        custom_segments = get_custom_connection_segments(self.connection_id)
        for cs in custom_segments:
            if cs['id'] == seg_id:
                return cs
        return None

    def _parse_custom_segment_condition(self, condition):
        return {
            'orClauses': [{
                'fieldId': cd_seg['field']['id'],
                'operator': cd_seg['operator'],
                'values': [cd_seg['value']] if not isinstance(
                    cd_seg['value'], list) else cd_seg['value'],
            } for cd_seg in condition]
        }

    def sort(self):
        """sort parse"""
        v2_sort = self.data.get('sort') or {}
        field_uuid = v2_sort.get('uuid')
        order = v2_sort.get('order')
        v2_field = None
        for field in self.data.get('fields', []):
            if field['uuid'] == field_uuid:
                v2_field = field
                break
        vx_sort = {'field': self._field_parse(v2_field), 'order': order} if v2_field else {}
        return {'sort': vx_sort}

    # pylint: disable=too-many-branches,too-many-statements
    def date_range(self):
        """dataRange parse"""
        return {'dateRange': self.data.get('time') or {}}

    def compare_with_previous_period(self):
        """compare_with_previous_period parse"""

        # TODO special case for cwp unsupported graph types, no need macro
        graph_types_with_no_cwp = [gt.lower() for gt in [
            GraphType.BAR.value, GraphType.STACKBAR.value, GraphType.DOUBLEAXIS.value,
            GraphType.PIE.value, GraphType.PROGRESSBAR.value, GraphType.FUNNELBYCATEGORY.value,
            GraphType.FUNNELBYMETRICS.value, GraphType.BUBBLE.value
        ]]

        graph_type = self.data.get('graphType', '').lower()
        if graph_type in graph_types_with_no_cwp:
            return {}

        vx_cwp = {}
        cwp = self.data.get('compareWithPreviousPeriod')
        if cwp and cwp.get('compareWithPreviousPeriodStatus'):
            if graph_type == GraphType.NUMBER.value:
                cwp['compareFields'] = [self.data['fields'][0]]
            vx_cwp['code'] = \
                Fields.NameMapping.compare_with_previous_period_code_map.get(
                    cwp['comparePeriod']
                )
            compute_method = Fields.NameMapping.compare_with_previous_period_compute_map.get(
                cwp['compareDisplay']
            )
            vx_cwp['computing'] = compute_method
            cwp_fields = self._fields_parse(cwp['compareFields'])
            if compute_method == 'growth_rate':
                for f in cwp_fields:
                    f['dataFormat'] = 'percentage'
            # filter the dimension/colorby fields mixed in cwp fields
            vx_cwp['fields'] = [true_cwp_field for true_cwp_field in cwp_fields if
                                not true_cwp_field.get('groupBy')]

        return {'compareWithPrevious': vx_cwp}


class DataAdaptor:
    """
    Adapting data result
    """

    def __init__(self, data, req_param, locale):
        self.i18n = get_translator(locale, domain='data')
        self.vx_header = data.get('header') or []
        self.vx_data = data.get('data') or []
        self.vx_summary = data.get('summaryValues') or []
        self.extra_info = data.get('extra_info') or {}
        self.original_req_param = req_param
        self.fields = self._get_fields()

    def _get_fields(self):
        """set fields, might inject cwp fields"""

        def _match_field(field_uuid, fields):
            cwp = False
            if field_uuid.endswith(':cwp'):
                cwp = True
                # remove compare with previous field uuid's suffix
                field_uuid = field_uuid[:-4]
            for f in fields:
                if f['uuid'] == field_uuid:
                    field = copy.deepcopy(f)
                    if cwp:
                        fmt = self.original_req_param['compareWithPreviousPeriod']['compareDisplay']
                        self._cwp_field_decorate(field, fmt)
                    return field
            raise ValueError("can not match header field with request fields")

        request_fields = self.original_req_param['fields'] or []
        graph_type_str = self.original_req_param.get('graphType')
        if graph_type_str and GraphType(graph_type_str).is_map():
            map_header_field = self.vx_header[0]
            map_field = copy.deepcopy(request_fields[0])
            map_field['id'] = map_header_field['id']
            map_field['type'] = 'category'
            map_field['uuid'] = map_header_field['uuid']
            request_fields.append(map_field)

        # result headers illustrates the data result sequence in the second-dimension list
        return [_match_field(h_field['uuid'], request_fields) for h_field in self.vx_header]

    def _cwp_field_decorate(self, field, display_format):
        """before inject cwp fields in, must change their names/ids/uuids"""
        # special flag to recognize a cwp field from all fields
        if display_format in ['growRate', 'growValue']:
            field['graphType'] = GraphType.LINE.value
        field['compare_with'] = True
        field['id'] += '(2)'
        field['uuid'] += '(2)'
        field['extra']['code'] += '(2)'
        if display_format == 'growRate':
            field['dataType'] = 'PERCENT'
            field['dataFormat'] = 'percentage'

    def _is_contain_cwp(self):
        for field in self.fields:
            if field.get('compare_with'):
                return True
        return False

    def _cwp_indexes(self):
        return [i for i, x in enumerate(self.fields) if x.get('compare_with')]

    def _legend_index(self):
        return next((i for i, x in enumerate(self.fields) if x['type'] == 'legend'), None)

    def _dimension_index(self):
        return next((i for i, x in enumerate(self.fields) if x['type'] == 'xAxis'), None)

    def _series_limit(self):
        return DictQuery(self.original_req_param).get('settings/maxLimit/series', 10)

    def _dimension_limit(self):
        return int(DictQuery(self.original_req_param).get('settings/maxLimit/bars', 1000))

    def _is_show_other(self):
        return DictQuery(self.original_req_param).get('settings/showOther/visible')

    # pylint: disable=too-many-locals
    def _get_highchart_series(self, data, metric_index, compare_base_index=None):
        legend_index = self._legend_index()
        if legend_index is not None:
            df = pd.DataFrame(data)
            data_by_legend = df.groupby(legend_index)
            # Used to find the top N series, if it's the compared field,
            # use the orginal metric to find the top N series
            serie_index = compare_base_index if compare_base_index is not None else metric_index
            sum_by_legend = data_by_legend[serie_index].sum()
            result = self._get_colorby_data(sum_by_legend, data_by_legend, metric_index)
        else:
            if self._dimensions():
                current_series = self._get_series_data(data, 0, metric_index)
            else:
                current_series = [[self.fields[metric_index]['name'], data[0][metric_index]]]

            result = self._get_widget_inner_data(current_series, metric_index)

        if compare_base_index is not None:
            # if compare with previous metric, need fillin one dimension column at last
            dimensions = self._dimensions()

            if not dimensions:
                dimension_field = {}
            elif legend_index is not None:
                dimension_fields_filter_legend = \
                    [dim for dim in dimensions if dim['uuid'] != self.fields[legend_index]['uuid']]
                dimension_field = dimension_fields_filter_legend[0] if \
                    dimension_fields_filter_legend else {}
            else:
                dimension_field = dimensions[0]

            for serie in result:
                try:
                    self.fillin_cwp_dimension_column(serie['rows'],
                                                     dimension_field.get('dataType') == 'DATETIME',
                                                     granularity=dimension_field.get('dataFormat'))
                except Exception as e:  # pylint: disable=broad-except
                    logger.warning("Highchart tooltip adapting failed: %s", str(e))

        return result

    def fillin_cwp_dimension_column(self, rows, dimension_is_date, granularity=None):
        cwp_code = self.original_req_param['compareWithPreviousPeriod']['comparePeriod']
        datestr_fmt = DATE_GRANULARITY_FORMAT_MAP.get(granularity) if granularity else None
        cwp_date_range_info = self.extra_info.get('cwp_date_range')
        period_offset = cwp_date_range_info['start'] - cwp_date_range_info['end']
        for row in rows:
            if dimension_is_date:
                dim_dt = DateTime(ds=row[0], fmt=datestr_fmt)
                if cwp_code == 'compareWithPreviousPeriod':
                    new_col = dim_dt.offset(second=period_offset / 1000).format(datestr_fmt)
                elif cwp_code == 'compareWithLastYear':
                    new_col = dim_dt.offset(year=-1).format(datestr_fmt)
                elif cwp_code == 'compareWithLastMonth':
                    new_col = dim_dt.offset(month=-1).format(datestr_fmt)
                else:
                    raise ServiceError('Invalid compare period code: %s' % cwp_code)
                row.append(new_col)
            else:
                row.append(row[0])

    def _get_widget_inner_data(self, data, metric_index=0):
        metric_key = self.fields[metric_index]['uuid'] \
            if self.is_highchart() else self.metrics_key()
        variable_name = self._headers()[metric_index] \
            if self.is_highchart() else self.metric_name()
        metric_code = self.fields[metric_index]['id'] \
            if self.is_highchart() else self.metrics_code()
        graph_type = self.fields[metric_index].get('graphType') \
            if self.is_highchart() else None
        result = [
            {
                'color': None,
                'dataFormatMap': {},  # todo
                # 'dataKey': self.date_key(),
                'dataTypeMap': self.data_type_map(),
                # 'dateRange': self.date_range(),
                'dimensions': self.dimension_code(),
                'dimensionsId': None,
                'dimensionsKey': self.dimension_key(),
                'extInfo': {},
                'graphType': graph_type or self.graph_type().value,
                'max': None,
                'metricsCode': metric_code,
                'metricsKey': metric_key,
                'metricsName': variable_name,
                'metricsNames': self.metric_names(),
                'metricsSign': None,
                'metricsTotalsMap': self.metric_total_map(),
                'orderColumn': self.get_order_column(),
                'orderRule': self.get_order_rule(),
                'orderType': None,  # todo
                'rows': data,
                'stack': None,
                'tableColumnIdList': self.table_column_id_list(),
                'unitMap': self.unit_map(),
                'useDatetimeAxis': False,  # todo
                'variableName': variable_name,
                'totals':{}
            }
        ]
        return result

    def _covert_nan_value(self, value, default_value):
        # None value
        if not value:
            return default_value
        # numpy nan
        if isinstance(value, numbers.Number) and np.isnan(value):
            return default_value
        return value

    def _get_series_data(self, data, dimension_index, metric_index):
        if dimension_index is not None:
            dimension_limit = self._dimension_limit()
            result = [[row[dimension_index], self._covert_nan_value(row[metric_index], None)]
                      for row in data][:dimension_limit]
            if self._is_show_other():
                other_value = sum([self._covert_nan_value(row[metric_index], 0)
                                   for row in data[dimension_limit:]])
                result.append([OTHERS_CATEGORY_NAME, other_value])
            return result
        # For case no dimensions
        return [[self.fields[metric_index]['name'],
                 self._covert_nan_value(row[metric_index], None)] for row in data]

    def _get_colorby_data(self, sum_by_legend, data_by_legend, metric_index):
        result = []
        top_keys = sum_by_legend.nlargest(self._series_limit()).keys()

        dimension_index = self._dimension_index()
        for key in top_keys:
            # Convert pandas type to normal python type to avoid JSON seralization
            serie_data = self._get_series_data(data_by_legend.get_group(key).values.astype(object),
                                               dimension_index, metric_index)
            serie_widget = self._get_widget_inner_data(serie_data, metric_index)

            serie_widget[0]['variableName'] = key if len(self._metrics()) == 1 \
                else '{}-{}'.format(self._headers()[metric_index], key)

            serie_widget[0]['metricsSign'] = \
                self.fields[metric_index]['id'].replace('(2)', '') + '-' + str(key)
            serie_widget[0]['dimensionsId'] = key
            serie_widget[0]['dimensions'] = self.fields[self._legend_index()]['id']
            result += serie_widget

        return result

    def _get_category(self):
        if self._dimension_index() is not None:
            # Need to preserve the original order.
            used = set()
            dimension_limit = self._dimension_limit()
            dimension_values = [row[0] for row in self.vx_data
                                if row[0] not in used and not used.add(row[0])]
            result = dimension_values[:dimension_limit]
            if self._is_show_other():
                result.append(OTHERS_CATEGORY_NAME)
            return result
        # category is the original fields without compare-with-previous-data fields
        return [field['name'] for field in self.original_req_param['fields']]

    def _get_target_value(self):
        return self.original_req_param['targetValue']

    def _get_compare_base_field_index(self, field):
        for idx, f in enumerate(self.fields):
            if f['fieldId'] == field['fieldId'] and field['uuid'].startswith(f['uuid']):
                return idx

        return None

    def collect(self):  # pylint: disable=too-many-locals
        """data result for vx"""
        if not self.vx_data:
            return self.make_data_null_body()
        inner_data = []

        graph_type = self.graph_type()
        if graph_type.is_highchart():
            for idx, f in enumerate(self.fields):
                if self._is_metric(f):
                    compare_base_idx = self._get_compare_base_field_index(f) if f.get(
                        'compare_with') else None
                    result = self._get_highchart_series(self.vx_data, idx, compare_base_idx)
                    if compare_base_idx is None:
                        inner_data.extend(result)
                    else:
                        j = len(result)
                        for i, row in enumerate(result[:-1]):
                            inner_data.insert(i - j + 1, row)
                        inner_data.append(result[-1])

        elif graph_type == GraphType.NUMBER:
            inner_data = self._get_widget_inner_data(self.data_rows(), 0)
            if self._is_contain_cwp():
                title = [None]
                metric_keys = inner_data[0]['metricsKey']
                if "," in metric_keys:
                    metric_key = metric_keys.split(',')[0]
                else:
                    metric_key = metric_keys

                for field in self.fields:
                    if field['uuid'] == metric_key:
                        title = [field['name']]
                        break

                nums = inner_data[0]['rows'][1]
                cwp_type = self.original_req_param['compareWithPreviousPeriod']['compareDisplay']
                if cwp_type == 'growValue':
                    nums[1] = nums[0] - nums[1]
                elif cwp_type == 'growRate':
                    try:
                        nums[1] = float(nums[0]) / (1 + nums[1] / 100)
                    except Exception:  # pylint: disable=broad-except
                        nums[1] = None
                nums = ["%.04f" % float(_) for _ in nums if _ is not None]
                inner_data[0]['rows'] = [title + nums]

        elif graph_type == GraphType.PROGRESSBAR:
            data = [['', self.vx_data[0][0], self._get_target_value()]]
            inner_data = self._get_widget_inner_data(data, 0)
        else:
            inner_data = self._get_widget_inner_data(self.data_rows(), 0)

        outer_data = {
            'availableDatePeriod': [],
            'categories': self._get_category(),
            'data': inner_data,
            'dataSetlastSyncTime': int(time.time() * 1000),
            'datePeriod': None,
            'ds_code': 'todo',
            'endDate': None,
            'errorCode': None,
            'errorLogs': None,
            'errorMsg': None,
            'errorParam': None,
            'extInfo': {},
            'graphType': graph_type.value,
            'isCacheData': False,
            'isDemoData': False,
            'max': None,
            'maxValue': None,
            'metricsAmountsMap': self.metric_total_map(),  # same with metric total map
            'minValue': None,
            'orderColumn': None,
            'orderRule': None,
            'panelComponents': self.get_pannel_components(),
            'panelId': self.original_req_param.get("panelId"),
            'rows': None,
            'showOthers': None,
            'sortType': None,
            'startDate': None,
            'status': 'success',
            'widgetId': self.original_req_param['widgetId']
        }

        return outer_data

    def get_pannel_components(self):
        """Merge global panel and time filters"""
        result = []
        widget = self.original_req_param
        if widget.get('global_filter'):
            result.extend(widget.get('panelFilterComponents'))
        if widget.get('global_time'):
            result.append(widget.get('panelTimeComponent'))

        return result

    def get_order_column(self):
        sort = self.original_req_param.get("sort")
        if sort and 'uuid' in sort:
            return sort.get('uuid')
        return None

    def get_order_rule(self):
        sort = self.original_req_param.get("sort")
        if sort and 'order' in sort:
            return sort.get('order')
        return None

    def make_data_null_body(self):
        return {
            'availableDatePeriod': [],
            'categories': [],
            'data': [],
            'dataSetlastSyncTime': 0,
            'ds_code': 'todo',
            'panelId': self.original_req_param.get("panelId"),
            'status': 'success',
            'widgetId': self.original_req_param.get("widgetId"),
            'panelComponents': self.get_pannel_components(),
        }

    def data_rows(self):
        """get rows, add field headers first"""
        rows = [self._headers()]
        rows.extend(self.vx_data)
        return rows

    def data_format_map(self):
        return {f['uuid']: None for f in self.fields}

    def data_type_map(self):
        dmt = {}
        for field in self.fields:
            anal = field.get('analysisFunctionType')
            dtype = field.get('dataType')
            if anal:
                if anal == 'occupy':
                    dtype = 'PERCENT'
                elif anal == 'growthRate':
                    dtype = 'PERCENT'
            dmt[field['uuid']] = dtype
        return dmt

    def graph_type(self):
        """e.g. TABLE"""
        return GraphType(self.original_req_param['graphType'])

    def is_highchart(self):
        return self.graph_type().is_highchart()

    def _headers(self):
        """fill in data headers"""

        headers = []

        try:
            display_format = self.original_req_param['compareWithPreviousPeriod']['compareDisplay']
        except Exception:  # pylint: disable=broad-except
            display_format = None

        for field in self.fields:
            name = field['alias'] if field.get('alias') else field['name']
            if field.get('compare_with') and display_format:
                name_suffix = self.i18n(
                    Fields.NameMapping.compare_with_previous_period_display_format_map[
                        display_format]
                )
                name += name_suffix

            anal = field.get('analysisFunctionType')
            if anal == 'occupy':
                name += self.i18n('(Contribution)')
            elif anal == 'growthRate':
                name += self.i18n('(% Growth)')
            elif anal == 'cumulate':
                name += self.i18n('(Cumulative SUM)')
            headers.append(name)
        return headers

    def _field_show_name(self, field):
        """Handle alias"""
        return field['alias'] if field.get('alias') else field['name']

    def _is_metric(self, field):
        return field['type'] in ['yAxis', 'leftYAxis', 'rightYAxis']

    def _metrics(self):
        """metrics"""
        return list(filter(self._is_metric, self.fields))

    def _dimensions(self):
        """dimensions"""
        return list(filter(lambda f: not self._is_metric(f), self.fields))

    def metrics_code(self):
        """e.g. ga:users,ga:newUsers"""
        return ",".join([m['id'] for m in self._metrics()])

    def metrics_key(self):
        """e.g. d0949682-613f-4d1a-8540-dd34461560b3,92a60ec0-c976-4960-83bf-91f7a0b9b4d3"""
        return ",".join([m['uuid'] for m in self._metrics()])

    def metric_names(self):
        """e.g. ["Users", "New Users"]"""
        return [self._field_show_name(m) for m in self._metrics()]

    def metric_name(self):
        """e.g. Users,New Users"""
        return ",".join(self.metric_names())

    def dimension_code(self):
        """e.g. ga:medium"""
        return ",".join([m['id'] for m in self._dimensions()])

    def dimension_key(self):
        """e.g. d0949682-613f-4d1a-8540-dd34461560b3,92a60ec0-c976-4960-83bf-91f7a0b9b4d3"""
        return ",".join([m['uuid'] for m in self._dimensions()])

    def metric_total_map(self):
        """ totals map"""

        def data_formating(field_idx, val):
            if self.fields[field_idx].get('dataType') == 'PERCENT':
                if isinstance(val, (int, float)):
                    return round(val * 100, 4)
            return val

        filter_field_ids = [fil['id'] for fil in self.original_req_param.get('filters') or []]
        metrics = self._metrics()
        metric_ids = [m['id'] for m in metrics]
        invalid = bool(set(metric_ids) & set(filter_field_ids))
        return {
            m['uuid']: {
                'invalid': invalid,
                'code': m['id'],
                'dataFormat': None,
                'dataType': m['dataType'],
                'id': idx + 1,
                'key': m['uuid'],
                'name': m['name'],
                'showName': self._field_show_name(m),
                'unit': '',
                'value': data_formating(idx, self.vx_summary[idx])
            } for idx, m in enumerate(self.fields) if m['id'] in metric_ids
        } if self.vx_summary else {}

    def table_column_id_list(self):
        """e.g. ["d0949682-613f-4d1a-8540-dd34461560b3", "92a60ec0-c976-4960-83bf-91f7a0b9b4d3"]"""
        if self.graph_type() is GraphType.TABLE:
            return [f['uuid'] for f in self.fields]
        return []

    def unit_map(self):
        """e.g. {92a60ec0-c976-4960-83bf-91f7a0b9b4d3: "",
        d0949682-613f-4d1a-8540-dd34461560b3: ""}"""
        # todo all values are empty string?
        unit_string_map = {
            DataFormat.DURATION_IN_SECONDS: 's',
            DataFormat.PERCENTAGE: '%',
        }
        return {f['uuid']: unit_string_map.get(f.get('dataFormat'), '') for f in self.fields}
