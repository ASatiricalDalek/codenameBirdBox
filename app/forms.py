# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField, SubmitField
from wtforms.validators import data_required


class signIn(FlaskForm):
    username = StringField('Username', validators=['DataRequired()'])
    password = StringField('Password', validators=['DataRequired()'])
    remember = BooleanField('Remember Me')
    signInBtn = SubmitField('Sign In')
