"""REST API input/output schemas"""
# pylint: disable=global-statement
# pylint: disable=invalid-name

from flask_restplus import fields

from common.model.flask_restplus_custom_fields import Timestamp
from common.schemas.schemas import init_common_models

connection_create_model = None
connection_read_model = None
connection_table_read_model = None
connection_table_create_model = None
field_model = None
segment_model = None
connection_account_read_model = None
hierarchy_read_model = None
data_request_model = None
data_response_model = None
table_preview_data_response_model = None
custom_segment_read_model = None
custom_segment_list_read_model = None
custom_segment_create_expect_model = None
custom_segment_update_expect_model = None
share_connection_expect_model = None
transfer_data_expect_model = None
calculated_field_response_model = None
calculated_field_request_model = None
etl_datasource_save_read_model = None
etl_datasource_get_read_model = None


def init_models(api):
    """Initializes REST models with the given api"""

    init_common_models(api)

    global data_request_model

    field_info = api.model('fieldInfo', {
        'id' : fields.String,
        'groupBy' : fields.Boolean,
        'agg': fields.String(
            enum=['sum', 'average', 'min', 'max', 'var', 'stdev', 'counta', 'dcount']),
        'uuid': fields.String
    })

    data_request_model = api.model('BusinessDataRequestPayload', {
        'path': fields.List(fields.String),
        'locale': fields.String,
        'paging': fields.Raw,
        'columns': fields.List(fields.String),
        'fields': fields.List(fields.Nested(field_info)),
        'segment': fields.Raw,
        'compareWithPrevious': fields.Raw,
        'filters': fields.List(fields.Raw),
        'sort': fields.Raw,
        'dateRange': fields.Raw,
        'timezone': fields.String,
        'weekStartOn': fields.String,
        'noCache': fields.Boolean(default=False)
    })

    global data_response_model
    data_response_model = api.model('BusinessDataResponsePayload', {
        'header': fields.List(fields.Raw),
        'data': fields.List(fields.List(fields.Raw)),
        'summaryValues': fields.List(fields.Float),
        'extra_info': fields.Raw
    })

    global connection_create_model
    connection_create_model = api.model('ConnectionCreate', {
        'name': fields.String,
        'user_id': fields.String,
        'space_id': fields.String,
        'ds_code': fields.String,
        'account_id': fields.String,
        'auth_type': fields.String,
        'auth_info': fields.String,
        'created_at': Timestamp,
        'last_updated_at': Timestamp,
        'share_users': fields.List(fields.Raw),
        'share_to_all': fields.Boolean,
        'share_to_all_access_level': fields.String(required=False),
        'share_connection': fields.Boolean(default=False)
    })

    global connection_read_model
    connection_read_model = api.inherit('ConnectionRead',
                                        connection_create_model,
                                        {'id': fields.String})

    global connection_table_create_model
    tabel_column_model = api.model('TableColumnModel', {
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
        'columns': fields.List(fields.Nested(tabel_column_model))
    })
    global connection_table_read_model
    connection_table_read_model = api.inherit('TableReadModel',
                                              connection_table_create_model,
                                              {
                                                  'id': fields.String(),
                                                  'created_at': Timestamp,
                                                  'last_updated_at': Timestamp
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

    global segment_model
    segment_model = api.model('Segment', {
        'id': fields.String(),
        'name': fields.String(),
        'is_custom': fields.Boolean(default=False)
    })

    global hierarchy_read_model
    hierarchy_item = api.model('ConnectionHierarchyItem', {
        'id' : fields.String(),
        'name' : fields.String(),
        'hasChild': fields.Boolean,
        'children': fields.List(fields.Raw)
    })
    hierarchy_read_model = api.model('ConnectionHierarcheyRead', {
        'items': fields.List(fields.Nested(hierarchy_item))
    })

    global connection_account_read_model
    connection_account_read_model = api.model('ConnectionAccountRead', {
        "success": fields.Boolean,
        "data": fields.Nested({
            "dataType": fields.String,
            "isNeedTranslateI18nCode": fields.Boolean,
            "isOnlyTranslateName": fields.Boolean,
            "value": fields.List(
                fields.Nested({
                    "displayName": fields.String,
                    "id": fields.String,
                    "instanceId": fields.String,
                    "name": fields.String,
                    "ownerId": fields.String,
                    "ownerName": fields.String,
                    "uid": fields.String,
                })
            )
        })
    })

    global table_preview_data_response_model
    table_preview_data_response_model = api.model('BusinessTablePreviewDataResponsePayload', {
        'fields': fields.List(fields.Nested(field_model)),
        'data': fields.List(fields.List(fields.Raw))
    })

    global custom_segment_read_model
    custom_segment_read_model = api.model('CustomSegmentModel', {
        "id": fields.String,
        "name": fields.String,
        "scope": fields.String,
        "operation": fields.String,
        "conditions": fields.List(fields.Raw),
        "space_id": fields.String,
        "user_id": fields.Integer,
        "ds_code": fields.String,
        "modifier_id": fields.Integer
    })

    global custom_segment_list_read_model
    custom_segment_list_read_model = api.model('CustomSegmentListModel', {
        "id": fields.String,
        "name": fields.String,
        "scope": fields.String,
        "operation": fields.String,
        "conditions": fields.List(fields.Raw),
        "space_id": fields.String,
        "user_id": fields.Integer,
        "ds_code": fields.String
    })

    global custom_segment_create_expect_model
    custom_segment_create_expect_model = api.model('CustomSegmentCreateExpectModel', {
        "spaceId": fields.String,
        "scope": fields.String,
        "operation": fields.String,
        "name": fields.String,
        "conditions": fields.List(fields.List(fields.Raw))
    })

    global custom_segment_update_expect_model
    custom_segment_update_expect_model = api.model('CustomSegmentUpdateExpectModel', {
        "spaceId": fields.String,
        "scope": fields.String,
        "operation": fields.String,
        "name": fields.String,
        "conditions": fields.List(fields.List(fields.Raw)),
        "segmentId": fields.String,
        "uid": fields.String
    })

    global share_connection_expect_model
    share_connection_expect_model = api.model('ShareConnectionExpectModel', {
        "accountInfo": fields.String,
        "cid": fields.String,
        "dataSourceCode": fields.String,
        "members": fields.List(fields.Raw),
        "shareToAllOperateType": fields.String,
        "spaceId": fields.String,
        "isShareToAll": fields.String(required=False),
        "shareToAllRoleCode": fields.String(required=False)
    })

    global transfer_data_expect_model
    transfer_data_expect_model = api.model("TransferDataExpectModel", {
        "oldUid": fields.String,
        "newUid": fields.String,
        "spaceId": fields.String
    })

    global calculated_field_response_model
    calculated_field_response_model = api.model('BusinessCalculatedFieldResponsePayload', {
        'id': fields.String,
        'connection': fields.String,
        'name': fields.String,
        'display': fields.String,
        'expression': fields.String,
        'fields': fields.List(fields.Raw),
        'keys': fields.List(fields.String),
        'type': fields.String(attribute='data_type'),
        'allow_filter': fields.Boolean,
        'filter_options': fields.List(fields.Raw),
        'allow_aggregation': fields.Boolean,
        'aggr_options': fields.List(fields.Raw),
        'function_contain': fields.Boolean,
        'group_function_contain': fields.Boolean,
    })

    global calculated_field_request_model
    calculated_field_request_model = api.model('BusinessCalculatedFieldRequestPayload', {
        'expression': fields.String,
        'candidates': fields.List(fields.Raw),
        'name': fields.String
    })

    global etl_datasource_save_read_model
    etl_datasource_save_read_model = api.model("EtlDatasourceReadModel", {
        "id": fields.String
    })

    global etl_datasource_get_read_model
    etl_datasource_get_read_model = api.model("EtlDatasourceGetReadModel", {
        "id": fields.String,
        "name": fields.String,
        "fields": fields.List(fields.Raw(required=False)),
        "time": fields.Raw(required=False),
        "filters": fields.List(fields.Raw(required=False)),
        "segment": fields.Raw(required=False),
        "sort": fields.Raw(required=False),
        "space_id": fields.String,
        "widget_connection_config_id": fields.String,
        "language": fields.String,
        "timezone": fields.String
    })
