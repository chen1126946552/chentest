"""Local conftest.py plugins contain directory-specific hook implementations."""
import os
import sys
import pytest
import test_config

sys.path.append(os.path.join(os.path.dirname(__file__), '../main'))
from app import create_app, db


@pytest.fixture(scope='session')
def test_client():
    """
    Returns: a test client, clear work would be done when client finished
    """
    flask_app = create_app('test',
                           app_config_module=test_config,
                           logging_config_file=None)
    app_test_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    db.create_all()
    yield app_test_client
    db.drop_all()
    ctx.pop()
