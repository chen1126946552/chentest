'''REST API input/output schemas'''

from flask_restplus import fields

from common.model.flask_restplus_custom_fields import Timestamp
from common.schemas.schemas import init_common_models

connection_read_model = None
connection_create_model = None
connection_table_read_model = None
connection_table_create_model = None
datasource_read_model = None
datasource_create_model = None
datasource_auth_model = None
datasource_auth_callback_model = None
datasource_auth_validate_model = None
meta_request_model = None
field_model = None
hierarchy_request_model = None
hierarchy_response_model = None
segment_model = None
data_request_model = None
data_response_model = None
table_preview_data_request_model = None  # pylint: disable=invalid-name
table_preview_data_response_model = None  # pylint: disable=invalid-name
cal_field_validating_request_model = None  # pylint: disable=invalid-name
cal_field_validating_response_model = None  # pylint: disable=invalid-name


# pylint: disable=global-statement


def init_models(api):
    '''Initializes REST models with the given api'''

    init_common_models(api)

    global connection_create_model
    connection_create_model = api.model('ConnectionCreate', {
        'name': fields.String,
        'ds_code': fields.String,
        'account_id': fields.String,
        'auth_info': fields.String
    })

    global connection_read_model
    connection_read_model = api.inherit('ConnectionRead',
                                        connection_create_model,
                                        {
                                            'id': fields.String,
                                            'created_at': Timestamp,
                                            'last_updated_at': Timestamp
                                        })

    global connection_table_create_model
    table_column_model = api.model('TableColumnModel', {
        'id': fields.String,
        'code': fields.String,
        'name': fields.String,
        'include': fields.Boolean,
        'dataType': fields.String,
        'formatOptions': fields.Raw
    })
    connection_table_create_model = api.model('TableCreateModel', {
        'connection_id': fields.String,
        'name': fields.String,
        'database': fields.String,
        'columns': fields.List(fields.Nested(table_column_model), attribute='columns_populated')
    })
    global connection_table_read_model
    connection_table_read_model = api.inherit('TableReadModel',
                                              connection_table_create_model,
                                              {
                                                  'id': fields.String(),
                                                  'created_at': Timestamp,
                                                  'last_updated_at': Timestamp
                                              })

    global datasource_read_model
    datasource_read_model = api.model('Datasource',
                                      {
                                          'id': fields.String,
                                          'code': fields.String,
                                          'name': fields.String,
                                          'description': fields.String,
                                          'api_version': fields.String,
                                          'published': fields.Boolean,
                                          'config': fields.Raw,
                                          'ds_id': fields.Integer,
                                          'type': fields.String
                                      })

    global datasource_create_model
    datasource_create_model = datasource_read_model

    global datasource_auth_model
    datasource_auth_model = api.model('DatasourceAuth', {
        'type': fields.String(required=True),
        'oauth_uri': fields.String,
        'oauth_state': fields.String
    })

    global datasource_auth_callback_model
    datasource_auth_callback_model = api.model('DatasourceAuthCallBack', {
        'id': fields.String,
        'name': fields.String,
        'account_id': fields.String,
        'oauth_state': fields.String
    })

    global datasource_auth_validate_model
    datasource_auth_validate_model = api.model('DatasourceAuthValidate', {
        'status': fields.String,
        'message': fields.String
    })

    global meta_request_model
    meta_request_model = api.model('DatasourceMetaRequest', {
        'path': fields.List(
            fields.String()
        )
    })

    global field_model
    field_model = api.model('DatasourceField', {
        'id': fields.String(),
        'name': fields.String(required=True),
        'type': fields.String(enum=['string', 'number', 'date']),
        'allowFilter': fields.Boolean(default=True),
        'allowSegment': fields.Boolean(default=False),
        'filterOps': fields.List(
            fields.String(
                enum=['in_list',
                      'not_in_list',
                      'str_contain',
                      'str_not_contain',
                      'regex_match',
                      'regex_not_match',
                      'is_null',
                      'is_not_null',
                      'gt',
                      'ge',
                      'lt',
                      'le',
                      'equal',
                      'not_equal'])),
        'allowGroupby': fields.Boolean(default=True),
        'allowAggregation': fields.Boolean(default=False),
        'aggOps': fields.List(
            fields.String(
                enum=['sum', 'average', 'min', 'max', 'var', 'stdev', 'counta', 'dcount'])),
        'granularities': fields.List(
            fields.String(
                enum=['hour', 'day', 'week', 'month', 'quarter', 'year'])),
        'children': fields.List(fields.Raw)
    })

    global hierarchy_request_model
    hierarchy_request_model = api.model('HierarcheyRequest', {
        'path': fields.List(
            fields.String()
        ),
        'expandAll': fields.Boolean
    })

    global hierarchy_response_model
    hierarchy_item = api.model('HierarchyItem', {
        'id' : fields.String(),
        'name' : fields.String(),
        'hasChild': fields.Boolean,
        'children': fields.List(fields.Raw)
    })

    hierarchy_response_model = api.model('HierarcheyResponse', {
        'items': fields.Nested(hierarchy_item)
    })

    global segment_model

    segment_model = api.model('Segment', {
        'id' : fields.String(),
        'name' : fields.String()
    })

    global data_request_model
    data_request_model = api.model('DataManagerDataRequestPayload', {
        'path': fields.List(fields.String),
        'locale': fields.String,
        'paging': fields.Raw,
        'fields': fields.List(fields.Raw),
        'calculatedFields': fields.List(fields.Raw),
        'segment': fields.Raw,
        'compareWithPrevious': fields.Raw,
        'filters': fields.List(fields.Raw),
        'sort': fields.Raw,
        'dateRange': fields.Raw,
        'timezone': fields.String,
        'compareWithPreviousPeriod': fields.Raw,
        'weekStartOn': fields.String,
        'noCache': fields.Boolean(default=False),
        'dsInfo': fields.Raw

    })

    global data_response_model
    data_response_model = api.model('DataManagerDataResponsePayload', {
        'tokenUpdate': fields.Raw,
        'header': fields.List(fields.Raw),
        'data': fields.List(fields.List(fields.Raw)),
        'nextPageCursor': fields.String,
        'summaryValues': fields.List(fields.Float),
        'extra_info': fields.Raw
    })

    global table_preview_data_request_model # pylint: disable=invalid-name
    table_preview_data_request_model = api.model('DataManagerTablePreviewDataRequestPayload', {
        'path': fields.List(fields.String),
        'locale': fields.String,
        'timezoneOffset': fields.Integer
    })

    global table_preview_data_response_model  # pylint: disable=invalid-name
    table_preview_data_response_model = api.model('DataManagerTablePreviewDataResponsePayload', {
        'fields': fields.List(fields.Nested(field_model)),
        'data': fields.List(fields.List(fields.Raw))
    })

    global cal_field_validating_request_model  # pylint: disable=invalid-name
    cal_field_validating_request_model = api.model('CalculatedFieldValidatingRequestPayload', {
        'expression': fields.String,
        'keys': fields.List(fields.String)
    })

    global cal_field_validating_response_model  # pylint: disable=invalid-name
    cal_field_validating_response_model = api.model('CalculatedFieldValidatingResponsePayload', {
        'ok': fields.Boolean,
        'function_contain': fields.Boolean(default=False),
        'group_function_contain': fields.Boolean(default=False)
    })
