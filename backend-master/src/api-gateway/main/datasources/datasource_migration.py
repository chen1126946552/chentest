"""Migrate v2 datasource to vnext"""
from uuid import uuid1
from datetime import datetime
from functools import wraps
from urllib.parse import unquote, quote
import time
import sys
import copy
import json
import logging
import logging.config
import MySQLdb
import MySQLdb.cursors
import yaml
# pylint: disable=too-many-arguments, line-too-long, missing-docstring, too-many-locals, invalid-name, redefined-outer-name,
# pylint: disable=broad-except, too-many-instance-attributes, logging-fstring-interpolation


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

def error_catcher(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            migration = args[0]
            if migration.v2_conn:
                migration.v2_conn.ping(True)
            if migration.vnext_conn:
                migration.vnext_conn.ping(True)
            if migration.v3_conn:
                migration.v3_conn.ping(True)
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e, args)

    return wrapper

class DataSourceMigration:

    # overwrite by datasource
    auth_type = 'oauth'
    old_ds_code = 'googleanalysis'
    old_ds_id = 1
    new_ds_code = 'googleanalytics-v4'
    new_ds_id = 1001

    condition_code_v2_vnext_map = {
        'contain': 'str_contain',
        'not_contain': 'str_not_contain',
    }
    filter_select_v2_vnext_map = {
        'equal': 'in_list',
        'not_equal': 'not_in_list'
    }



    def __init__(self, v2_conn, vnext_conn, space_id, v3_conn):
        self.v2_conn = v2_conn
        self.vnext_conn = vnext_conn
        self.space_id = space_id
        self.v3_conn = v3_conn

        self.shared_connections = {}
        self.migrated_user_connections = []
        self.migrated_ds_connection = {}
        self.migrated_panel_global_components = []
        self.migrated_segments = {}
        self.migrated_shared_connections = {}
        self.migrated_etl_datasources = []
        self.migrated_etl_configs = {}
        self.migrated_cal_fields = []
        self.migrated_widgets = []

    #TODO: Use long
    def _get_or_default_datetime(self, config, key, is_millisecond=True):
        result = None
        if key in config:
            value = int(config.get(key))
            if not is_millisecond:
                value = value * 1000
            result = value

        return  result

    # overwrite by datasource
    def _get_auth_info(self, config):
        return {
            'access_token': config['accessToken'],
            'client_id': config['clientId'],
            'client_secret': config['clientSecret'],
            'exp': config['expireTime'],
            'iat': None,
            'refresh_token': config['refreshToken']
            }

    def _get_account_id(self, config):
        return config['accountName']


    def _create_or_find_dm_connection(self, connection):

        config = json.loads(connection['config'])

        account_name = self._get_account_id(config)

        query = f"select * from data_manager_connection where ds_code = '{self.new_ds_code}'"\
               + f" and account_id = '{account_name}'"

        with self.vnext_conn.cursor() as cursor:
            cursor.execute(query)
            dm_connection = cursor.fetchone()
            if dm_connection:
                return dm_connection['id']

        with self.vnext_conn.cursor() as cursor:
            id = str(uuid1())
            update_time = self._get_or_default_datetime(connection, 'update_time')
            auth_info = json.dumps(self._get_auth_info(config), ensure_ascii=False)

            query = f'insert into data_manager_connection (id, is_deleted, created_at, last_updated_at, name, ds_code, auth_type, auth_info, account_id)'\
                + f" values('{id}', 0, '{update_time}', '{update_time}', '{account_name}', '{self.new_ds_code}', '{self.auth_type}', %s, '{account_name}')"

            cursor.execute(query, (auth_info,))
            self.vnext_conn.commit()

            return id

    def _create_business_connection(self, connection):
        id = connection['connection_id']
        dm_connection_id = self._create_or_find_dm_connection(connection)
        update_time = self._get_or_default_datetime(connection, 'update_time')
        user_id = connection['uid']
        name = connection['name']
        config = json.loads(connection['config'])
        account_id = self._get_account_id(config)

        query = f'insert into business_connection (id, is_deleted, created_at, last_updated_at, user_id, space_id, ds_code, dm_connection_id, name, ds_account_id)' \
            + f" values('{id}', 0, '{update_time}', '{update_time}', {user_id}, '{self.space_id}', '{self.new_ds_code}', '{dm_connection_id}', '{name}', '{account_id}')"

        with self.vnext_conn.cursor() as cursor:
            cursor.execute(query)
            self.vnext_conn.commit()

        return id

    @error_catcher
    def _migrate_ds_connection(self, ds_config):
        config = json.loads(ds_config['config'])
        ds_connection_id = ds_config['ds_connection_id']
        account_info, profile_info = config

        connection_id = account_info['id']

        # for shared connection need to change it to the oringial connection
        if connection_id in self.shared_connections:
            original_connection_id = self.shared_connections[connection_id]
            account_info['id'] = original_connection_id
            profile_info['requestParams']['params']['account.id'] = original_connection_id

        # "168055156" to "[\"\", \"\", \"168055156\"]"
        old_id = profile_info['id']
        new_id = ['', '', old_id]
        profile_info['id'] = json.dumps(new_id, ensure_ascii=False)

        profile_info['requestParams']['provider'] = self.new_ds_code
        profile_info['uniqueField'] = 'legacyId'

        new_config = json.dumps(config, ensure_ascii=False)

        query = f"update ptone_ds_connection_config set config = %s, ds_id ={self.new_ds_id} " \
            + f" where ds_connection_id = '{ds_connection_id}' "

        with self.v2_conn.cursor() as cursor:
            cursor.execute(query, (new_config,))
            self.v2_conn.commit()
            self.migrated_ds_connection[ds_connection_id] = {'old_config':config, 'new_config':new_config}


    def _migrate_connection_share(self, connection):
        connection_id = connection['connection_id']

        query = "select UR.cid, CR.code, UR.uid as sid, C.uid as owner_id, C.is_share_to_all, UR.create_time, UR.modify_time " + \
        " from ptone_custom_user_role as UR left join ptone_custom_role CR on UR.role_id = CR.id " + \
        " left join user_connection as  C on UR.cid = C.connection_id where UR.is_delete =0 and C.status =1" + \
        f" and cid = '{connection_id}' and UR.individual_shared = 1"

        if connection['is_share_to_all']:
            role_id = connection['share_to_all_role_id']
            if role_id:
                role_code_query = f"select code from ptone_custom_role where id = {role_id}"
                with self.v2_conn.cursor() as cursor:
                    cursor.execute(role_code_query)
                    share_to_all_code = cursor.fetchone().get('code')
            else:
                share_to_all_code = 'read'

            rule = {
                'cid' : connection_id,
                'code' :share_to_all_code,
                'owner_id': connection['uid']
            }

            self.create_access_rule(rule, True)

        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            share_rules = cursor.fetchall()
            for rule in share_rules:
                self.create_access_rule(rule)

    def create_access_rule(self, rule, is_share_to_all=False):
        data = {
            'rule_id':str(uuid1()),
            'resource_id': rule['cid'],
            'resource_type': 'connection',
            'space_id': self.space_id,
            'group_id': 'SPACE' if  is_share_to_all else None,
            'user_id': None if is_share_to_all else rule['sid'],
            'last_updated_at': self._get_or_default_datetime(rule, 'modify_time', False),
            'owner_id': rule['owner_id'],
            'create_time': self._get_or_default_datetime(rule, 'create_time', False),
            'access_level' : rule['code']
            }

        group_id_value = " ='SPACE'" if is_share_to_all else 'is NULL'
        user_id_value = 'is NULL' if is_share_to_all else f"={rule['sid']}"

        query = "insert into business_access_rule (id, is_deleted, resource_id, resource_type, space_id, group_id, user_id, owner_id, created_at, last_updated_at, access_level) " \
            "select %(rule_id)s, 0, %(resource_id)s,%(resource_type)s,%(space_id)s, %(group_id)s, %(user_id)s, %(owner_id)s, %(create_time)s, %(last_updated_at)s, %(access_level)s from dual where not EXISTS " \
            f"(select id from business_access_rule where resource_id = %(resource_id)s and space_id = %(space_id)s and user_id {user_id_value} and group_id {group_id_value} and is_deleted = 0)"


        with self.vnext_conn.cursor() as cursor:
            cursor.execute(query, data)
            self.vnext_conn.commit()


    def migrate_connections(self):
        query = f'select * from user_connection where status = 1 AND share_connection = 0 ' \
            + f" and space_id = '{self.space_id}' AND ds_code ='{self.old_ds_code}'"

        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            connections = cursor.fetchall()
            for connection in connections:
                self._create_business_connection(connection)
                self._migrate_connection_share(connection)
                self.migrated_user_connections.append(connection['connection_id'])

    @error_catcher
    def _get_shared_connection(self):
        query = f'select * from user_connection where status = 1 AND share_connection = 1 ' \
            + f" and space_id = '{self.space_id}' AND ds_code ='{self.old_ds_code}'"
        result = {}
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            for share_connection in cursor.fetchall():
                result[share_connection['connection_id']] = share_connection['share_connection_id']

        return result


    def migrate_ds_connections(self):
        query = f'select * from ptone_ds_connection_config where status = 1 AND is_delete= 0 ' \
            + f" and space_id = '{self.space_id}' AND ds_id ={self.old_ds_id}" \

        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            ds_connections = cursor.fetchall()
            for ds_connection in ds_connections:
                self._migrate_ds_connection(ds_connection)

    @error_catcher
    def migrate_calculated_fields(self):
        query = f"select * from user_compound_metrics_dimension where ds_id={self.old_ds_id}" \
            + f" and space_id = '{self.space_id}' and is_delete =0 "
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            cal_fields = cursor.fetchall()
            for calf in cal_fields:
                self._migrate_calculated_field(calf)

    @error_catcher
    def _migrate_calculated_field(self, calf):
        from services.adaptors.calculated_field import calculated_field_params_parse
        _id = calf['id']
        name = calf['name']
        connection = calf['connection_id']

        if connection in self.shared_connections:
            connection = self.shared_connections[connection]

        original_aggregator = calf['original_aggregator']
        items = json.loads(calf['items_data'])
        create_at = calf['create_time']
        last_update_at = calf['modify_time']
        is_delete = calf['is_delete']
        space_id = calf['space_id']

        # insert into vx db
        parsed = calculated_field_params_parse(
            {'originalAggregator': original_aggregator, 'items': items, 'name': name})
        _connection = connection
        _space_id = space_id
        _expression = parsed['expression']
        _candidates = json.dumps(parsed['candidates'], ensure_ascii=False)
        _type = 'number'
        _name = name
        _is_deleted = is_delete
        _create_at = int(time.mktime(datetime.strptime(create_at, "%Y-%m-%d %H:%M:%S").timetuple()) * 1000)
        _last_updated_at = int(time.mktime(datetime.strptime(last_update_at, "%Y-%m-%d %H:%M:%S").timetuple()) * 1000)
        query = f"insert into business_calculated_field (id, created_at, last_updated_at, is_deleted, connection, space_id, name, display, expression, " \
                f"candidates, function_contain, group_function_contain, type, allow_filter, allow_aggregation) " \
                f"values ('{_id}',{_create_at},{_last_updated_at},{_is_deleted},'{_connection}','{_space_id}', '{_name}','{_name}','{_expression}','{_candidates}',0,0,'number',0,0)"
        with self.vnext_conn.cursor() as cursor:
            cursor.execute(query)
        self.vnext_conn.commit()
        self.migrated_cal_fields.append(_id)

    @error_catcher
    def _migrate_global_filter(self, global_filter):
        self._convert_global_filter_code(global_filter)
        config = json.loads(global_filter['value'])
        profile = config['profile']
        profile['dsCode'] = self.new_ds_code
        profile['dsId'] = self.new_ds_id
        profile_id = profile['profileId']
        new_profile_id = json.dumps(["", "", profile_id], ensure_ascii=False)
        profile['profileId'] = new_profile_id
        profile['id'] = profile['id'].replace(f'|{self.old_ds_code}', f'|{self.new_ds_code}').\
            replace(f'{profile_id}|', f"{new_profile_id}|")

        if profile['connectionId'] in self.shared_connections:
            profile['connectionId'] = self.shared_connections[profile['connectionId']]

        new_config = json.dumps(config, ensure_ascii=False)
        query = f"update panel_global_component set value = %s where id = {global_filter['id']}"

        with self.v2_conn.cursor() as cursor:
            cursor.execute(query, (new_config,))
            self.v2_conn.commit()

    @error_catcher
    def migrate_global_filters(self):
        query = f'SELECT * FROM panel_global_component pgc'\
            + f" WHERE pgc.`code` ='GLOBAL_FILTER' AND pgc.status =1 AND pgc.space_id = '{self.space_id}'"

        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            for global_filter in cursor.fetchall():
                config = json.loads(global_filter['value'])
                if config['profile']['dsCode'] == self.old_ds_code:
                    self._migrate_global_filter(global_filter)
                    self.migrated_panel_global_components.append(global_filter['component_id'])

    @error_catcher
    def _migrate_segment(self, segment):
        # add segment for all the connections
        create_time = int(time.mktime(datetime.strptime(segment['create_time'], "%Y-%m-%d %H:%M:%S").timetuple()) * 1000)
        last_updated_at = int(time.mktime(datetime.strptime(segment['modify_time'], "%Y-%m-%d %H:%M:%S").timetuple()) * 1000)
        name = segment['name']
        scope = segment['scope']
        operation = segment['operation']
        user_id = segment['uid']
        modifier_id = segment['modifier_id']
        self._convert_segment_condition_operator(segment)
        created_ids = {}

        for connection_id in self.migrated_user_connections:
            id = str(uuid1())
            query = f"insert into business_segment"\
                 + "(id, created_at, last_updated_at, is_deleted, name, scope, operation, conditions, space_id, user_id, ds_code, modifier_id, connection_id)" \
                 + f"values ('{id}', '{create_time}', '{last_updated_at}', 0, '{name}', '{scope}', '{operation}', %s, '{self.space_id}', {user_id}, '{self.new_ds_code}', {modifier_id}, '{connection_id}')"

            with self.vnext_conn.cursor() as cursor:
                cursor.execute(query, (segment['conditions'],))
                self.vnext_conn.commit()
                created_ids[connection_id] = id

        self.migrated_segments[segment['segment_id']] = created_ids

    def _convert_segment_condition_operator(self, segment):
        conditions_list = json.loads(segment['conditions'])
        for condition in conditions_list:
            for c in condition:
                operator = c['operator']
                if operator in self.condition_code_v2_vnext_map:
                    c['operator'] = self.condition_code_v2_vnext_map[operator]
        segment['conditions'] = json.dumps(conditions_list, ensure_ascii=False)

    def _convert_widget_filter_code(self, widget):
        """Convert widget filter condition code v2 to vnext"""
        filter_data = widget.get('filter_data')
        if filter_data and filter_data not in ['null', '[]']:
            filter_data_list = json.loads(filter_data)
            for f in filter_data_list:
                self._convert_filter_code(f)
            widget['filter_data'] = json.dumps(filter_data_list, ensure_ascii=False)

    def _convert_filter_code(self, f):
        if f and f.get('dataType') == 'STRING':
            _type = f.get('setting', {}).get('type')
            if _type == 'select':
                for item in f['setting']['items']:
                    code = item['code']
                    if code in self.filter_select_v2_vnext_map:
                        item['code'] = self.filter_select_v2_vnext_map[code]
            elif _type == 'advance':
                for item in f['setting']['items']:
                    code = item['code']
                    if code in self.condition_code_v2_vnext_map:
                        item['code'] = self.condition_code_v2_vnext_map[code]

    def _convert_global_filter_code(self, global_filter):
        field = global_filter.get('field')
        if field and field not in ['null', '[]']:
            global_filter_dict = json.loads(field)
            self._convert_filter_code(global_filter_dict)
            global_filter['field'] = json.dumps(global_filter_dict, ensure_ascii=False)

    @error_catcher
    def migrate_segments(self):
        query = f"SELECT * FROM ptone_segment_info WHERE space_id = '{self.space_id}'"\
            + f" and ds_code = '{self.old_ds_code}'"

        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            for segment in cursor.fetchall():
                self._migrate_segment(segment)

    @error_catcher
    def migrate_etl_datasources(self):
        query = f"SELECT a.* from etl_dataset_datasource a, ptone_ds_connection_config b where a.ds_connection_id = b.ds_connection_id  and b.ds_id={self.new_ds_id} and a.space_id = '{self.space_id}'"
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            for etl_datasource in cursor.fetchall():
                self._migrate_etl_datasource(etl_datasource)
        self._migrate_v3_etl_config()

    def migrate_finished_delete(self, table_name, where_field, field_val):
        delete_sql = f"update {table_name} set is_delete=1 where {where_field}='{field_val}'"
        with self.v2_conn.cursor() as cursor:
            cursor.execute(delete_sql)
            self.v2_conn.commit()

    @error_catcher
    def _etl_config_update_ds_code(self, config):
        c_id = config['id']
        data_source_list_str = config['data_source_list']
        data_source_list = json.loads(data_source_list_str)
        old_data_source_list = copy.deepcopy(data_source_list)
        is_save = False
        for datasource in data_source_list:
            ds_info = datasource['dsInfo']
            if ds_info.get("dsId") == self.old_ds_id:
                ds_info['dsId'] = self.new_ds_id
                ds_info['dataSourceCode'] = self.new_ds_code
                is_save = True
        if is_save:
            update_etl_sql = f"update datadeck_etl_config set data_source_list = '{json.dumps(data_source_list, ensure_ascii=False)}' where id = '{c_id}'"
            with self.v3_conn.cursor() as cursor:
                cursor.execute(update_etl_sql)
                self.v3_conn.commit()
                self.migrated_etl_configs[c_id] = {'old': old_data_source_list, 'new': data_source_list}

    @error_catcher
    def _migrate_v3_etl_config(self):
        query_sql = f"select b.* from datadeck_data_set a INNER JOIN datadeck_etl_config b on a.data_set_id=b.data_set_id where a.space_id='{self.space_id}'"
        with self.v3_conn.cursor() as cursor:
            cursor.execute(query_sql)
            for config in cursor.fetchall():
                self._etl_config_update_ds_code(config)

    def _etl_datasource_segment_update(self, segment, widget_connection_config_id):
        query_ds_conn_config = f"select * from ptone_ds_connection_config c where c.ds_connection_id='{widget_connection_config_id}'"
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query_ds_conn_config)
            config_map = cursor.fetchone()
            config_json = json.loads(config_map['config'])
            if config_json:
                bussin_conn_id = config_json[0]['id']
                old_id = segment['id']
                old_segm_map = self.migrated_segments.get(old_id)
                if old_segm_map:
                    new_segment_id = old_segm_map.get(bussin_conn_id)
                    if new_segment_id:
                        segment['id'] = new_segment_id

    @error_catcher
    def _migrate_etl_datasource(self, etl_datasource):

        id = etl_datasource['datasource_id']
        name = etl_datasource['name']
        fields = etl_datasource['fields']
        time = etl_datasource.get("time")
        filters = etl_datasource.get("filters")
        segment = etl_datasource.get("segment")
        sort = etl_datasource.get("sort")
        space_id = etl_datasource['space_id']
        widget_connection_config_id = etl_datasource['ds_connection_id']
        language = etl_datasource['language']
        timezone = etl_datasource['timezone']
        created_at = etl_datasource['create_time']

        null_list = ['null', '[]']

        data_dict = {
            "id": id,
            "name": name,
            "fields": fields if fields not in null_list else None,
            "time": time if time not in null_list else None,
            "filters": filters if filters not in null_list else None,
            "segment": segment if segment not in null_list else None,
            "sort": sort if sort not in null_list else None,
            "space_id": space_id,
            "widget_connection_config_id": widget_connection_config_id,
            "language": language,
            "timezone": timezone,
            "created_at": created_at,
            "is_deleted": 0,
            'status': 0
        }
        # segment
        if data_dict['segment']:
            segment_json = json.loads(segment)
            self._etl_datasource_segment_update(segment_json, widget_connection_config_id)
            data_dict['segment'] = json.dumps(segment_json, ensure_ascii=False)

        # filter
        if data_dict['filters']:
            filter_list = json.loads(data_dict['filters'])
            for f in filter_list:
                self._convert_filter_code(f)
                data_dict['filters'] = json.dumps(filter_list, ensure_ascii=False)

        columns_sql = ''
        values_sql = ''
        for column, value in data_dict.items():
            if value or column in ('is_deleted', 'status'):
                columns_sql += f"`{column}`,"
                values_sql += f"'{value}',"
        insert_sql = f"insert into business_etl_datasource({columns_sql[:-1]}) values ({values_sql[:-1]})"

        with self.vnext_conn.cursor() as cursor:
            cursor.execute(insert_sql)
            self.migrate_finished_delete('etl_dataset_datasource', 'datasource_id', id)
            self.vnext_conn.commit()
            self.migrated_etl_datasources.append(id)

    @error_catcher
    def migrate_widgets(self):
        query = f"SELECT * FROM ga_widget_info WHERE widget_id in (select widget_id from ptone_widget_info where space_id ='{self.space_id}') "\
            + f" and ds_id = '{self.old_ds_id}'"

        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            for widget in cursor.fetchall():
                self._migrate_widget(widget)

    @error_catcher
    def _migrate_widget(self, widget, update_sql_statments='', update_fields=()):
        #fields
        fields_str = widget['fields']
        if fields_str:
            fields = json.loads(fields_str)
            change_types = ['PERCENT', 'DATE']

            for field in fields:
                data_type = field['dataType'].upper()
                if data_type in change_types:
                    if data_type == 'PERCENT':
                        field['dataFormat'] = 'percentage'

                    if data_type == 'DATE':
                        data_format = field['dataFormat'].lower()
                        if data_format == 'yyyymmdd':
                            data_format = 'day'
                        elif data_format == 'yyyy':
                            data_format = 'year'
                        elif data_format == 'yyyymm':
                            data_format = 'month'
                        elif data_format == 'yyyymmddhh':
                            data_format = 'hour'
                            field['dataType'] = 'STRING'

                        field['dataFormat'] = data_format
                    update_sql_statments += ',fields = %s '
                    new_field_str = json.dumps(fields, ensure_ascii=False)
                    update_fields += (new_field_str,)

        #segment
        segments_str = widget['segment_data']
        if segments_str:
            segment = json.loads(segments_str)
            if 'type' not in segment or not segment['type']:
                segment_id = segment['id']
                if not segment_id in self.migrated_segments:
                    logger.error(f'[ERROR] segment_id : {segment_id}, widget: {widget}')
                else:
                    migrated_segment_ids = self.migrated_segments[segment_id]
                    ds_connection_id = widget['ds_connection_id']
                    migrated_ds_connection = self.migrated_ds_connection[ds_connection_id]

                    if not migrated_ds_connection:
                        logger.error(f'[ERROR] ds_connection_id : {ds_connection_id}, widget: {widget}')
                    else:
                        connection_id = migrated_ds_connection['old_config'][0]['id']
                        new_segment_id = migrated_segment_ids[connection_id]
                        segment['id'] = new_segment_id
                        new_segments_str = json.dumps(segment, ensure_ascii=False)
                        update_sql_statments += ',segment_data = %s '
                        update_fields += (new_segments_str,)
        # filter
        filter_data = widget.get('filter_data')
        self._convert_widget_filter_code(widget)
        new_filter_data = widget.get('filter_data')
        if filter_data != new_filter_data:
            update_sql_statments += ',filter_data = %s '
            update_fields += (new_filter_data,)

        # update
        if update_fields:
            widget_id = widget['Widget_ID']
            sql = f"update ga_widget_info set Widget_ID = '{widget_id}' {update_sql_statments} where Widget_ID = '{widget_id}'"
            with self.v2_conn.cursor() as cursor:
                cursor.execute(sql, update_fields)
                self.v2_conn.commit()
                self.migrated_widgets.append(widget_id)

    def migrate_template_panel(self, panel_id):
        sql = f" SELECT gw.* from ptone_widget_info w left join ptone_panel_info p on w.panel_id = p.panel_id" \
            + f" left join ga_widget_info gw on w.widget_id = gw.widget_id " \
            + f" left join ptone_ds_connection_config dsc on gw.ds_connection_id = dsc.ds_connection_id "\
            + f" where p.panel_id = '{panel_id}' and dsc.ds_id = {self.old_ds_id} "\
            + f" and p.status = 1 and w.status = 1 and w.widget_type = 'chart' "

        ds_connection_ids = []
        with self.v2_conn.cursor() as cursor:
            cursor.execute(sql)
            widgets = cursor.fetchall()

            ds_connection_ids = {widget['ds_connection_id'] for widget in widgets}
            ds_connection_map = {old_id:self._copy_ds_info(old_id) for old_id in ds_connection_ids}
            logger.info(f"ds_connection_map: {ds_connection_map}")

            for widget in widgets:
                old_ds_connection_id = widget['ds_connection_id']
                new_ds_connection_id = ds_connection_map[old_ds_connection_id]
                self._migrate_widget(widget, ',ds_connection_id = %s ', (new_ds_connection_id,))

    def _copy_ds_info(self, ds_connection_id):
        query = f"SELECT * FROM ptone_ds_connection_config WHERE ds_connection_id = '{ds_connection_id}'"
        new_ds_connection_id = str(uuid1())
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            ds_config = cursor.fetchone()
            ds_config['ds_connection_id'] = new_ds_connection_id
            del ds_config['id']
            ds_config['ds_id'] = self.new_ds_id
            config = json.loads(ds_config['config'])
            _, profile_info = config

            # "168055156" to "[\"\", \"\", \"168055156\"]"
            old_id = profile_info['id']
            new_id = ['', '', old_id]
            profile_info['id'] = json.dumps(new_id, ensure_ascii=False)

            profile_info['requestParams']['provider'] = self.new_ds_code
            profile_info['uniqueField'] = 'legacyId'
            new_config = json.dumps(config, ensure_ascii=False)
            ds_config['config'] = new_config
            self._insert('ptone_ds_connection_config', ds_config)

        return new_ds_connection_id

    def _insert(self, table, dict):
        fields = []
        values = []
        for key, val in dict.items():
            fields.append(key)
            values.append(val)

        query = 'INSERT INTO %s (%s) VALUES (%s)' % (
            table,
            ', '.join(fields),
            ', '.join(['%s'] * len(values))
        )
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query, values)
            self.v2_conn.commit()

    def migrate(self):
        self.shared_connections = self._get_shared_connection()
        self.migrate_connections()
        logger.info('connection is done')
        self.migrate_ds_connections()
        logger.info('dsconnection is done')
        self.migrate_global_filters()
        logger.info('global filter is done')
        self.migrate_segments()
        logger.info('segment is done')
        self.migrate_widgets()
        logger.info('widgets is done')
        self.migrate_etl_datasources()
        logger.info('etl datasource is done')
        self.migrate_calculated_fields()
        logger.info('etl datasource is done')

    def migrate_test(self):
        self.shared_connections = self._get_shared_connection()
        self.migrate_widgets()


class WigetTemplateMigration:

    old_ds_code = 'googleanalysis'
    old_ds_id = 1
    new_ds_code = 'googleanalytics-v4'
    new_ds_id = 1001

    def __init__(self, v2_conn, panel_id):
        self.v2_conn = v2_conn
        self.panel_id = panel_id
        self.widget_maps = {}

    def copy_widgets(self):
        query = f"SELECT pw.* FROM ptone_widget_info pw "\
            + f" LEFT JOIN ptone_widget_templet pwt on pw.widget_id = pwt.widget_id "\
            + f" LEFT JOIN ga_widget_info gw ON pw.widget_id = gw.widget_id"\
            + f" LEFT JOIN ptone_ds_connection_config ds_config ON gw.ds_connection_id = ds_config.ds_connection_id "\
            + f" WHERE pw.panel_id = '{self.panel_id}'"\
            + f" AND ds_config.ds_id = {self.old_ds_id}"\
            + f" AND pw.status = 1 "

        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            for widget in cursor.fetchall():
                self.copy_widget(widget)

        logger.info(self.widget_maps)
        self.update_layout()

    def update_layout(self):
        query = f"SELECT * from ptone_panel_info where Panel_ID = '{self.panel_id}'"
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            panel = cursor.fetchone()
            layout = json.loads(unquote(panel['Layout']))

            for old_widget_id, new_widget_id in self.widget_maps.items():
                old_layout = next((x for x in layout if x['id'] == old_widget_id))
                new_layout = old_layout.copy()
                new_layout['id'] = new_widget_id
                layout.append(new_layout)

            new_layout_str = quote(json.dumps(layout))
            update = f"UPDATE ptone_panel_info SET Layout = %s WHERE Panel_ID = '{self.panel_id}'"
            cursor.execute(update, (new_layout_str,))
            self.v2_conn.commit()


    def copy_widget(self, widget):
        old_widget_id = widget['Widget_ID']
        new_widget_id = str(uuid1())
        self.copy_widget_template(old_widget_id, new_widget_id)
        widget['Widget_ID'] = new_widget_id
        del widget['Ptone_Widget_Info_ID']
        self._insert('ptone_widget_info', widget)
        self._copy_ga_widget(old_widget_id, new_widget_id)
        self._copy_widget_variable(old_widget_id, new_widget_id)
        self.widget_maps[old_widget_id] = new_widget_id
        logger.info('Widget %s->%s', old_widget_id, new_widget_id)


    def copy_widget_template(self, widget_id, new_widget_id):
        query = f"SELECT * FROM ptone_widget_templet WHERE Widget_ID = '{widget_id}'"
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            widget_template = cursor.fetchone()
            del widget_template['Ptone_Widget_Info_ID']
            widget_template['Widget_ID'] = new_widget_id
            self._insert('ptone_widget_templet', widget_template)


    def _copy_widget_variable(self, widget_id, new_widget_id):
        query = f"SELECT * FROM ptone_widget_variable WHERE Widget_ID = '{widget_id}'"
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            widget_variable = cursor.fetchone()
            del widget_variable['Ptone_Widget_Variable_ID']
            variable_id = widget_variable['Variable_ID']
            new_variable_id = self._copy_variable(variable_id, new_widget_id)
            widget_variable['Variable_ID'] = new_variable_id
            widget_variable['Widget_ID'] = new_widget_id
            self._insert('ptone_widget_variable', widget_variable)


    def _copy_variable(self, variable_id, new_widget_id):
        query = f"SELECT * FROM ptone_variable_info WHERE Variable_ID = '{variable_id}'"
        new_variable_Id = str(uuid1())
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            variable = cursor.fetchone()
            del variable['Ptone_Variable_Info_ID']
            variable['Variable_ID'] = new_variable_Id
            variable['Widget_ID'] = new_widget_id
            self._insert('ptone_variable_info', variable)

        return new_variable_Id


    def _copy_ga_widget(self, widget_id, new_widget_id):
        query = f"SELECT * FROM ga_widget_info WHERE widget_id = '{widget_id}'"
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            ga_widget = cursor.fetchone()
            ga_widget['Widget_ID'] = new_widget_id
            ga_widget['Ds_Id'] = self.new_ds_id
            ds_connection_id = ga_widget['ds_connection_id']
            new_ds_connection_id = self._copy_ds_info(ds_connection_id)
            ga_widget['ds_connection_id'] = new_ds_connection_id
            del ga_widget['Ga_Widget_Info_ID']

            fields_str = ga_widget['fields']
            if fields_str:
                fields = json.loads(fields_str)
                change_types = ['PERCENT', 'DATE']
                for field in fields:
                    data_type = field['dataType'].upper()
                    if data_type in change_types:
                        if data_type == 'PERCENT':
                            field['dataFormat'] = 'percentage'

                        if data_type == 'DATE':
                            data_format = field['dataFormat'].lower()
                            if data_format == 'yyyymmdd':
                                data_format = 'day'
                            elif data_format == 'yyyy':
                                data_format = 'year'
                            elif data_format == 'yyyymm':
                                data_format = 'month'
                            elif data_format == 'yyyymmddhh':
                                data_format = 'hour'
                                field['dataType'] = 'STRING'
                            field['dataFormat'] = data_format

            new_field_str = json.dumps(fields, ensure_ascii=False)
            ga_widget['fields'] = new_field_str
            self._insert('ga_widget_info', ga_widget)

    def _copy_ds_info(self, ds_connection_id):
        query = f"SELECT * FROM ptone_ds_connection_config WHERE ds_connection_id = '{ds_connection_id}'"
        new_ds_connection_id = str(uuid1())
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query)
            ds_config = cursor.fetchone()
            ds_config['ds_connection_id'] = new_ds_connection_id
            del ds_config['id']
            ds_config['ds_id'] = self.new_ds_id
            config = json.loads(ds_config['config'])
            _, profile_info = config

            # "168055156" to "[\"\", \"\", \"168055156\"]"
            old_id = profile_info['id']
            new_id = ['', '', old_id]
            profile_info['id'] = json.dumps(new_id, ensure_ascii=False)

            profile_info['requestParams']['provider'] = self.new_ds_code
            profile_info['uniqueField'] = 'legacyId'
            new_config = json.dumps(config, ensure_ascii=False)
            ds_config['config'] = new_config
            self._insert('ptone_ds_connection_config', ds_config)

        return new_ds_connection_id



    def _insert(self, table, dict):
        fields = []
        values = []
        for key, val in dict.items():
            fields.append(key)
            values.append(val)

        query = 'INSERT INTO %s (%s) VALUES (%s)' % (
            table,
            ', '.join(fields),
            ', '.join(['%s'] * len(values))
        )
        with self.v2_conn.cursor() as cursor:
            cursor.execute(query, values)
            self.v2_conn.commit()

def create_connection(db_info):
    return MySQLdb.connect(user=db_info['user'], password=db_info['password'],
                           host=db_info['host'],
                           port=db_info['port'],
                           database=db_info['database'],
                           cursorclass=MySQLdb.cursors.DictCursor,
                           charset='utf8'
                           )



def space_migrate(info):
    v2_connection = create_connection(info['v2_db'])
    vnext_connection = create_connection(info['vnext_db'])
    v3_connection = create_connection(info['v3_db'])
    spaces = info['space_ids']

    for space_id in spaces:
        migration = DataSourceMigration(v2_connection, vnext_connection, space_id, v3_connection)
        migration.migrate()

    result = {x:y for x, y in migration.__dict__.items() if not x.endswith('_conn')}
    logger.info(json.dumps(result, ensure_ascii=False))

    v2_connection.close()
    vnext_connection.close()


def widget_tempalte_migrate(info):
    v2_connection = create_connection(info['v2_db_online'])
    panel_id = info['panel_id']
    widget_migration = WigetTemplateMigration(v2_connection, panel_id)
    widget_migration.copy_widgets()


def panel_template_migrate(info):
    v2_connection = create_connection(info['v2_db'])
    migration = DataSourceMigration(v2_connection, None, None, None)

    for panel_id in info['panel_template_ids']:
        migration.migrate_template_panel(panel_id)

def main(argv):
    input_file = argv[1]
    with open(input_file, encoding='utf-8') as f:
        info = json.load(f)
        panel_template_migrate(info)


if __name__ == '__main__':
    main(sys.argv)
