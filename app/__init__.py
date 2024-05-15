from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.auth import bp as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.dashboard import bp as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

    from app.requests import bp as requests_blueprint
    app.register_blueprint(requests_blueprint, url_prefix='/requests')

    from app.profile import bp as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/profile')

    from .main import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app



