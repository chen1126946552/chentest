"""
Dispatch rules for connection services
"""
from __future__ import absolute_import

import logging

from flask import Blueprint
from flask import current_app as app
from flask import jsonify

from common.http.utils import get_json

api = Blueprint('interim', __name__)
logger = logging.getLogger(__name__)


@api.route('/api/v1/connections/<string:cid>/exist')
def check_connection_exist(cid):
    """
    Check if the connection exists
    Args:
        cid: Connection's id
    """
    busines_url = f'{app.config["VNEXT_BUSINESS_URL"]}/api/v1/connections/{cid}'
    conn = get_json(busines_url, raise_on_error=False)
    return jsonify({"exist": bool(conn)})
