from app import db, lm, app
from config import WHOOSH_ENABLED
# dependencies for OAuth Autenthification
from flask_login import UserMixin
from oauth import FacebookSignIn
# for security handler
import re

import sys
# if version is 3 or newer, cant use search tool
if sys.version_info >= (3,0):
    enable_search = False
else:
    enable_search = True
    import flask_whooshalchemy as whooshalchemy

# Table of followers
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

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
    # Post and User (one-to-many)
    posts = db.relationship('Post', 
                            backref='author', # = used as a reference in Post()
                            lazy='dynamic')
    # User to User (many-to-many)
    followed = db.relationship('User',
                                secondary=followers, # = table referred, 
                                primaryjoin=(followers.c.follower_id == id), # links left side with association table
                                secondaryjoin=(followers.c.followed_id == id), # links association table with right side
                                backref=db.backref('followers', lazy='dynamic'), # how this relationship will be accessed from the right side
                                lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def default_picture(picture):
        """Assigns a default picture if there is None returned"""
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

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
            
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers,(followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

    def ordered_posts(self):
        return Post.query.order_by(Post.timestamp.desc())

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname) #sub == remove

class Post(db.Model):
    """User Posts model."""
    __tablename__ = 'posts'
    __searchable__ = ['body'] # field indexed by whoosh
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime) # all in UTC time zone
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post %r>' % (self.body)

if enable_search:
    whooshalchemy.whoosh_index(app, Post)

# user loader callback function
@lm.user_loader 
def load_user(id):
    return User.query.get(int(id))