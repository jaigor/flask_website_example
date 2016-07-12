from app import db
# dependencies for OAuth Autenthification
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin

app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '636798506489008',
        'secret': '4d94fc2a98b9b50e1ac0b658e6ead3cc'
    },
    'twitter': {
        'id': 'PcivizZbO4nUHDxVNL61eP1VA',
        'secret': 'OPSnX2aNfrNa4kykxze9h1HQkynpMAC3qtxvRD8b8jtrtpmugR'
    }
}

lm = LoginManager(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True) 
    # relationship between Post and User, backref used as a reference in Post()
    posts = db.relationship('Post', backref='author', lazy='dynamic') 

    def __repr__(self):
        return '<User %r>' % (self.nickname)

# user loader callback function
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime) # all in UTC time zone
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

    def __repr__(self):
        return '<Post %r>' % (self.body)


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))