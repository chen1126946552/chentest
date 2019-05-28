"""some helper decorators"""

from functools import wraps
from flask import request
from exception import RequestHeaderError, ArgumentError

# pylint: disable=missing-docstring


def header_check(not_empty_fields, custom_fields=None):
    """
    A decorator for checking the front-end request headers
    :param not_empty_fields: positional args, non-null/empty fields in headers
    :param custom_fields: key-value args, custom checking fields, key is field,
    value is checking method with boolean return value
    :return: raising exception if checking failed
    """
    if not custom_fields:
        custom_fields = {}

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            headers = request.headers
            if not all([headers.get(_) for _ in not_empty_fields]):
                raise RequestHeaderError("Request header params invalid.")
            try:
                if not all([v(headers.get(k)) for k, v in custom_fields.items()]):
                    raise RequestHeaderError("Request header params invalid.")
            except TypeError:
                raise ArgumentError("Your argument is not ok.")
            return func(*args, **kwargs)
        return wrapper
    return decorate
