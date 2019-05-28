'''
Factory methods for creating standard Flask
responses.
'''

from flask import jsonify


def make_error_response(message, code):
    '''
    Makes an error response with an error message and Http status code.
    '''
    return jsonify({'message': message}), code
