from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models and routes
from .models import User, Request, Response, accepted_requests
from .routes import *

if __name__ == '__main__':
    app.run()

