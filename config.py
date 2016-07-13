import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

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
APP_ID = '636798506489008'
REDIRECT_URI = 'http://localhost:5000/callback/facebook'
SCOPE = 'public_profile,email'
APP_SECRET = '4d94fc2a98b9b50e1ac0b658e6ead3cc'