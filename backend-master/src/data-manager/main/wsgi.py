'''Service entry point'''

import os
import logging

from app import create_app


env = os.environ.get('ENV', 'Local').lower()
app = create_app(env)
logger = logging.getLogger(__name__)

logger.info('App starting with %s configuration:', env)
for k, v in app.config.items():
    logger.info('\t%s=%s', k, v)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(app.config['PORT']), debug=False)
else:
    logger.info('Starting in container')
