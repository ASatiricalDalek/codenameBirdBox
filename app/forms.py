# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField, SubmitField, RadioField, SelectField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from app.models import users


class signIn(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me', default=False)
    signInBtn = SubmitField('Sign In')


class register(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    reg = SubmitField('Register')


    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
    def validate_username(self, username):
        usr = users.query.filter_by(username=username.data).first()
        if usr is not None:
            raise ValidationError('This username already exists! Please choose another.')

    def validate_email(self, email):
        user = users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Account with this email already exists!')


class feedSettings(FlaskForm):
    # Radio buttons for if the user can feed the bird, or view the bird (tuple format: ['value', 'label']
    canFeed = RadioField('User can Feed Bird', choices=[('True', 'Yes'), ('False', 'No')], validators=[DataRequired()],
                         default=True)
    # Checkbox for turning on scheduled feed
    # TODO: Enable the rest of this form only if this box is checked
    scheduledFeed = BooleanField('Enable Scheduled Feeding?', default=True)
    # Checkboxes for each day
    feedDay_Monday = BooleanField('Monday')
    feedDay_Tuesday = BooleanField('Tuesday')
    feedDay_Wednesday = BooleanField('Wednesday')
    feedDay_Thursday = BooleanField('Thursday')
    feedDay_Friday = BooleanField('Friday')
    feedDay_Saturday = BooleanField('Saturday')
    feedDay_Sunday = BooleanField('Sunday')
    # Dropdown box for each hour of the day. Stored in military time in the DB
    feedHour = SelectField('Hour', choices=(['00', '12 AM'], ['01', '1 AM'], ['02', '2 AM'], ['03', '3 AM'], ['04', '4 AM'],
                                            ['05', '5 AM'], ['06', '6 AM'], ['07', '7 AM'], ['08', '8 AM'], ['09', '9 AM'],
                                            ['10', '10 AM'], ['11', '11 AM'], ['12', '12 PM'], ['13', '1 PM'],
                                            ['14', '2 PM'], ['15', '3 PM'], ['16', '4 PM'], ['17', '5 PM'], ['18', ' 6 PM'],
                                            ['19', '7 PM'], ['20', '8 PM'], ['21', '9 PM'], ['22', '10 PM'],
                                            ['23', '11 PM']))
    # Associated minute for the hour
    feedMinute = SelectField('Minute', choices=(['0', '0'], ['5', '5'], ['10', '10'], ['15', '15'], ['20', '20'],
                                                ['25', '25'], ['30', '30'], ['35', '35'],
                                                ['40', '40'], ['45', '45'], ['50', '50'], ['55', '55']))
    apply = SubmitField('Apply Settings')

class themeSettings(FlaskForm):
    # Dropdown box for the theme selector
    themes = SelectField('Birdbox Theme',
                         choices=(['light', 'Light Theme'], ['dark', 'Dark Theme'], ['contrast', 'High Contrast']),
                         validators=[DataRequired()])
    apply = SubmitField('Apply Theme')
