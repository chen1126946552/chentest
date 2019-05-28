"""Local conftest.py plugins contain directory-specific hook implementations."""
import os
import sys
import pytest
import test_config

sys.path.append(os.path.join(os.path.dirname(__file__), '../main'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from app import create_app

from utils.system_constant import clear_all_cache


@pytest.fixture(scope='session')
def test_client():
    """test client"""
    flask_app = create_app('test', app_config_module=test_config, logging_config_file=None)
    app_test_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield app_test_client


@pytest.fixture(autouse=True)
def test_setup():
    # Clear cache to make sure test cases don't interfere
    clear_all_cache()
