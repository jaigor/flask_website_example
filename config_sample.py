import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

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
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['you@example.com']