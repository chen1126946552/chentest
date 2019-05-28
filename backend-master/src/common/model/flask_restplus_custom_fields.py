"""Custom Fields for flask restplus"""
from flask_restplus import fields
import datetime


class Timestamp(fields.Raw):
    """
    convert datetime to timestamp
    """
    def format(self, value):
        if not isinstance(value, datetime.datetime):
            return super().format(value)
        return int(value.timestamp() * 1000)
