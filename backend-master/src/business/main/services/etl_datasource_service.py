"""Etl datasource service"""
from __future__ import absolute_import

import json
import logging

from flask import current_app as app

from exception import EntityNotFoundError
from models.etl_datasource import EtlDatasource as EtlDatasourceModel
from common.http.utils import post_json, get_headers

# pylint: disable=no-member

logger = logging.getLogger(__name__)


def insert_or_update(data):
    """Save or update etl datasource"""
    es_id = data.get("id")
    if es_id:
        EtlDatasourceModel.update_by_id(data)
    else:
        del data["id"]
        etl_dm = EtlDatasourceModel.insert(EtlDatasourceModel(**data))
        es_id = etl_dm.id
    _notification_dataset_sync_data(es_id)
    return {"id": es_id}


def get_by_datasource_id(datasource_id, raise_if_not_found=False):
    """Get datasource config by id"""
    etl_dsm = EtlDatasourceModel.get_by_id(datasource_id)
    if raise_if_not_found and not etl_dsm:
        raise EntityNotFoundError(f'ETL datasource not found: {datasource_id}')
    if etl_dsm:
        return _make_return_field(etl_dsm)
    return None


def _notification_dataset_sync_data(etl_datasource_id):
    url = f'{app.config["DS_GATEWAY_URL"]}/dataset-service/etl/syncTableInfo/{etl_datasource_id}'
    post_json(url, get_headers())


def _make_return_field(etl_dsm):
    return {
        "id": etl_dsm.id,
        "name": etl_dsm.name,
        "language": etl_dsm.language,
        "timezone": etl_dsm.timezone,
        "fields": json.loads(etl_dsm.fields) if etl_dsm.fields else None,
        "time": json.loads(etl_dsm.time) if etl_dsm.time else None,
        "filters": json.loads(etl_dsm.filters) if etl_dsm.filters else None,
        "segment": json.loads(etl_dsm.segment) if etl_dsm.segment else None,
        "sort": json.loads(etl_dsm.sort) if etl_dsm.sort else None,
        "widget_connection_config_id": etl_dsm.widget_connection_config_id,
        "space_id": etl_dsm.space_id
    }
