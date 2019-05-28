import logging
import os
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)

db_file = NamedTemporaryFile(delete=False, suffix='.db')
db_file.close()
logger.info('Using database file: %s', db_file.name)


class ConfigTest:
    TESTING = True
    APP_NAME = 'business'
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:////{db_file.name}' if os.name != 'nt' else f'sqlite:///{db_file.name}'
    DATA_MANAGER_URL = 'http://datadeck-data-manager:9082/api/v1'
    REDIS_SOCKET_TIMEOUT = 5
    AUTH_CALLBACK_URL = 'https://datadeck-api-gateway:9080/api/v4/business/oauth/callback/{ds_code}'
    REDIS_URL = "redis://:ptmind@redis.datadeck.com:6379/0"
    V2_MIDDLE_URL = 'http://local.middle.com:7090'
    DS_GATEWAY_URL = 'http://dsgateway.datadeck.com:8020'
