# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class configObject(object):
    # Secret key will be set to env var on production deployment
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'birds-for-lyfe'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'birdBox.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
