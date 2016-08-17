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
SECRET_KEY = 'my-secret-is-well-known'

# credentials used for the services to access
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '636798506489008',
        'secret': '4d94fc2a98b9b50e1ac0b658e6ead3cc'
    },
    'twitter': {
        'id': 'PcivizZbO4nUHDxVNL61eP1VA',
        'secret': 'OPSnX2aNfrNa4kykxze9h1HQkynpMAC3qtxvRD8b8jtrtpmugR'
    }
}

# mail server settings (configuration depends on the server to use (SMTP, POP3, ...))
MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS',  False))
MAIL_USE_SSL = int(os.environ.get('MAIL_USE_SSL',  True))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME','jaigor@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','GUCITusr%5')

# administrator list
ADMINS = ['jaigor@gmail.com']

# pagination
POSTS_PER_PAGE = 3

# Available Languages
LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

# microsoft translation service
MS_TRANSLATOR_CLIENT_ID = 'flask_website_example' # enter your MS translator app id here
MS_TRANSLATOR_CLIENT_SECRET = 'rQFWALD49+ZfNj3IW9ogYRKuR9rhDeCe/jlJIFi8Jjs=' # enter your MS translator app secret here

## Google Recaptcha
# Check https://www.google.com/recaptcha/intro/index.html
RECAPTCHA_SITE_KEY = '6Ld6qicTAAAAAIbQZLK1HPjyhI7BO2F2t5dU8A-M'
RECAPTCHA_SECRET_KEY = '6Ld6qicTAAAAAAf5nAaHCBOg5vA0ddNVTwHvSX1e'