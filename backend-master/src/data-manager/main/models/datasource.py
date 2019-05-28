'''Datasource related models for storage'''

from dataclasses import dataclass
from app import db
from .base import BaseModel

# pylint: disable=no-member

@dataclass(init=False, repr=True)
class DatasourceModel(BaseModel):
    '''
    Data model for datasource.
    '''
    __tablename__ = 'data_manager_datasource'
    name = db.Column(db.String(length=50), nullable=False)
    code = db.Column(db.String(length=50), nullable=False)
    description = db.Column(db.String(length=512), nullable=True)
    api_version = db.Column(db.String(length=50), nullable=False, default='1.0')
    published = db.Column(db.Boolean(), nullable=False, default=True)
    ds_id = db.Column(db.Integer)

    # datasource type: ['api', 'db', 'file']
    type = db.Column(db.String(length=50), nullable=False, default='api')

@dataclass
class DatasourceAuthModel:
    '''
    Data model for datasource auth info.
    '''
    type: str
    form_items: list = None
    oauth_uri: str = None
    oauth_state: str = None
