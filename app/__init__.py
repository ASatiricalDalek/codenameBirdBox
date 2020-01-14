from flask import Flask
from config import configObject
app = Flask(__name__)
from app import routes
# Load our configuration from the config.py file
app.config.from_object(configObject)
