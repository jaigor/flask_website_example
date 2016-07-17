from flask import render_template, flash, redirect, url_for
from app import app, db
from .models import User
from .forms import EditForm
from flask_login import login_user, logout_user, current_user, login_required
from oauth import OAuthSignIn
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required # make the user be logged on the website
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        {
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', 
                           title='Sign In')
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email, picture = oauth.callback()
    user = instance_user(social_id)

    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))

    if not user:
        user = User(social_id=social_id, 
                    nickname=username, 
                    email=email,
                    picture=picture)
        db.session.add(user)
        db.session.commit()
    else:
        # update Database with logged user
        user.username = username
        user.email = email
        user.picture = picture
        db.session.commit()

    # Login and validate the user
    login_user(user, True)
    return redirect(url_for('index'))

def instance_user(social_id):
    return User.query.filter_by(social_id=social_id).first()

@app.route('/user/<nickname>')
@login_required # make the user be logged on the website
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                            user=user,
                            posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = current_user.nickname
        form.about_me.data = current_user.about_me
    return render_template('edit.html', form=form)
