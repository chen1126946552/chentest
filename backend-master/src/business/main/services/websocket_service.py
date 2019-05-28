"""
Push message to frontend
"""
from flask import current_app as app
from common.http.utils import post_json

# pylint: disable=missing-docstring


def ws_push_json(socked_id, json_data):
    """
    Push data based on socketId
    :param socked_id: connection socket id
    :param json_data: Send character data
    :return: Boolean
    """
    v2_websocket_url = f'{app.config["V2_MIDDLE_URL"]}/api/v1/public/websocket/push/{socked_id}'
    return post_json(v2_websocket_url, body=json_data)
