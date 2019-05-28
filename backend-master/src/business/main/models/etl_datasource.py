"""
DataDeck etl data source model
"""
from __future__ import absolute_import
from uuid import uuid1
from dataclasses import dataclass
from app import db
from models.base import BaseModel

# pylint: disable=missing-docstring,no-member

ID_PREFIX = 'datasource_'


def build_uuid():
    etl_ds_id = ID_PREFIX + str(uuid1())
    return etl_ds_id.replace("-", "_")


@dataclass(init=False, repr=True)
class EtlDatasource(BaseModel):
    __tablename__ = 'business_etl_datasource'

    """
    Data model for etl datasource
    """
    id = db.Column(db.String(length=47), default=lambda _: build_uuid(), primary_key=True)
    name = db.Column(db.String(length=255), nullable=False)
    fields = db.Column(db.Text)
    time = db.Column(db.Text)
    filters = db.Column(db.Text)
    segment = db.Column(db.Text)
    sort = db.Column(db.Text)
    status = db.Column(db.Integer, default=0)
    space_id = db.Column(db.String(length=36), nullable=False, index=True)
    widget_connection_config_id = db.Column(db.String(length=50), nullable=False, index=True)
    language = db.Column(db.String(length=50), nullable=True)
    timezone = db.Column(db.String(length=50), nullable=True)
