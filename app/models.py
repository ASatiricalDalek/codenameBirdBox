from app import db


# Python object that maps to our users in the database
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    # This built-in function tells Python how to print these objects for debugging purposes
    def __repr__(self):
        return '<User {}>'.format(self.username)


class attributes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey(users.id))
    canFeed = db.Column(db.Integer)
    canView = db.Column(db.Integer)
    style = db.Column(db.String(32))
