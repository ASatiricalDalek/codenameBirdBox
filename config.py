# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
import os


class configObject(object):
    # Secret key will be set to env var on production deployment
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'birds-for-lyfe'
