# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField, SubmitField, RadioField, SelectField, BooleanField
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
    scheduledFeed = BooleanField('Enable Scheduled Feeding?')
    feedDay_Monday = BooleanField('Monday')
    feedDay_Tuesday = BooleanField('Tuesday')
    feedDay_Wednesday = BooleanField('Wednesday')
    feedDay_Thursday = BooleanField('Thursday')
    feedDay_Friday = BooleanField('Friday')
    feedDay_Saturday = BooleanField('Saturday')
    feedDay_Sunday = BooleanField('Sunday')
    feedHour = SelectField('Hour', choices=(['00', '12 AM'], ['01', '1 AM'], ['02', '2 AM'], ['03', '3 AM'], ['04', '4 AM'],
                                            ['05', '5 AM'], ['06', '6 AM'], ['07', '7 AM'], ['08', '8 AM'], ['09', '9 AM'],
                                            ['10', '10 AM'], ['11', '11 AM'], ['12', '12 PM'], ['13', '1 PM'],
                                            ['14', '2 PM'], ['15', '3 PM'], ['16', '4 PM'], ['17', '5 PM'], ['18', ' 6 PM'],
                                            ['19', '7 PM'], ['20', '8 PM'], ['21', '9 PM'], ['22', '10 PM'],
                                            ['23', '11 PM']))
    feedMinute = SelectField('Minute', choices=(['0', '0'], ['15', '15'], ['30', '30'], ['45', '45']))
    apply = SubmitField('Apply Settings')

