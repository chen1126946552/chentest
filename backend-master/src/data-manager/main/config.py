'''App configuration classes'''

import logging

# pylint: disable=missing-docstring,line-too-long


class Config:
    PORT = 9082
    APP_NAME = 'data-manager'
    LOGGING_LEVEL = logging.INFO
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATASOURCE_HOSTNAME_PREFIX = 'datadeck-datasource-'
    DATASOURCE_SERVICE_PORT = 9090
    CACHE_TYPE = 'flask_cache_redis_cluster.rediscluster'
    CACHE_KEY_PREFIX = APP_NAME


class ConfigProduct(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://datadeck_v2:Q0dO4D@jpddcommdb.datadeck.com:13307/datadeck_vnext'
    AUTH_CALLBACK_URL = 'https://gateway.datadeck.com/api/v4/business/oauth/callback/{}'
    CACHE_KEY_PREFIX = f'prod:{Config.CACHE_KEY_PREFIX}'
    CACHE_REDIS_HOST = 'redis1.datadeck.com'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = 'Ptminddatadeck2018!'

    ELASTIC_APM = {
        'SERVICE_NAME': 'datadeck-' + Config.APP_NAME,
        'ENVIRONMENT': 'prod'
    }


class ConfigDogfood(Config):
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = 'mysql://datadeck_v2:Q0dO4D@ddstagingdb.datadeck.com/datadeck_vnext'
    AUTH_CALLBACK_URL = 'https://dogfoodgateway.datadeck.com/api/v4/business/oauth/callback/{}'
    CACHE_KEY_PREFIX = f'dogfood:{Config.CACHE_KEY_PREFIX}'
    CACHE_REDIS_HOST = 'dogfood.redis1.datadeck.com'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = 'ptmind'


class ConfigStaging(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://datadeck_v2:Q0dO4D@ddstagingdb.datadeck.com/datadeck_vnext_staging'
    AUTH_CALLBACK_URL = 'https://staginggateway.datadeck.com/api/v4/business/oauth/callback/{}'
    CACHE_KEY_PREFIX = f'staging:{Config.CACHE_KEY_PREFIX}'
    CACHE_REDIS_HOST = 'redis1.datadeck.com'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = 'ptmind'


class ConfigLocal(Config):
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = 'mysql://datadeck:datadeck@mysql.local/datadeck_vnext'
    AUTH_CALLBACK_URL = 'https://datadeck-api-gateway.datadeck.com:9080/api/v4/business/oauth/callback/{}'
    CACHE_TYPE = 'simple'
    CACHE_KEY_PREFIX = f'local:{Config.CACHE_KEY_PREFIX}'
