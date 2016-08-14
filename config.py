# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

# Search Engine
WHOOSH_BASE = os.path.join(basedir, 'search.db')
# Whoosh does not work on Heroku
WHOOSH_ENABLED = os.environ.get('HEROKU') is None

MAX_SEARCH_RESULTS = 50

# deactivating event system
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'SECRET-KEY'

# credentials used for the services to access
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': os.environ['FACEBOOK-APP-ID'],
        'secret': os.environ['FACEBOOK-APP-SECRET']
    },
    'twitter': {
        'id': os.environ['TWITTER-APP-ID'],
        'secret': os.environ['TWITTER-APP-SECRET']
    }
}

# mail server settings (configuration depends on the server to use (SMTP, POP3, ...))
# Gmail example
MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS',  False))
MAIL_USE_SSL = int(os.environ.get('MAIL_USE_SSL',  True))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME','username@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','password')

# administrator list
ADMINS = 'ADMINS'

# pagination
POSTS_PER_PAGE = 3

# Available Languages
LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

# microsoft translation service
MS_TRANSLATOR_CLIENT_ID = 'MS_TRANSLATOR_CLIENT_ID' # enter your MS translator app id here
MS_TRANSLATOR_CLIENT_SECRET = 'MS_TRANSLATOR_CLIENT_SECRET' # enter your MS translator app secret here