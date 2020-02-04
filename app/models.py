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
    canFeed = db.Column(db.Integer)
    canView = db.Column(db.Integer)
    style = db.Column(db.String(32))


@loginManager.user_loader
def load_user(id):
    return users.query.get(int(id))

