"""Base model"""
from uuid import uuid1
import time
from app import db
from common.model.query_with_soft_delete import QueryWithSoftDelete


# pylint: disable=missing-docstring,no-member


class BaseModel(db.Model):
    """Base model"""
    __abstract__ = True
    query_class = QueryWithSoftDelete

    id = db.Column(db.String(length=36), default=lambda _: str(uuid1()), primary_key=True)
    created_at = db.Column(db.BigInteger, default=lambda: time.time() * 1000)
    last_updated_at = db.Column(db.BigInteger, default=lambda: time.time() * 1000,
                                onupdate=lambda: time.time() * 1000)
    is_deleted = db.Column(db.Boolean, default=False)

    def _as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def delete(self):
        self.is_deleted = True
        db.session.commit()

    @classmethod
    def insert(cls, data):
        db.session.add(data)
        db.session.commit()
        return data

    @classmethod
    def update_by_id(cls, data):
        data_result = cls.query.filter_by(id=data.get("id")).first()
        if data_result:
            for k, v in data.items():
                setattr(data_result, k, v)
        db.session.commit()
        return data_result

    @classmethod
    def get_by_id(cls, _id, with_deleted=False):
        data_result = cls.query.filter_by(id=_id).first() \
            if not with_deleted else cls.query.with_deleted().filter_by(id=_id).first()
        return data_result

    @classmethod
    def delete_by_id(cls, _id):
        data_result = cls.query.filter_by(id=_id).first()
        if data_result:
            data_result.delete()
        return data_result
