"""Business logic for managing business-layer connections"""

from __future__ import absolute_import

import json
import logging
from flask import g
from app import db
from common.http.utils import (ApiError, delete_json, get_headers, get_json,
                               post_json, put_json)
from exception import ArgumentError, BusinessError, EntityNotFoundError, ErrorCode
from models.connection import Connection as ConnectionModel
from models.connection import Segment as SegmentModel
from models.connection import Table as TableModel
from utils import resource_type

from .access_rule_service import get_by_space_resource_type
from .downstream import make_dm_connection_url, make_dm_datasource_url
from .utils import Fields

logger = logging.getLogger(__name__)


# pylint: disable=no-member,invalid-name,no-else-return


class Connection:
    """Connection related services."""

    # non-null/empty fields when creating a connection
    required_fields = ("user_id", "space_id", "dm_connection_id", "name",)

    @classmethod
    def get_connection_with_share_info(cls, owned_connection_list, user_id, space_id):
        """
        Get connection with share info
        Args:
            owned_connection_list: Owner's connection list
            user_id: user id
            space_id: space id

        Returns:
            All shared connection list
        """
        user_id = int(user_id)
        for owned_conn in owned_connection_list:
            cls._set_share_connection(owned_conn, False)

        access_rule_list = get_by_space_resource_type(space_id, resource_type.CONNECTION)
        shared_connection_list = cls._get_shared_connection(user_id, access_rule_list)
        all_conn_list = []
        all_conn_list.extend(owned_connection_list)
        # Remove the duplicate one
        for shared_conn in shared_connection_list:
            check_results = list(filter(lambda x, _conn=shared_conn:
                                        x.id == _conn.id, all_conn_list))
            if not check_results:
                all_conn_list.append(cls._set_share_connection(shared_conn, True))
        # Set shared User list
        for _all_conn in all_conn_list:
            rule_list = list(filter(lambda x, _conn=_all_conn:
                                    x.resource_id == _conn.id and
                                    bool(x.user_id), access_rule_list))
            setattr(_all_conn, "share_users", [cls._make_share_users(r) for r in rule_list])

            share_to_all_rule = list(filter(lambda x, _conn=_all_conn: x.resource_id == _conn.id and
                                            x.is_share_to_all(), access_rule_list))
            if share_to_all_rule:
                setattr(_all_conn, "share_to_all", True)
                setattr(_all_conn, "share_to_all_access_level", share_to_all_rule[0].access_level)
            else:
                setattr(_all_conn, "share_to_all", False)

        return all_conn_list

    @classmethod
    def _make_share_users(cls, rule):
        return {
            "user_id": rule.user_id,
            "status": "accepted",
            "owner": False,
            # TODO load user info
            "user_email": "xxxxxx",
            # TODO load user info
            "user_name": "xxxx",
            "role": {
                "code": rule.access_level
            }
        }

    @classmethod
    def _get_shared_connection(cls, user_id, access_rule_list):
        # filter owner
        shared_rule_list = list(
            filter(lambda x: x.user_id == user_id or (x.is_share_to_all()
                                                      and x.owner_id != user_id), access_rule_list))
        shared_conn_list = []
        if shared_rule_list:
            shared_conn_list = cls.get_by_ids([r.resource_id for r in shared_rule_list])
        return shared_conn_list

    @classmethod
    def _set_share_connection(cls, conn, val):
        setattr(conn, "share_connection", val)
        return conn

    @classmethod
    def get_by_ids(cls, id_list):
        """Get by id list"""
        return ConnectionModel.query.filter(db.and_(ConnectionModel.id.in_(id_list),
                                                    ConnectionModel.is_deleted == 0)).all()

    @classmethod
    def get_hierarchy_info(cls, conn_id, req_params):
        """
        Get connection account hierarchy
        Args:
            conn_id: connection id
            req_params: request params

        Returns: The hierarchy of processing completion
        """
        conn = cls.get_by_id(conn_id, raise_if_not_found=True)
        dm_url = make_dm_connection_url(f'/{conn.dm_connection_id}/hierarchy')
        result = post_json(dm_url, headers=get_headers(), body=req_params)
        return result

    @classmethod
    def get_by_space_id_and_ds_code_uid(cls, space_id, ds_code, user_id):
        """Gets the account corresponding to the connection according to spaceId"""
        return ConnectionModel.query.filter_by(
            space_id=space_id, ds_code=ds_code, user_id=user_id).all()

    @staticmethod
    def scan(filter_params):
        """scan all connections according to custom query kws"""

        return ConnectionModel.query.filter_by(**filter_params).all()

    @classmethod
    def get_all(cls, user_id, space_id):
        """Get all connections under one space(obviously, one user) scope"""

        return ConnectionModel.query.filter_by(
            user_id=user_id, space_id=space_id).all()

    @classmethod
    def get_by_id(cls, _id, raise_if_not_found=False):
        """Gets a connection by id"""

        connection = ConnectionModel.query.filter_by(id=_id).first()
        if raise_if_not_found and not connection:
            raise EntityNotFoundError(error_code=ErrorCode.CONNECTION_NOT_FOUND, locale=g.locale)
        return connection

    @classmethod
    def insert_or_recover(cls, data):
        """
        insert or update(on duplicate dm_connection_id) an connection from mapping fields
        :param data: connection fields map
        :return: connection created or updated
        """
        if not isinstance(data, dict) or not all([data.get(_) for _ in cls.required_fields]):
            raise ArgumentError("Insert or update Connection fields invalid.")
        conn = ConnectionModel(**data)

        # if some deleted connection with same user_id/space_id/ds_account_id is found
        # recover it!
        existing = ConnectionModel.query.with_deleted().filter_by(
            user_id=conn.user_id,
            space_id=conn.space_id,
            ds_account_id=conn.ds_account_id).first()

        if existing:
            data.update({'is_deleted': False})
            cls._connection_instance_update(existing, data)
            logger.info('Updating existing connection: %s', existing)
            db.session.commit()
            return existing

        logger.info('Creating new connection: %s', conn)
        db.session.add(conn)
        db.session.commit()
        return conn

    @classmethod
    def update_by_id(cls, _id, data, raise_if_not_found=False):
        """Updates an existing connection"""

        connection = cls.get_by_id(_id, raise_if_not_found=raise_if_not_found)
        cls._connection_instance_update(connection, data)
        db.session.commit()
        return connection

    @classmethod
    def transfer_connections(cls, old_uid, new_uid, space_id):
        """Transfer remove's user connection"""
        conn_list = ConnectionModel.query.filter_by(
            user_id=old_uid,
            space_id=space_id).all()
        for conn in conn_list:
            conn.user_id = new_uid
        db.session.commit()

    @classmethod
    def delete_by_id(cls, _id, raise_if_not_found=False):
        """Deletes a connection by id"""
        conn = cls.get_by_id(_id, raise_if_not_found)
        conn.delete()
        db.session.commit()
        return conn

    @classmethod
    def _connection_instance_update(cls, connection, data):
        """
        helper function to update an connection instance
        :param connection: an connection instance
        :param data: connection fields map
        :return:
        """
        if "id" in data:
            del data["id"]
        for k, v in data.items():
            setattr(connection, k, v)

    @classmethod
    def create(cls, data):
        """
        before create business connection. must create/get data-manager connection first
        Args:
            data:{
                    # following fields are for data-manager level connection
                    "ds_code" string
                    "account_id": string
                    "auth_type": string
                    "name": name
                    "auth_info" : string

                    # following fields are for business level connection
                    "user_id": user_id
                    "space_id": space_id
                 }
        Returns: business connection create model

        """
        user_id, space_id, ds_code = data.get('user_id'), data.get('space_id'), data.get('ds_code')
        if not all((user_id, space_id, ds_code)):
            raise ArgumentError('Argument error: user_id - %s, '
                                'space_id - %s, ds_code - %s.' % (user_id, space_id, ds_code))

        # auth info validate
        url_validation = make_dm_datasource_url('/auth/validate', ds_code=ds_code)
        post_json(url=url_validation,
                  headers=None,
                  body={"token": data.get("auth_info")},
                  raise_on_error=True)

        # create/get a data-manager level connection
        dm_conn_url = make_dm_connection_url('/')
        dm_conn_data = {
            "ds_code": ds_code,
            "account_id": data.get("account_id"),
            "name": data.get("name"),
            "auth_info": data.get("auth_info"),
            "auth_type": data.get("auth_type")
        }
        dm_conn = post_json(url=dm_conn_url, body=dm_conn_data, raise_on_error=True)

        # create a business level connection
        business_conn_data = {
            "ds_code": ds_code,
            "user_id": user_id,
            "space_id": space_id,
            "dm_connection_id": dm_conn['id'],
            "name": dm_conn['name'],
            "ds_account_id": dm_conn['account_id']
        }
        return cls.insert_or_recover(business_conn_data)

    @classmethod
    def get_fields(cls, conn_id, req_data):
        """
        get connection fields from data-manager
        Args:
            conn_id: [string] connection_id
            req_data: [dict] request body

        Returns: connection fields

        """
        conn = cls.get_by_id(conn_id, raise_if_not_found=True)
        url = make_dm_connection_url(f'{conn.dm_connection_id}/fields')
        resp = post_json(url=url,
                         headers=get_headers(),
                         body=req_data)
        if not resp:
            raise BusinessError("Get fields from data manager failed")

        def _sort_fields(fields):
            """recursively sorting the fields according to rule above"""
            if isinstance(fields, list):
                for field in fields:
                    _sort_fields(field)
            # pylint: disable=line-too-long
            elif fields.get('children'):
                fields['children'] = sorted(fields['children'],
                                            key=lambda f: (
                                                Fields.type_order[f.get('type')],
                                                Fields.number_format_order[
                                                    f.get('displayFormat', {}).get('numberFormat')],
                                                Fields.granularity_format_order[
                                                    f.get('displayFormat', {}).get('granularity')]
                                            ))
                for field in fields['children']:
                    _sort_fields(field)
            else:
                pass

        # sorting fields
        _sort_fields(resp)
        return resp

    @classmethod
    def get_calculated_fields(cls, conn_id):
        conn = cls.get_by_id(conn_id, raise_if_not_found=True)
        url = make_dm_connection_url(f'{conn.dm_connection_id}/calculated_fields')
        return get_json(url)

    @classmethod
    def get_segments(cls, conn_id, req_data):
        """
        get connection segments from data-manager
        Args:
            conn_id: [string] connection_id
            req_data: [dict] request body
            locale: [string] language in header

        Returns: connection segments

        """
        conn = cls.get_by_id(conn_id, raise_if_not_found=True)
        url = make_dm_connection_url(f'{conn.dm_connection_id}/segments')
        resp = post_json(url=url,
                         headers=get_headers(),
                         body=req_data)
        custom_list = Segment.get_by_cid(conn_id)
        data_list = [{
            "id": segment.get("id"),
            "name": segment.get("name"),
            "is_custom": True
        } for segment in custom_list]
        resp.extend(data_list)
        return resp


class Sheet:
    pass


class Table:
    """
    Database table related services.
    """

    @classmethod
    def get_all(cls, conn_id):
        """
        Gets all tables under a connection.
        """

        connection = Connection.get_by_id(conn_id)
        assert connection.dm_connection_id

        tables = TableModel.query.filter_by(connection_id=conn_id)

        # include table detail information from remote
        result = []
        for table in tables:
            try:
                full_table = cls.get_by_id(conn_id, table.id, True)
            except ApiError:
                # log downstream errors but still proceed
                logger.exception('Unable to get table info from DM')
                continue
            else:
                result.append(full_table)
        return result

    @classmethod
    def create(cls, conn_id, req_body):
        """
        Creates a table under a connection.
        """

        connection = Connection.get_by_id(conn_id, raise_if_not_found=True)
        assert connection.dm_connection_id

        table_url = make_dm_connection_url(f'{connection.dm_connection_id}/tables')

        # create downstream DM table
        dm_table = post_json(table_url, body=req_body)

        # create business layer table
        table = TableModel()
        table.connection_id = conn_id
        table.dm_table_id = dm_table['id']

        db.session.add(table)
        db.session.commit()

        dm_table['id'] = table.id
        dm_table['connection_id'] = table.connection_id
        return dm_table

    @classmethod
    def get_by_id(cls, conn_id, table_id, raise_if_not_found=False):
        """
        Gets a table by id under a connection.
        """

        connection = Connection.get_by_id(conn_id)
        assert connection.dm_connection_id

        table = TableModel.query.filter_by(id=table_id, connection_id=conn_id) \
                .first()
        if not table and raise_if_not_found:
            raise EntityNotFoundError(f'Table not found: {table_id}')

        downstream_url = f'{connection.dm_connection_id}/tables/{table.dm_table_id}'
        table_url = make_dm_connection_url(downstream_url)
        dm_table = get_json(table_url)
        dm_table['id'] = table.id
        dm_table['connection_id'] = table.connection_id
        return dm_table

    @classmethod
    def get_fields(cls, conn_id, table_id, raise_if_not_found=False):
        """
        Gets fields defined in a table.
        """

        connection = Connection.get_by_id(conn_id)
        assert connection.dm_connection_id

        table = TableModel.query.filter_by(id=table_id, connection_id=conn_id) \
                .first()
        if not table:
            if raise_if_not_found:
                raise EntityNotFoundError(f'Table not found: {table_id}')
            else:
                return []

        downstream_url = f'{connection.dm_connection_id}/tables/{table.dm_table_id}/fields'
        fields_url = make_dm_connection_url(downstream_url)
        fields = get_json(fields_url, headers=get_headers())
        return fields

    @classmethod
    def get_data(cls, conn_id, table_id, req_body, raise_if_not_found=False):
        """
        Gets data from a table.
        """

        connection = Connection.get_by_id(conn_id, raise_if_not_found=raise_if_not_found)
        assert connection.dm_connection_id

        table = TableModel.query.filter_by(id=table_id, connection_id=conn_id) \
                .first()
        if not table:
            if raise_if_not_found:
                raise EntityNotFoundError(f'Table not found: {table_id}')
            else:
                return None

        downstream_url = f'{connection.dm_connection_id}/tables/{table.dm_table_id}/data'
        data_url = make_dm_connection_url(downstream_url)
        data = post_json(data_url, body=req_body)
        return data

    @classmethod
    def update_by_id(cls, conn_id, table_id, req_body, raise_if_not_found=False):
        """
        Updates a table under a connection.
        """

        connection = Connection.get_by_id(conn_id, raise_if_not_found=raise_if_not_found)
        assert connection.dm_connection_id

        table = TableModel.query.filter_by(id=table_id, connection_id=conn_id) \
                .first()
        if not table:
            if raise_if_not_found:
                raise EntityNotFoundError(f'Table not found: {table_id}')
            else:
                return None

        downstream_path = f'{connection.dm_connection_id}/tables/{table.dm_table_id}'
        table_url = make_dm_connection_url(downstream_path)

        # update downstream DM table
        dm_table = put_json(table_url, body=req_body)

        dm_table['id'] = table.id
        dm_table['connection_id'] = table.connection_id
        return dm_table

    @classmethod
    def delete(cls, conn_id, table_id, raise_if_not_found=False):
        """
        Deletes a table under a connection.
        """

        if conn_id:
            table = TableModel.query.filter_by(id=table_id, connection_id=conn_id).first()
        else:
            # TODO: this is a special handling for deleting table without
            # parent connection information; should be fixed and removed
            # in the future
            table = TableModel.query.filter_by(id=table_id).first()

        if not table:
            if raise_if_not_found:
                raise EntityNotFoundError()
            else:
                return None

        connection = Connection.get_by_id(table.connection_id)
        assert connection.dm_connection_id

        # delete downstream DM table
        downstream_url = f'{connection.dm_connection_id}/tables/{table.dm_table_id}'
        table_url = make_dm_connection_url(downstream_url)
        dm_table = delete_json(table_url)

        table.delete()
        db.session.commit()

        dm_table['id'] = table_id
        dm_table['connection_id'] = conn_id
        return dm_table


class File:
    pass


class FileSheet:
    pass


class Segment:
    """Segment methods"""

    # non-null/empty fields when creating a segment
    required_fields = ("name", "scope", "operation", "conditions", "space_id", "user_id", "ds_code")

    @classmethod
    def insert(cls, data):
        """
        Create segment
        Args:
            data: segment vo object
        Returns: Segment
        """
        if not isinstance(data, dict) or not all([data.get(_) for _ in cls.required_fields]):
            raise ArgumentError("Insert or update segment fields invalid.")
        seg = SegmentModel(**data)
        logger.info('Creating new segment: %s', seg)
        SegmentModel.insert(seg)
        return cls._make_return_field(seg)

    @classmethod
    def update(cls, data):
        """
        Update segment
        Args:
            data: segment vo object
        Returns:
        """
        segment = SegmentModel.update_by_id(data)
        dd = cls._make_return_field(segment)
        return dd

    @classmethod
    def get_by_cid(cls, connection_id):
        segment_list = SegmentModel.query.filter_by(
            connection_id=connection_id).order_by(SegmentModel.created_at).all()
        return [cls._make_return_field(segment) for segment in segment_list]

    @classmethod
    def get_by_id(cls, segment_id):
        segment = SegmentModel.get_by_id(segment_id)
        return cls._make_return_field(segment)

    @classmethod
    def _make_return_field(cls, segment):
        conditions_str = getattr(segment, "conditions")
        if conditions_str:
            conditions_list = json.loads(conditions_str)
        return {
            "id": getattr(segment, "id"),
            "created_at": getattr(segment, "created_at"),
            "last_updated_at": getattr(segment, "last_updated_at"),
            "name": getattr(segment, "name"),
            "scope": getattr(segment, "scope"),
            "operation": getattr(segment, "operation"),
            "conditions": conditions_list,
            "space_id": getattr(segment, "space_id"),
            "user_id": getattr(segment, "user_id"),
            "ds_code": getattr(segment, "ds_code"),
            "connection_id": getattr(segment, "connection_id")
        }

    @classmethod
    def delete_by_id(cls, segment_id):
        """
        Delete segment by id
        Args:
            segment_id:  segment id
        Returns:
        """
        SegmentModel.delete_by_id(segment_id)
