from flask import Flask
from config import configObject
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
# Load our configuration from the config.py file for CSRF form security
app.config.from_object(configObject)
# Connect SQLAlchehmy to Database
db = SQLAlchemy(app)
# Connect DB migration tool to DB and SQLAlchemy
migrate = Migrate(app, db)
# Create instance of Flask_Login login manager
loginManager = LoginManager(app)
# Allow for "Login Required Decorator
loginManager.login_view = 'login'
from app import routes, models, schedule_pi

        
schedule_pi.schedule_feed()  # Scheduled feed thread initalization


    







