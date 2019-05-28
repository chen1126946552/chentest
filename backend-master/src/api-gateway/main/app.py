'''Flask app factory'''

import logging
import traceback
from http import HTTPStatus
from flask import jsonify
import config
from common.http.executor import Executor
from common.http.utils import ApiError
from common.log import setup_logging
from common.log.helper import log_exception
from common.service import create_service_app
from services.exception import ServiceError


logger = logging.getLogger(__name__)
executor = Executor()


def create_app(env,
               app_config_module=config,
               logging_config_file='./logging.yml'):
    '''
    Creates a configured Flask app
    '''

    app = create_service_app(env, app_config_module)
    executor.init_app(app)
    if logging_config_file:
        setup_logging(app, logging_config_file)

    _register_routes(app)
    return app


def _register_routes(app):
    from blueprints.health import api as health
    app.register_blueprint(health)

    from blueprints.legacy import api as legacy
    app.register_blueprint(legacy)

    from blueprints.oauth import api as oauth
    app.register_blueprint(oauth)

    from blueprints.widget import api as widget
    app.register_blueprint(widget)

    from blueprints.share import api as share
    app.register_blueprint(share)

    from blueprints.etl import api as etl
    app.register_blueprint(etl)

    from blueprints.form_auth import api as form_auth
    app.register_blueprint(form_auth)

    from blueprints.database_table import api as database_table
    app.register_blueprint(database_table)

    from blueprints.interim import api as interim
    app.register_blueprint(interim)

    from blueprints.catch_all import api as catch_all
    app.register_blueprint(catch_all)

    @app.errorhandler(ServiceError)
    def service_error_handler(err): # pylint: disable=unused-variable
        """
        Map generic service error to proper error response.
        """
        logger.error('Service error: %s', err)
        return jsonify({
            'success': False,
            'errorCode': err.error_code,
            'data':{
                'errorMsg': err.message,
                'status' : 'failed'
            }
        }), HTTPStatus.OK


    @app.errorhandler(ApiError)
    def api_error_handler(err): # pylint: disable=unused-variable
        """
        Map downstream API call error to proper error response.
        For business error like get data fail, FrontEnd now requires
        to return HTTP 200 message with data.status == failed, then
        it will show the data.errorMsg to user.
        """
        logger.error('Downstream API call error: %s', err)
        return jsonify({
            'success': False,
            'errorCode': err.error_code,
            'debugMessage': err.debug_message,
            'data':{
                'errorMsg': err.message,
                'status' : 'failed'
            }
        }), HTTPStatus.OK


    @app.errorhandler(Exception)
    def generic_err_handler(err): # pylint: disable=unused-variable
        """
        Map generic unhandled error to proper error response.
        """
        log_exception(logger, err)
        stack = traceback.format_exception(err.__class__, err, err.__traceback__)
        return jsonify({
            'success': False,
            'debugMessage': str(err) + ''.join(stack),
            'data':{
                'errorMsg': 'Request failed, try again later',
                'status' : 'failed'
            }
        }), HTTPStatus.OK
