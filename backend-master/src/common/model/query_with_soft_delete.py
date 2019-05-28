'''Soft Delete Query'''

from flask_sqlalchemy import BaseQuery

# pylint: disable=protected-access
class QueryWithSoftDelete(BaseQuery):
    '''
    This class is used to provide default soft delete query for Flask-SQLAlchemy.

    TO use it, the model should look like:
            class User(db.Model):
            ...
            is_deleted = db.Column(db.Boolean(), default=False)
            ...

            query_class = QueryWithSoftDelete

    When delete row, you should set is_deleted to False instead of really delete it:
            user.deleted = True
            db.session.commit()

    If you want to get deleted rows, you can achieve it by below:
            
            User.query.with_deleted().filter(...)

    '''
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if args:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(is_deleted=False) if not obj._with_deleted else obj
        return obj

    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(self._mapper_zero().class_,
                              session=self.session, _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, ident):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(self, ident)
        return obj if obj is None or self._with_deleted or not obj.is_deleted else None
