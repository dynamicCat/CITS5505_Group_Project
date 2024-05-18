from flask import Flask
from app.main import bp as main_blueprint
from app.auth import bp as auth_blueprint
from app.dashboard import bp as dashboard_blueprint 
from app.requests import bp as requests_blueprint
from app.profile import bp as profile_blueprint
from app import db
from tests.test_config import TestConfig
import sys 
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))






def create_app():
    app = Flask(__name__)
    app.config.from_object(TestConfig)
    db.init_app(app)
    app.register_blueprint(main_blueprint, url_prefix='/main')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
    app.register_blueprint(requests_blueprint, url_prefix='/requests')
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    return app