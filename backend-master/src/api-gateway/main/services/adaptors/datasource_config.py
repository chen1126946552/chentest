"""
Adaptation code for converting vnext datasource config to v2 format.
"""


from pydatadeck.datasource.aggregation import AggregationFunctions
from pydatadeck.datasource.operators import FilterOperators, SegmentOperators

from services.translate import get_translator


def ds_config_adapt(ds_code, vx_ds_config, locale): # pylint: disable=too-many-locals
    """
    Adapting vnext datasource config to v2 format.

    Args:
        ds_code (str): datasource code
        vx_ds_config (dict): vnext datasource config

    Returns:
        dict: datasource config in v2 format
    """

    _ = get_translator(locale, 'config')

    result = {}
    result['config'] = config = {}

    # basic info
    config['basicInfo'] = basic_info = {}
    basic_info['isSupportI18n'] = True
    basic_info['isSupportCorrelateField'] = False
    basic_info['isSupportCalculatedField'] = True

    # datasource
    config['datasource'] = datasource = {}
    datasource['commands'] = commands = []
    datasource['view'] = view = {}
    view['steps'] = view_steps = []

    is_watch_change = vx_ds_config.get('hierarchy', {}).get('reloadFieldsOnHierarchyChange', False)

    vx_auth = vx_ds_config.get('auth')
    if vx_auth and vx_auth.get('type') in ['oauth', 'hybrid']:
        step = {
            'bindTo': 'account',
            'componentType': 'list',
            'connect': {
                'type': 'oAuth'
            },
            'description': _('Account'),
            'name': 'account',
            'output': ['id', 'name'],
            'placeholder': _('Please select your account'),
            'text': _('Account'),
            'type': 'account',
            'isWatchChange': is_watch_change
        }
        view_steps.append(step)

    vx_hier_items = vx_ds_config.get('hierarchy', {}).get('items', [])
    for item in vx_hier_items:
        command = {
            'id': item['id'],
            'response': {'type': 'tree'},
            'request': {'params': ['account.id', 'account.name']},
            'provider': ds_code,
        }
        commands.append(command)

        step = {
            'type': item['id'],
            'text': item['name'],
            'name': item['id'],
            'bindTo': item['id'],
            'command': item['id'],
            'componentType': 'tree',
            'placeholder': item['name'],
            'description': item['name'],
            'output': ['id', 'name'],
            'isWatchChange': is_watch_change
        }
        view_steps.append(step)

    # widgetEditor

    data_config = vx_ds_config.get('data', {})

    config['widgetEditor'] = widget_editor = {}
    widget_editor['fields'] = {'getFieldsMethod': 'vnext'}

    # aggregation
    agg_config = data_config.get('aggregation')
    if agg_config and agg_config.get('enabled'):
        widget_editor['calculateType'] = _adapt_agg_config(agg_config, _)

    # filter
    widget_editor['filter'] = _adapt_filter_config(data_config.get('filter'), ds_code, _)

    # segment
    if data_config.get('supportSegment'):
        widget_editor['segment'] = _adapt_segment_config(data_config.get('segment'), _)

    # timegroup
    if data_config.get('supportDateFieldGranularity'):
        widget_editor['timeGroup'] = _make_default_time_group(_)

    # graphs
    geolocation = data_config.get('geolocation')
    widget_editor['graphs'] = _make_default_graphs(geolocation, _)
    if geolocation:
        widget_editor['map'] = map = {}
        map['mapType'] = []

        if 'countryField' in geolocation:
            map['mapType'].append({
                'code': 'world',
                'name': _('World Map')
            })
            map['countryFields'] = [{
                'id': geolocation['countryField']['id'],
                'code': geolocation['countryField']['id'],
                'name': _(geolocation['countryField'].get('name', 'Country'))
            }]
        if 'regionField' in geolocation:
            map['mapType'].append({
                'code': 'country',
                'name': _('Country')
            })
            map['cityFields'] = [{
                'id': geolocation['regionField']['id'],
                'code': geolocation['regionField']['id'],
                'name': _(geolocation['regionField'].get('name', 'City'))
            }]

    # date range
    widget_editor['time'] = _make_time_config(data_config.get('dateRange'), _)

    return result


def _adapt_agg_config(agg_config, translate):
    _ = translate
    result = []
    operators = agg_config.get('operators')
    if not operators:
        operators = [
            AggregationFunctions.SUM,
            AggregationFunctions.AVERAGE,
            AggregationFunctions.MIN,
            AggregationFunctions.MAX,
            AggregationFunctions.STDEV,
            AggregationFunctions.VAR,
            AggregationFunctions.COUNTA,
            AggregationFunctions.DCOUNT
        ]

    for operator in operators:
        # vnext and v2 use different agg operator for "dcount" ...
        code = operator if operator != 'dcount' else 'countunique'
        item = {'code': code, 'name': _(operator.upper()), 'tip': operator.upper()}
        result.append(item)

    return result


SEGMENT_OPERATOR_NAME_MAPPING = {
    (SegmentOperators.EQUAL, 'string'): 'Exactly match',
    (SegmentOperators.NOT_EQUAL, 'string'): 'Does not exactly match',
    (SegmentOperators.STR_CONTAIN, 'string'): 'Contains',
    (SegmentOperators.STR_NOT_CONTAIN, 'string'): 'Does not contain',
    (SegmentOperators.REGEX_MATCH, 'string'): 'Matches RegEx',
    (SegmentOperators.REGEX_NOT_MATCH, 'string'): 'Does not match RegEx',
    (SegmentOperators.IS_NULL, ''): 'Is blank',
    (SegmentOperators.IS_NOT_NULL, ''): 'Is not blank',
    (SegmentOperators.EQUAL, 'number'): 'Equal to',
    (SegmentOperators.NOT_EQUAL, 'number'): 'Not equal to',
    (SegmentOperators.LT, 'number'): 'Less than',
    (SegmentOperators.LE, 'number'): 'Less than or equal to',
    (SegmentOperators.GT, 'number'): 'Greater than',
    (SegmentOperators.GE, 'number'): 'Greater than or equal to'
}


def _adapt_segment_config(segment_config, translate):

    _ = translate
    result = {
        'operators': {'string': {'items': []}, 'number': {'items': []}},
        'operations': {
            'items': [
                {'code': 'include', 'name': _('Include')},
                {'code': 'exclude', 'name': _('Exclude')}
            ],
            'default': {
                'name': _('Include'),
                'code': 'include'
            }
        },
        'scopes': {'items': []}
    }

    string_ops = segment_config and segment_config.get('stringOps')
    if not string_ops:
        string_ops = [SegmentOperators.EQUAL,
                      SegmentOperators.NOT_EQUAL,
                      SegmentOperators.STR_CONTAIN,
                      SegmentOperators.STR_NOT_CONTAIN,
                      SegmentOperators.REGEX_MATCH,
                      SegmentOperators.REGEX_NOT_MATCH]
    items = result['operators']['string']['items']
    for operator in string_ops:
        op_name = SEGMENT_OPERATOR_NAME_MAPPING.get((operator, 'string'))
        if not op_name:
            op_name = SEGMENT_OPERATOR_NAME_MAPPING.get((operator, ''))
        items.append({'code': operator, 'name': _(op_name)})
    if items:
        result['operators']['string']['default'] = items[2]

    number_ops = segment_config and segment_config.get('numberOps')
    if not number_ops:
        number_ops = [SegmentOperators.EQUAL,
                      SegmentOperators.NOT_EQUAL,
                      SegmentOperators.LT,
                      SegmentOperators.LE,
                      SegmentOperators.GT,
                      SegmentOperators.GE]
    items = result['operators']['number']['items']
    for operator in number_ops:
        op_name = SEGMENT_OPERATOR_NAME_MAPPING.get((operator, 'number'))
        if not op_name:
            op_name = SEGMENT_OPERATOR_NAME_MAPPING.get((operator, ''))
        items.append({'code': operator, 'name': _(op_name)})
    if items:
        result['operators']['number']['default'] = items[2]

    scopes = segment_config.get('scopes')
    if scopes:
        scope_items = [{'code': scope['id'], 'name': _(scope['name'])} \
                       for scope in scopes]
        result['scopes']['items'] = scope_items
        # use the first scope defined as default
        if scope_items:
            result['scopes']['default'] = scope_items[0]

    return result


def _adapt_filter_config(filter_config, ds_code, translate):

    if filter_config and filter_config.get('enabled') is False:
        return {}

    _ = translate
    result = {}

    # string operators

    result['string'] = {'options': []}
    string_ops = filter_config and filter_config.get('stringOps')
    if not string_ops:
        string_ops = [FilterOperators.IN_LIST,
                      FilterOperators.NOT_IN_LIST,
                      FilterOperators.STR_CONTAIN,
                      FilterOperators.STR_NOT_CONTAIN,
                      FilterOperators.IS_NULL,
                      FilterOperators.IS_NOT_NULL]

    need_filter_candidates = False
    if string_ops:
        if FilterOperators.IN_LIST in string_ops or FilterOperators.NOT_IN_LIST in string_ops:
            need_filter_candidates = True
            option = {'name': _('Select'), 'code': 'select', 'default_equal': 'equal'}
            option['items'] = items = []
            if FilterOperators.IN_LIST in string_ops:
                item = _make_filter_option_item(FilterOperators.IN_LIST,
                                                'multipleList', 'string', translate)
                item['command'] = 'dimensionValues'
                items.append(item)
            if FilterOperators.NOT_IN_LIST in string_ops:
                item = _make_filter_option_item(FilterOperators.NOT_IN_LIST,
                                                'multipleList', 'string', translate)
                item['command'] = 'dimensionValues'
                items.append(item)
            result['string']['options'].append(option)

    if any((op for op in string_ops \
            if op not in [FilterOperators.IN_LIST, FilterOperators.NOT_IN_LIST])):
        option = {
            'name': _('Advanced'),
            'code': 'advance',
            'default_equal': 'equal',
        }
        result['string']['options'].append(option)
        option['items'] = items = []
        for operator in string_ops:
            if operator in [FilterOperators.IN_LIST, FilterOperators.NOT_IN_LIST]:
                continue
            if operator in [FilterOperators.IS_NULL, FilterOperators.IS_NOT_NULL]:
                items.append(_make_filter_option_item(operator, '', '', translate))
            elif operator in [FilterOperators.REGEX_MATCH, FilterOperators.REGEX_NOT_MATCH]:
                items.append(_make_filter_option_item(operator, 'regex', 'string', translate))
            else:
                items.append(_make_filter_option_item(operator, 'tagInput', 'string', translate))

    if need_filter_candidates:
        result['commands'] = commands = []
        commands.append({
            'provider': ds_code,
            'id': 'dimensionValues',
            'request': {'params': ['dsConnectionId', 'time', 'field']},
            'response': {'type': 'list'}
        })

    # number operators
    number_ops = filter_config and filter_config.get('numberOps')
    if not number_ops:
        number_ops = [
            FilterOperators.EQUAL,
            FilterOperators.NOT_EQUAL,
            FilterOperators.GT,
            FilterOperators.GE,
            FilterOperators.LT,
            FilterOperators.LE
        ]

    option = {'default_equal': 'equal', 'default': FilterOperators.GT, 'name': _('Advanced'),
              'code': 'advance', 'items': []}
    result['number'] = {'options': [option]}
    for operator in number_ops:
        if operator in [FilterOperators.IS_NULL, FilterOperators.IS_NOT_NULL]:
            option['items'].append(_make_filter_option_item(operator, '', '', translate))
        else:
            option['items'].append(_make_filter_option_item(operator, 'inputNumber',
                                                            'number', translate))

    if FilterOperators.LE in number_ops and FilterOperators.GE in number_ops:
        option['items'].append({
            'options': {'between': True},
            'code': 'between',
            'cType': 'inputNumber',
            'name': _('Between')
        })

    # date
    date_ops = filter_config and filter_config.get('dateOps')
    if not date_ops:
        date_ops = [
            FilterOperators.EQUAL,
            FilterOperators.NOT_EQUAL,
            FilterOperators.GE,
            FilterOperators.LE,
            FilterOperators.IS_NULL,
            FilterOperators.IS_NOT_NULL
        ]

    option = {'default': FilterOperators.GE, 'default_equal': 'equal',
              'name': _('Advanced'), 'code': 'advance', 'items': []}
    result['date'] = {'options': [option]}
    for operator in date_ops:
        if operator in [FilterOperators.IS_NULL, FilterOperators.IS_NOT_NULL]:
            option['items'].append(_make_filter_option_item(operator, '', '', translate))
        else:
            option['items'].append(_make_filter_option_item(operator, 'date', 'date', translate))

    if FilterOperators.LE in date_ops and FilterOperators.GE in date_ops:
        option['items'].append({
            'options': {'between': True},
            'code': 'between',
            'cType': 'date',
            'name': _('Between')
        })

    return result


FILTER_OPERATOR_NAME_MAPPING = {
    (FilterOperators.IN_LIST, ''): 'Include',
    (FilterOperators.NOT_IN_LIST, ''): 'Exclude',
    (FilterOperators.STR_CONTAIN, ''): 'Contains',
    (FilterOperators.STR_NOT_CONTAIN, ''): 'Does not contain',
    (FilterOperators.STR_BEGIN_WITH, ''): 'Begin with',
    (FilterOperators.STR_NOT_BEGIN_WITH, ''): 'Does not begin with',
    (FilterOperators.STR_END_WITH, ''): 'End with',
    (FilterOperators.STR_NOT_END_WITH, ''): 'Does not end with',
    (FilterOperators.REGEX_MATCH, ''): 'Matches RegEx',
    (FilterOperators.REGEX_NOT_MATCH, ''): 'Does not match RegEx',
    (FilterOperators.EQUAL, 'date'): 'On',
    (FilterOperators.EQUAL, 'number'): 'Equal to',
    (FilterOperators.EQUAL, ''): 'Exactly match',
    (FilterOperators.NOT_EQUAL, 'date'): 'Is not on',
    (FilterOperators.NOT_EQUAL, 'number'): 'Not equal to',
    (FilterOperators.NOT_EQUAL, ''): 'Does not exactly match',
    (FilterOperators.GT, ''): 'Greater than',
    (FilterOperators.GE, 'date'): 'On or after',
    (FilterOperators.GE, ''): 'Greater than or equal to',
    (FilterOperators.LT, ''): 'Less than',
    (FilterOperators.LE, 'date'): 'On or before',
    (FilterOperators.LE, ''): 'Less than or equal to',
    (FilterOperators.IS_NULL, ''): 'Is blank',
    (FilterOperators.IS_NOT_NULL, ''): 'Is not blank',
}


def _make_filter_option_item(operator, c_type, data_type, translate):
    _ = translate
    item = {'code': operator, 'cType': c_type}
    key = (operator, data_type)
    name = FILTER_OPERATOR_NAME_MAPPING.get(key)
    if not name:
        key = (operator, '')
        name = FILTER_OPERATOR_NAME_MAPPING.get(key)

    assert name
    item['name'] = _(name)
    return item


def _make_default_time_group(translate):
    _ = translate
    return [
        {'code': 'year', 'name': _('Year')},
        {'code': 'quarter', 'name': _('Quarter')},
        {'code': 'month', 'name': _('Month')},
        {'code': 'week', 'name': _('Week')},
        {'code': 'day', 'name': _('Day')},
        {'code': 'hour', 'name': _('Hour')},
        {'code': 'minute', 'name': _('Minute')},
        {'code': 'seconds', 'name': _('Seconds')}
    ]


def _make_default_graphs(support_map, translate):
    _ = translate
    result = [
        {'code': 'table', 'name': _('Table')},
        {'code': 'column', 'name': _('Column')},
        {'code': 'bar', 'name': _('Bar')},
        {'code': 'stackColumn', 'name': _('Stacked Column')},
        {'code': 'stackBar', 'name': _('Stacked Bar')},
        {'code': 'line', 'name': _('Line')},
        {'code': 'area', 'name': _('Area')},
        {'code': 'doubleAxis', 'name': _('Grouped Column')},
        {'code': 'pie', 'name': _('Pie')},
        {'code': 'number', 'name': _('Single Value')},
        {'code': 'progressbar', 'name': _('Progress Bar')}
    ]
    if support_map:
        result.append({'code': 'map', 'name': _('Map')})

    result.append({'code': 'funnel', 'name': _('Funnel')})
    result.append({'code': 'bubble', 'name': _('Bubble')})

    return result


def _make_time_config(date_range_config, translate):

    if date_range_config and date_range_config.get('enabled') is False:
        return {}

    _ = translate
    result = {}

    if date_range_config:
        result['supportSelectDateFields'] = \
            date_range_config.get('supportDateRangeFieldSelection', False)
    else:
        result['supportSelectDateFields'] = True

    result['default'] = 'past'  # TODO: specify default in datasource config
    result['items'] = items = []

    if date_range_config and date_range_config.get('supportAllTime'):
        items.append({'code': 'all_time', 'name': _('All Time')})

    items.append({'code': 'category', 'name': _('Current')})
    items.append({'code': 'today', 'name': _('Today')})
    items.append({'code': 'this_week', 'name': _('This Week')})
    items.append({'code': 'this_month', 'name': _('This Month')})
    items.append({'code': 'this_year', 'name': _('This Year')})
    items.append({'code': 'separator', 'name': ''})

    items.append({'code': 'category', 'name': _('Past')})
    items.append({'code': 'yesterday', 'name': _('Yesterday')})
    items.append({'code': 'last_week', 'name': _('Last Week')})
    items.append({'code': 'last_month', 'name': _('Last Month')})
    items.append({'code': 'last_year', 'name': _('Last Year')})
    items.append({
        'code': 'past',
        'name': _('Past ... days'),
        'type': 'number',
        'configs': {
            'includeToday': False,
            'min': 1,
            'max': 999
        }})

    if date_range_config and date_range_config.get('supportFuture'):
        items.append({'code': 'separator', 'name': ''})
        items.append({'code': 'category', 'name': _('Future')})
        items.append({'code': 'tomorrow', 'name': _('Tomorrow')})
        items.append({'code': 'next_week', 'name': _('Next Week')})
        items.append({'code': 'next_month', 'name': _('Next Month')})
        items.append({'code': 'next_year', 'name': _('Next Year')})
        items.append({
            'code': 'next',
            'name': _('Next ... days'),
            'type': 'number',
            'configs': {
                'includeToday': False,
                'min': 1,
                'max': 999
            }})

    items.append({'code': 'separator', 'name': ''})
    items.append({'code': 'category', 'name': _('Custom')})
    items.append({'code': 'custom_today', 'name': _('Custom date to today'), 'type': 'single'})
    items.append({'code': 'custom', 'name': _('Custom date range'), 'type': 'range'})

    return result
