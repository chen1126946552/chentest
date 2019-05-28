'''Health check endpoints'''

from http import HTTPStatus

from flask import Blueprint, jsonify


api = Blueprint('health', __name__)


@api.route('/health')
def health():
    '''Health check'''
    return jsonify({'status': 'good'}), HTTPStatus.OK
