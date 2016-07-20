from app import db, lm
# dependencies for OAuth Autenthification
from flask_login import UserMixin
from oauth import FacebookSignIn

class User(UserMixin, db.Model):
    """User Basic Information model."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # User id from the provider service
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=True)
    picture = db.Column(db.String(256), nullable=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    # User Relationships
    # relationship between Post and User, backref used as a reference in Post()
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def default_picture(picture):
        if picture == None:
            picture = 'http://www.gravatar.com/avatar/?d=mm'
        
        return picture

    @staticmethod
    def make_unique_nickname(nickname):
        """"Makes a new name for a used nickname
            It adds numbers of the versions that we are counting"""
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

class Post(db.Model):
    """User Posts model."""
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime) # all in UTC time zone
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

# user loader callback function
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))