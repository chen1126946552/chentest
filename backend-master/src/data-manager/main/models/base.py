'''SQL Base Model'''
import time
import uuid
from app import db
from common.model.query_with_soft_delete import QueryWithSoftDelete

# pylint: disable=no-member
class BaseModel(db.Model):
    '''SQL Base Model'''
    __abstract__ = True
    query_class = QueryWithSoftDelete
    id = db.Column(db.String(length=36), default=lambda _: str(uuid.uuid1()), primary_key=True)
    created_at = db.Column(db.BigInteger, nullable=False, default=lambda: time.time() * 1000)
    last_updated_at = db.Column(db.BigInteger, nullable=False, default=lambda: time.time() * 1000,
                                onupdate=lambda: time.time() * 1000)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)

    def delete(self):
        self.is_deleted = True
        db.session.commit()
