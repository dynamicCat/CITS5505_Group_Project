from app import create_app as create_flask_app
from tests.test_config import TestConfig
def create_app():
    return create_flask_app(TestConfig)