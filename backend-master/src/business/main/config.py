'''App configuration classes'''

import logging

# pylint: disable=missing-docstring,line-too-long


class Config:
    PORT = 9081
    APP_NAME = 'business'
    LOGGING_LEVEL = logging.INFO
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_MANAGER_URL = 'http://datadeck-data-manager:9082/api/v1'
    CACHE_TYPE = 'flask_cache_redis_cluster.rediscluster'
    CACHE_KEY_PREFIX = APP_NAME


class ConfigProduct(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://datadeck_v2:Q0dO4D@jpddcommdb.datadeck.com:13307/datadeck_vnext'
    AUTH_CALLBACK_URL = 'http://gateway.datadeck.com/api/v4/business/oauth/callback/{ds_code}'
    V2_MIDDLE_URL = 'http://middle.datadeck.com:8080'
    DS_GATEWAY_URL = 'http://dsgateway.datadeck.com:9020'
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
    AUTH_CALLBACK_URL = 'https://datadeck-api-gateway.datadeck.com:9080/api/v4/business/oauth/callback/{ds_code}'
    V2_MIDDLE_URL = 'https://dogfoodmiddle.datadeck.com'
    DS_GATEWAY_URL = 'https://gatewaydogfood.datadeck.com'
    CACHE_KEY_PREFIX = f'dogfood:{Config.CACHE_KEY_PREFIX}'
    CACHE_REDIS_HOST = 'dogfood.redis1.datadeck.com'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = 'ptmind'


class ConfigStaging(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://datadeck_v2:Q0dO4D@ddstagingdb.datadeck.com/datadeck_vnext_staging'
    AUTH_CALLBACK_URL = 'https://staginggateway.datadeck.com/api/v4/business/oauth/callback/{ds_code}'
    V2_MIDDLE_URL = 'http://middle.datadeck.com:8080'
    DS_GATEWAY_URL = 'http://dsgateway.datadeck.com:9020'
    CACHE_KEY_PREFIX = f'staging:{Config.CACHE_KEY_PREFIX}'
    CACHE_REDIS_HOST = 'redis1.datadeck.com'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = 'ptmind'


class ConfigLocal(Config):
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = 'mysql://datadeck:datadeck@mysql.local/datadeck_vnext'
    AUTH_CALLBACK_URL = 'https://datadeck-api-gateway:9080/api/v4/business/oauth/callback/{ds_code}'
    V2_MIDDLE_URL = 'https://dogfoodmiddle.datadeck.com'
    SQLALCHEMY_ECHO = True
    CACHE_TYPE = 'simple'
    CACHE_KEY_PREFIX = f'local:{Config.CACHE_KEY_PREFIX}'
    DS_GATEWAY_URL = 'http://dsgateway.datadeck.com:8020'
