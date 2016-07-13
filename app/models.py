from app import db
from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
# dependencies for OAuth Autenthification
from flask_login import UserMixin
from oauth import OAuthSignIn

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # User Information
    id = db.Column(db.Integer, primary_key=True)
    # User id from the provider service
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True) 
    # User Relationships
    # relationship between Post and User, backref used as a reference in Post()
    posts = db.relationship('Post', backref='author', lazy='dynamic') 

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime) # all in UTC time zone
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
