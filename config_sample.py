import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Search Engine
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# deactivating event system
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'YOUR-SECRET-KEY-GOES-HERE'

# credentials used for the services to access
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': 'FACEBOOK APP ID ASSIGNED',
        'secret': 'FACEBOOK APP SECRET ASSIGNED'
    },
    'twitter': {
        'id': 'TWITTER APP ID ASSIGNED',
        'secret': 'TWITTER APP SECRET ASSIGNED'
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
ADMINS = ['you@example.com']

# pagination
POSTS_PER_PAGE = 3