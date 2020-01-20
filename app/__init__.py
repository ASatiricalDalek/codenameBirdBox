from flask import Flask
from config import configObject
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
# Load our configuration from the config.py file
app.config.from_object(configObject)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
