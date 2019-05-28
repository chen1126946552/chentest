'''Logging setup'''

from logging.config import dictConfig
import logging
import yaml


def setup_logging(app, config_file):
    '''
    Setup logging for an app based on a YAML
    configuration file.

    Services can use root logger or per-module
    logger to log. DO NOT use Flask app's builtin
    logger.
    '''

    with open(config_file, 'r') as f:
        cfg = yaml.load(f)
        dictConfig(cfg)
    logging.getLogger('werkzeug').disabled = True
    app.logger.disabled = True
