# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
from app import db, loginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Python object that maps to our users in the database
# UserMixin is the generic implementation of Flask_Login requirements for our logins to work w/ flask
class users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(64))

    # This built-in function tells Python how to print these objects for debugging purposes
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class attributes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey(users.id))
    isAdmin = db.Column(db.Integer)
    canFeed = db.Column(db.Integer)
    style = db.Column(db.String(32))
    scheduleFeed = db.Column(db.Integer)
    # 1 Represents Monday - 7 For Sunday
    feedDays = db.Column(db.Integer)
    feedHour = db.Column(db.Integer)
    feedMinute = db.Column(db.Integer)

    def check_admin(self):
        if self.isAdmin == 1:
            return True
        else:
            return False

    def check_feed_right(self):
        if self.canFeed == 1:
            return True
        else:
            return False


class feedTimes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey(users.id))
    feed_time = db.Column(db.String)
    feed_type = db.Column(db.String)

@loginManager.user_loader
def load_user(id):
    return users.query.get(int(id))

