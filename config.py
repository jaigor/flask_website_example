import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

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