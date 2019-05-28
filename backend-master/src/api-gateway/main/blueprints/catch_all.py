"""
Catch call route to forward requests to middle by default.
"""

import logging

from flask import Blueprint
from flask import current_app as app
from flask import request

from common.http.proxy import proxy

api = Blueprint('catch_all', __name__)
logger = logging.getLogger(__name__)

METHODS = ['GET', 'POST', 'PUT', 'DELETE']

@api.route('/', defaults={'path': ''}, methods=METHODS)
@api.route('/<path:path>', methods=METHODS)
def catch_all(path):
    """
    Catch all based on: http://flask.pocoo.org/snippets/57/
    """
    logger.info('Catch all dispatching to MIDDLE: /%s', path)
    return proxy(request, f'{app.config["MIDDLE_URL"]}/{path}')
