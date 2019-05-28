"""HTTP request utilities"""

import logging
import json
import threading
from http import HTTPStatus
from requests import Session, RequestException
from flask import g
from .executor import request_proxy as request


logger = logging.getLogger(__name__)

thread_local = threading.local()

class ApiError(Exception):
    """API invocation error"""

    def __init__(self, status_code, error_code, message, debug_message=None):
        """
        Creates a new instance.

        Args:
            status_code (int): HTTP Status Code.
            error_code (str): Error code.
            message (str): Error message.
        """

        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.debug_message = debug_message

    def __repr__(self):
        return f'HTTP {self.status_code}, error_code: {self.error_code}, message: {self.message}'

    def __str__(self):
        return str(self.message)

#TODO: configure default max_retries and timeout
def init_session(_session):
    """Initializes the global requests.Session object used for making Http calls"""
    thread_local.session = _session

def get_session():
    """Get thread local session"""
    if not getattr(thread_local, "session", None):
        thread_local.session = Session()
    return thread_local.session

def get_headers():
    """Get flask thread(thread, process, or coroutine depending on wsgi server) request headers"""
    excluded_headers = [
        'content-encoding',
        'content-length',
        'content-type',
        'transfer-encoding',
        'connection',
        'host'
    ]
    try:
        headers = {name: value for name, value in
                   request.headers.items() if name.lower() not in excluded_headers}
        return headers
    except RuntimeError:
        # running without a flask request context
        return []


def get_json(url, headers=None, raise_on_error=True):
    """HTTP GET a URL for a JSON document"""
    return request_json('GET', url, headers, raise_on_error=raise_on_error)


def post_json(url, headers=None, body=None, raise_on_error=True):
    """HTTP POST to a URL for a JSON document"""
    return request_json('POST', url, headers, body, raise_on_error=raise_on_error)


def put_json(url, headers=None, body=None, raise_on_error=True):
    """HTTP PUT to a URL for a JSON document"""
    return request_json('PUT', url, headers, body, raise_on_error=raise_on_error)


def delete_json(url, headers=None, body=None, raise_on_error=True):
    """HTTP DELETE to a URL for a JSON document"""
    return request_json('DELETE', url, headers, body, raise_on_error=raise_on_error)


def get_header_with_uid(headers):
    """Add user id to header"""
    if not request:
        # In the test environment, the request object state is unbound.
        return None
    user_id = request.headers.get("UID")
    if not user_id:
        user_id = g.user_id if 'user_id' in g else ''

    if not headers:
        headers = {"UID": user_id}
    elif "UID" not in headers.keys() and user_id:
        headers['UID'] = user_id
    return headers


def request_json(method, url, headers=None, body=None, raise_on_error=True):
    """Sends an HTTP request and gets back a JSON document"""

    try:
        headers = get_header_with_uid(headers)
        resp = get_session().request(method, url, headers=headers, json=body)
        if resp.status_code >= 300:
            j = None
            try:
                j = resp.json()
            except (RequestException, json.JSONDecodeError) as ex:
                pass
            logger.warning('Http request error: url=%s, status=%s, body=%s',
                           url, resp.status_code, j)
            if raise_on_error:
                if j:
                    raise ApiError(resp.status_code, j.get('error_code'),
                                   j.get('message'), j.get('debug_message'))
                else:
                    raise ApiError(resp.status_code, None, 'Api invocation error')
            return None
        elif resp.status_code == HTTPStatus.NO_CONTENT:
            return None

        return resp.json()
    except RequestException as ex:
        logger.warning('Http request error: url=%s, exception=%s', url, ex)
        if raise_on_error:
            raise ApiError(None, None, 'Api invocation error')
        return None
