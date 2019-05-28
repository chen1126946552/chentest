'''Configurations'''

import logging

# pylint: disable=missing-docstring


class Config:
    PORT = 9080
    APP_NAME = 'api-gateway'
    LOGGING_LEVEL = logging.INFO
    VNEXT_BUSINESS_URL = 'http://datadeck-business:9081'
    VNEXT_DATA_MANAER_URL = 'http://datadeck-data-manager:9082'
    EXECUTOR_PROPAGATE_EXCEPTIONS = True

class ConfigProduct(Config):
    MIDDLE_URL = 'http://middle.datadeck.com:8080'
    AUTH_V2_URL = 'https://authv2.datadeck.com'
    DS_GATEWAY_URL = 'http://dsgateway.datadeck.com:9020'

    ELASTIC_APM = {
        'SERVICE_NAME': 'datadeck-' + Config.APP_NAME,
        'ENVIRONMENT': 'prod'
    }


class ConfigDogfood(Config):
    LOGGING_LEVEL = logging.DEBUG
    MIDDLE_URL = 'https://dogfoodmiddle.datadeck.com'
    AUTH_V2_URL = 'https://testauth.ptone.jp'
    DS_GATEWAY_URL = 'https://gatewaydogfood.datadeck.com'


class ConfigStaging(Config):
    MIDDLE_URL = 'http://middle.datadeck.com:8080'
    AUTH_V2_URL = 'https://stagingauth.datadeck.com'
    DS_GATEWAY_URL = 'http://dsgateway.datadeck.com:9020'


class ConfigLocal(Config):
    MIDDLE_URL = 'https://middlev2.datadeck.com'
    AUTH_V2_URL = 'https://authv2.datadeck.com'
    DS_GATEWAY_URL = 'https://dsgateway.datadeck.com'
