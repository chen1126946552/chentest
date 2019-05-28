'''Flask app factory'''

import logging
from http import HTTPStatus

from flask import Blueprint
from flask_migrate import Migrate, upgrade
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from requests import Session

import config
from common.http.utils import ApiError, init_session
from common.log import log_exception, setup_logging
from common.service import create_service_app
from common.service.cache import SimpleCache
from endpoints.schemas import init_models
from services.exceptions import EntityNotFoundError, ServiceError

db = SQLAlchemy()
cache = SimpleCache()
api = Api(version='0.9', title='Datadeck Datasource Provider API', validate=True)
logger = logging.getLogger(__name__)


def create_app(env,
               app_config_module=config,
               logging_config_file='./logging.yml'):
    '''Creates the Flask app'''

    app = create_service_app(env=env, config_module=app_config_module)

    # use less strict trailing slashes for route matching
    app.url_map.strict_slashes = False

    # register routes
    _register_routes(app)

    # initialize DB and migrate
    db.init_app(app)
    Migrate(app, db, version_table='alembic_version_data_manager', compare_type=True)
    # initialize cache
    cache.init_app(app)

    if not app.testing:
        # Upgrade database schema
        with app.app_context():
            upgrade()
    init_session(Session())

    if logging_config_file:
        setup_logging(app, logging_config_file)
    return app


def _register_routes(app):
    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    init_models(api)

    # pylint: disable=unused-import
    import endpoints.health
    import endpoints.datasources
    import endpoints.connections
    import endpoints.common

    app.register_blueprint(blueprint)

    @api.errorhandler(ApiError)
    def api_error_handler(err):  # pylint: disable=unused-variable
        log_exception(logger, err)
        return {'error_code': err.error_code, 'message': err.message,
                'debug_message': err.debug_message},\
                err.status_code or HTTPStatus.BAD_REQUEST

    @api.errorhandler(EntityNotFoundError)
    def entity_not_found_error_handler(err): # pylint: disable=unused-variable
        log_exception(logger, err)
        return {'error_code': 'ENTITY_NOT_FOUND', 'message': str(err)}, \
               HTTPStatus.NOT_FOUND

    @api.errorhandler(ServiceError)
    def service_error_handler(err): # pylint: disable=unused-variable
        log_exception(logger, err)
        return {'error_code': 'GENERIC_ERROR', 'message': f'Service error: {err}'}, \
               HTTPStatus.BAD_REQUEST

    @api.errorhandler(Exception)
    def generic_err_handler(ex):  # pylint: disable=unused-variable,unused-argument
        log_exception(logger, ex)
        msg = f'An unexpected error occurred: {ex}'
        return {'error_code': 'GENERIC_ERROR', 'message': msg},\
                HTTPStatus.INTERNAL_SERVER_ERROR
