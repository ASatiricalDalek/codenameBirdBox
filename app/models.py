from app import db


# Python object that maps to our users in the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    # This built-in function tells Python how to print these objects for debugging purposes
    def __repr__(self):
        return '<User {}>'.format(self.username)
