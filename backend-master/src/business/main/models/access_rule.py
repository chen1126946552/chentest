"""
DataDeck Resource access rule
"""
from __future__ import absolute_import
from dataclasses import dataclass
from app import db
from models.base import BaseModel
from utils import constant
# pylint: disable=missing-docstring,no-member


ACCESS_LEVEL_DICT = {
    "read": 1,
    "read-analysis": 2,
    "edit": 3,
    "edit-share": 4
}


@dataclass(init=False, repr=True)
class AccessRule(BaseModel):
    __tablename__ = 'business_access_rule'

    """
    Data model for access rule
    """
    resource_id = db.Column(db.String(length=50), nullable=False)
    resource_type = db.Column(db.String(length=50), nullable=False)
    space_id = db.Column(db.String(length=36), nullable=False, index=True)
    user_id = db.Column(db.BIGINT, nullable=True)
    owner_id = db.Column(db.BIGINT, nullable=False)
    group_id = db.Column(db.String(length=50), nullable=True)
    access_level = db.Column(db.String(length=50), nullable=False)

    def is_share_to_all(self):
        return bool(self.group_id == constant.ALL_SPACE_USERS_GROUP_ID)

    def get_access_level_weight(self):
        return ACCESS_LEVEL_DICT.get(self.access_level, 0)
