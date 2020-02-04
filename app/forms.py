# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import users


class signIn(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me', default=False)
    signInBtn = SubmitField('Sign In')


class register(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confPassword = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    reg = SubmitField('Register')

    def validate_username(self, username):
        usr = users.query.filter_by(username=username.data).first()
        if usr is not None:
            raise ValidationError('Please Select a Different Username')


class changeSettings(FlaskForm):
    canFeed = RadioField('User can Feed Bird', choices=(['True', 'Yes'], ['False', 'No']), validators=[DataRequired()])
    canView = RadioField('User can View Bird', choices=(['True', 'Yes'], ['False', 'No']), validators=[DataRequired()])
    themes = SelectField('Birdbox Theme', choices=(['light', 'Light Theme'], ['dark', 'Dark Theme'], ['contrast', 'High Contrast']), validators=[DataRequired()])
    apply = SubmitField('Apply Settings')

