from flask import render_template, flash, redirect, url_for, request, g, jsonify
from app import app, db, babel
from .models import User, Post
from .forms import EditForm, PostForm
from .emails import follower_notification
from .translate import microsoft_translate
from flask_login import login_user, logout_user, current_user, login_required
from oauth import OAuthSignIn
from datetime import datetime
from config import POSTS_PER_PAGE, LANGUAGES, DATABASE_QUERY_TIMEOUT
from flask_babel import gettext
from guess_language import guessLanguage
from flask_sqlalchemy import get_debug_queries


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required # make the user be logged on the website
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        language = guessLanguage(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, 
                    timestamp=datetime.utcnow(), 
                    author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(gettext(u'Your post is now live!'), 'info')
        return redirect(url_for('index'))

    posts = current_user.followed_posts().paginate(page, POSTS_PER_PAGE, False)

    return render_template('index.html',
                           title='Home',
                           form=form,
                           posts=posts,
                           request=request)

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
    g.locale = get_locale()

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

    # call provider (Facebook, Twitter, ...)
    oauth = OAuthSignIn.get_provider(provider)
    # assigns values to parameters
    social_id, username, email, picture = oauth.callback()
    user = instance_user(social_id)

    # fails the authentication method
    if social_id is None:
        flash(gettext(u'Authentication failed.'), 'error')
        return redirect(url_for('index'))

    if not user:
        if instance_username(username):
            # removes from the name some characters (security) 
            username = User.make_valid_nickname(username)
            # If username exits looks for another 
            username = User.make_unique_nickname(username)
        else:
            pass    
        # Instances new user in database
        user = User(social_id=social_id, 
                        nickname=username, 
                        email=email,
                        picture=picture)
        user.picture = User.default_picture(picture)
        db.session.add(user)
        # make the user follow him/herself
        db.session.add(user.follow(user))
        db.session.commit()
    else:
        # update Database with logged user
        user.email = email
        user.picture = User.default_picture(picture)
        db.session.commit()

    # Login and validate the user
    login_user(user, True)
    return redirect(url_for('index'))

def instance_user(social_id):
    """ Search for the user (social_id) in the database"""
    return User.query.filter_by(social_id=social_id).first()

def instance_username(username):
    """ Search for the user (username) in the database"""
    return User.query.filter_by(nickname=username).first()

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required # make the user be logged on the website
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash(gettext(u'User %(nickname)s not found.' % nickname), 'error')
        return redirect(url_for('index'))
    posts = user.ordered_posts.paginate(page, POSTS_PER_PAGE, False)
    
    return render_template('user.html',
                            user=user,
                            posts=posts,
                            request=request)

# Edit user profile form 
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(current_user.nickname)
    if form.validate_on_submit():
        # checks if the username didnt change
        if form.nickname.data == current_user.nickname:
            new_nickname = current_user.nickname
        else:
            # removes from the name some characters (security) 
            new_nickname = User.make_valid_nickname(form.nickname.data)
            new_nickname = User.make_unique_nickname(new_nickname)
        current_user.nickname = new_nickname
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        # alert correct message
        flash(gettext(u'Your changes have been saved.'), 'info') 
        return redirect(url_for('edit'))
    else:
        form.nickname.data = current_user.nickname
        form.about_me.data = current_user.about_me
    return render_template('edit.html', 
                            form=form)

# Custom HTTP Handlers: 404 and 500 
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Follow and Unfollow links
@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        # alert wrong message
        flash(gettext(u'User %(nickname)s not found.', nickname=nickname), 'error')
        return redirect(url_for('index'))
    if user == current_user:
        flash(gettext(u'You can\'t follow yourself!'), 'error')
        return redirect(url_for('user', nickname=nickname))
    u = current_user.follow(user)
    if u is None:
        flash(gettext(u'Cannot follow %(nickname)s.', nickname=nickname), 'error')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext(u'You are now following %(nickname)s!', nickname=nickname), 'info')
    follower_notification(user, current_user)
    return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(gettext(u'User %(nickname)s not found.', nickname=nickname), 'error')
        return redirect(url_for('index'))
    if user == current_user:
        flash(gettext(u'You can\'t unfollow yourself!'), 'error')
        return redirect(url_for('user', nickname=nickname))
    u = current_user.unfollow(user)
    if u is None:
        flash(gettext(u'Cannot unfollow %(nickname)s.', nickname=nickname), 'error')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext(u'You have stopped following %(nickname)s!', nickname=nickname), 'info')
    return redirect(url_for('user', nickname=nickname))

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

@app.route('/translate', methods=['POST'])
@login_required
def translate():
    return jsonify({ 
        'text': microsoft_translate(
            request.form['text'], 
            request.form['sourceLang'], 
            request.form['destLang']) })

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post is None:
        flash('Post not found.')
        return redirect(url_for('index'))
    if post.author.id != current_user.id:
        flash('You cannot delete this post.')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.')
    return redirect(url_for('index'))

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
    return response