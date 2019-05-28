'''Connection related models for storage'''

from __future__ import absolute_import

import json
from dataclasses import dataclass

from app import db

from .base import BaseModel


# pylint: disable=no-member


@dataclass(init=False, repr=True)
class ConnectionModel(BaseModel):
    '''
    Data model for connection.
    '''
    __tablename__ = 'data_manager_connection'
    name = db.Column(db.String(length=50), nullable=False)
    ds_code = db.Column(db.String(length=50), nullable=False)
    auth_type = db.Column(db.String(length=50), nullable=False)
    auth_info = db.Column(db.Text, nullable=True)
    account_id = db.Column(db.String(length=50), nullable=False)


@dataclass(init=False, repr=True)
class ConnectionTableModel(BaseModel):
    """
    Data model for database table
    """
    __tablename__ = 'data_manager_table'
    connection_id = db.Column(db.String(length=50),
                              db.ForeignKey('data_manager_connection.id'), nullable=False)
    name = db.Column(db.String(length=50), nullable=False)
    database = db.Column(db.String(length=512), nullable=False)
    columns = db.Column(db.Text, nullable=False)

    @property
    def columns_populated(self):
        """
        Columns are stored in DB as flat string. This property returns
        the deserialized json.
        """
        return json.loads(self.columns) if self.columns else None
