"""Constant used for v2 adaptors"""
from services.utils import NotMatchRaiseExceptionDict


class Constant:
    """Variety of constants to adapt to v2"""

    # v2's dsId field, will be removed in future
    DS_ID = "dsId"
    # to adapt v2's ds_id field, new vnext datasources with `dsId` >= `DS_ID_THRESHOLD`
    DS_ID_THRESHOLD = 1000
    # v2's global filter default time(date range) for searching field selections,
    # if no global date range offered, set this one(last 365 days)
    DEFAULT_GLOBAL_FILTER_DATERANGE_FOR_FIELD_SELECTIONS = \
        {'code': 'past', 'isIncludeToday': False, 'value': 365}


class Fields:
    """data fields related"""
    class NameMapping:
        """
        key is v2 vocabulary, value is vx.
        """

        # v2: [ PERCENT, CURRENCY, LOCATION_COUNTRY, LOCATION_REGION,
        # LOCATION_CITY, TEXT, DATE, DATETIME, TIME, INTEGER, FLOAT,
        # LONG, DOUBLE, NUMBER, DURATION, TIMESTAMP ]
        # vx:[ NUMBER, STRING, DATE ]

        type_map = NotMatchRaiseExceptionDict({
            'NUMBER': 'number',
            'INTEGER': 'number',
            'FLOAT': 'number',
            'LONG': 'number',
            'DOUBLE': 'number',
            'DURATION': 'number',
            'CURRENCY': 'number',
            'PERCENT': 'number',
            'TIMESTAMP': 'string',
            'STRING': 'string',
            'TEXT': 'string',
            'LOCATION_COUNTRY': 'string',
            'LOCATION_REGION': 'string',
            'LOCATION_CITY': 'string',
            'DATE': 'date',
            'DATETIME': 'date',
            'TIME': 'date'
        })
        # v2:['year', 'quarter', 'month', 'week', 'day', 'hour']
        # vx:[ Hour, Day, Week, Month, Quarter, Year ]
        granularity_map = NotMatchRaiseExceptionDict({
            'year': 'year',
            'quarter': 'quarter',
            'month': 'month',
            'week': 'week',
            'day': 'day',
            'hour': 'hour'
        })

        # v2: [SUM, AVG, MIN, MAX, VAR, STDEV, COUNTA, D_COUNT]
        # vx:[ sum, average, min, max, stdev, var, counta, dcount ]
        agg_map = NotMatchRaiseExceptionDict({
            'sum': 'sum',
            'average': 'average',
            'min': 'min',
            'max': 'max',
            'var': 'var',
            'stdev': 'stdev',
            'counta': 'counta',
            'countunique': 'dcount'
        })

        compare_with_previous_period_code_map = NotMatchRaiseExceptionDict({
            'compareWithPreviousPeriod': 'pop',
            'compareWithLastYear': 'yoy',
            'compareWithLastMonth': 'mom'
        })

        compare_with_previous_period_display_format_map = NotMatchRaiseExceptionDict({
            'growRate': ' - % Growth',
            'growValue': ' - Growth',
            'compareValue': ' - Previous value'
        })

        compare_with_previous_period_compute_map = NotMatchRaiseExceptionDict({
            'growRate': 'growth_rate',
            'growValue': 'growth',
            'compareValue': None
        })

        field_analysis_function_map = NotMatchRaiseExceptionDict({
            'occupy': 'proportion',
            'growthRate': 'growth_rate',
            'cumulate': 'cumulate',
            'none': None
        })


class SpecialCases:
    ga_scope_mapping = NotMatchRaiseExceptionDict({
        'users': 'User',
        'sessions': 'Session'
    })
