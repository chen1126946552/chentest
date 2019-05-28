""" flask app config for pytest"""
import logging
import os
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)

db_file = NamedTemporaryFile(delete=False, suffix='.db')
db_file.close()
logger.info('Using database file: %s', db_file.name)


class ConfigTest:
    """ app config for pytest"""
    TESTING = True
    APP_NAME = 'data-manager'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:////{db_file.name}' \
        if os.name != 'nt' else f'sqlite:///{db_file.name}'
    LOGGING_LEVEL = logging.DEBUG
    DATASOURCE_HOSTNAME_PREFIX = 'datadeck-datasource-'
    DATASOURCE_SERVICE_PORT = 9090
    AUTH_CALLBACK_URL = 'https://datadeck-api-gateway:9080/api/v4/datasources/{}/authCallback'
    CACHE_TYPE = 'simple'
