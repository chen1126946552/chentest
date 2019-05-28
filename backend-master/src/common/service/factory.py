"""
Factory functions for creating Flask apps with
different settings.
"""

import json
import logging
import os
import textwrap
import time
import uuid

import yaml
from flask import Flask, g, request
from flask_cors import CORS
from elasticapm.contrib.flask import ElasticAPM
from .constants import CommonHeaders

apm = ElasticAPM()

# pylint: disable=too-many-arguments,too-many-locals,too-many-statements

def create_service_app(env,
                       config_module,
                       enable_cors=True,
                       track_time=True,
                       track_request_body=True,
                       track_response_body=True,
                       track_path_prefix='/api/'):

    """
    Creates a configured Flask app for standard Datadeck service.

    Additional config file will be loaded if "EXTRA_CONFIG" environment
    variable is provided, which specifies an additional Yaml file which
    will be used for overriding config items loaded in the standard config
    file.

    :param env: service's deploy environment
    :param config_module: module containing config classes, named Config{Env}
    :param enable_cors: if the service should be configured to allow CORS
    :param track_time: if request should be timed (and logged)
    :param track_request_body: if request body should be logged
    :param track_response_body: if response body should be logged
    :param track_path_prefix: track only url path with the given prefix
    """

    config_class_name = "Config{}".format(env.capitalize())
    config_obj = getattr(config_module, config_class_name)
    if not config_obj:
        raise ValueError((f'Config class {config_class_name} '
                          f'cannot be found in module {config_module}'))

    app = Flask(config_obj.APP_NAME)
    app.config.from_object(config_obj)

    logger = logging.getLogger(config_obj.APP_NAME)

    if 'ELASTIC_APM' in app.config:
        logger.info('Initializing elastic APM')
        apm.init_app(app)

    # override config with yaml file specified in environment variable
    extra_config_file = os.environ.get('EXTRA_CONFIG')
    if extra_config_file:
        logger.info('"EXTRA_CONFIG" env var provided, adding config from: %s', extra_config_file)
        with open(extra_config_file, 'r') as f:
            extra_config_obj = yaml.load(f)
            app.config.from_mapping(extra_config_obj)

    app.secret_key = os.urandom(24)

    if enable_cors:
        logger.warning('Enabling CORS')
        CORS(app)

    def body_str(entity):
        if entity.json:
            result = json.dumps(entity.json, ensure_ascii=False)
        elif entity.data:
            try:
                result = entity.data.decode('utf-8').replace('\n', ' ')
            except UnicodeDecodeError:
                result = str(entity.data)
        else:
            result = ''
        return textwrap.shorten(result, width=4096, placeholder='...')

    @app.before_request
    def before_request():   # pylint: disable=unused-variable
        """
        Log and start timing request. Extract or generate trace id.
        """

        if request.method not in ['GET', 'POST', 'PUT', 'DELETE']:
            return

        if track_path_prefix and not request.path.startswith(track_path_prefix):
            return

        if 'TraceId' in request.headers:
            g.trace_id = request.headers['TraceId']
        elif 'traceId' in request.args:
            g.trace_id = request.args['traceId']
        else:
            g.trace_id = str(uuid.uuid1())

        if 'UID' in request.headers:
            g.user_id = request.headers['UID']
        else:
            g.user_id = ''

        if CommonHeaders.LOCALE in request.headers:
            g.locale = request.headers[CommonHeaders.LOCALE]
        else:
            g.locale = 'en_US'

        if track_time:
            g.start = time.time()
            logger.info('Request started, %s', request.full_path)

        if track_request_body:
            logger.debug('Request body: %s', body_str(request))


    @app.after_request
    def after_request(response):    # pylint: disable=unused-variable
        """
        Time and log response.
        """

        if request.method not in ['GET', 'POST', 'PUT']:
            return response

        if track_path_prefix and not request.path.startswith(track_path_prefix):
            return response

        err = response.status_code >= 400

        if track_time:
            log_method = logger.error if err else logger.info
            log_method('Request ended, took %d ms', int((time.time() - g.start) * 1000))

        if err:
            logger.error('Response body: %s', body_str(response))
        elif track_response_body:
            logger.debug('Response body: %s', body_str(response))
        return response

    return app
