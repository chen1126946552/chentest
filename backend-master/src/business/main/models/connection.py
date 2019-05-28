"""
Connection related models
"""
from __future__ import absolute_import
import json
from dataclasses import dataclass
from app import db
from models.base import BaseModel
# pylint: disable=missing-docstring,no-member


@dataclass(init=False, repr=True)
class Connection(BaseModel):
    __tablename__ = 'business_connection'

    """
    Data model for connection.
    """
    user_id = db.Column(db.BIGINT, nullable=False)
    space_id = db.Column(db.String(length=36), nullable=False)
    ds_code = db.Column(db.String(length=24), nullable=True)
    ds_account_id = db.Column(db.String(length=50), nullable=False)
    dm_connection_id = db.Column(db.String(length=36), nullable=False)
    name = db.Column(db.String(length=50), nullable=True)

    sheets = db.relationship('Sheet', backref='sheet', lazy='dynamic')
    tables = db.relationship('Table', backref='table', lazy='dynamic')
    files = db.relationship('File', backref='file', lazy='dynamic')
    segment = db.relationship('Segment', backref='segment', lazy='dynamic')

    __table_args__ = (db.Index('user_space_index', "user_id", "space_id"),)


@dataclass(init=False, repr=True)
class ConnectionCalFieldModel(BaseModel):
    """Data model for calculated field."""
    __tablename__ = 'business_calculated_field'

    # custom calculated field related
    connection = db.Column(db.String(length=50), db.ForeignKey('business_connection.id'),
                           nullable=False)
    space_id = db.Column(db.String(length=36), nullable=False)

    name = db.Column(db.String(length=120), nullable=False)
    display = db.Column(db.String(length=120), default=name)
    expression = db.Column(db.Text, nullable=False)
    candidates = db.Column(db.Text, nullable=False)
    function_contain = db.Column(db.Boolean(), default=False)
    group_function_contain = db.Column(db.Boolean(), default=False)

    # base field related
    data_type = db.Column('type', db.String(length=50), nullable=True)
    allow_filter = db.Column(db.Boolean(), default=False)
    filter_ops = db.Column(db.Text, nullable=True)
    allow_aggregation = db.Column(db.Boolean(), default=False)
    aggregation_ops = db.Column(db.Text, nullable=True)

    @property
    def filter_options(self):
        """filter options flat string to json"""
        if not self.allow_filter:
            return []
        return json.loads(self.filter_ops) if self.filter_ops else []

    @property
    def aggr_options(self):
        """aggregation options flat string to json"""
        if not self.allow_aggregation:
            return []
        return json.loads(self.aggregation_ops) if self.aggregation_ops else []

    @property
    def fields(self):
        """candidates(fields set) options flat string to json"""
        if not self.candidates:
            return []
        return json.loads(self.candidates) if self.candidates else []

    @property
    def keys(self):
        """field ids set"""
        return [f['id'] for f in self.fields]


@dataclass(init=False, repr=True)
class Sheet(BaseModel):
    __tablename__ = 'business_connection_sheet'

    """
    Data model for Sheet.
    """
    connection_id = db.Column(db.String(length=36), db.ForeignKey('business_connection.id'))


@dataclass(init=False, repr=True)
class Table(BaseModel):
    __tablename__ = 'business_connection_table'

    """
    Data model for Table.
    """
    connection_id = db.Column(db.String(length=36), db.ForeignKey('business_connection.id'))
    dm_table_id = db.Column(db.String(length=36), nullable=False)


@dataclass(init=False, repr=True)
class File(BaseModel):
    __tablename__ = 'business_connection_file'

    """
    Data model for File.
    """
    connection_id = db.Column(db.String(length=36), db.ForeignKey('business_connection.id'))
    filesheets = db.relationship('Filesheet', backref='filesheet', lazy='dynamic')


@dataclass(init=False, repr=True)
class Filesheet(BaseModel):
    __tablename__ = 'business_connection_filesheet'

    """
    Data model for Filesheet.
    """
    file_id = db.Column(db.String(length=36), db.ForeignKey('business_connection_file.id'))


@dataclass(init=False, repr=True)
class Segment(BaseModel):
    __tablename__ = 'business_segment'

    name = db.Column(db.String(length=255), nullable=False)
    scope = db.Column(db.String(length=255), nullable=True)
    operation = db.Column(db.String(length=255), nullable=True)
    conditions = db.Column(db.Text)
    space_id = db.Column(db.String(length=255), nullable=False)
    user_id = db.Column(db.BIGINT, nullable=False)
    ds_code = db.Column(db.String(length=50), nullable=False)
    modifier_id = db.Column(db.BIGINT, nullable=True)
    connection_id = db.Column(db.String(length=36), db.ForeignKey('business_connection.id'))
