import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from flask_mail import Mail

from .momentjs import momentjs

from flask.json import JSONEncoder

# Instance the app and config.py file
app = Flask(__name__)
app.config.from_object('config')
# Instance database in SQLAlchemy
db = SQLAlchemy(app)
# Instace Login Manager Handler
lm = LoginManager(app)
lm.login_view = 'login'
# Instance Mail object to connect SMTP server and send emails
mail = Mail(app)

# Language library
from flask_babel import Babel, lazy_gettext
babel = Babel(app)
lm.login_message = lazy_gettext('Please log in to access this page.')

class CustomJSONEncoder(JSONEncoder):
    """This class adds support for lazy translation texts to Flask's
    JSON encoder. This is necessary when flashing translated texts."""
    def default(self, obj):
        from speaklater import is_lazy_string
        if is_lazy_string(obj):
            try:
                return unicode(obj)  # python 2
            except NameError:
                return str(obj)  # python 3
        return super(CustomJSONEncoder, self).default(obj)

app.json_encoder = CustomJSONEncoder

if not app.debug and MAIL_SERVER != '':
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                               'no-reply@' + MAIL_SERVER, ADMINS,
                               'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

# Enable the email handler (only without debugging)
if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    # file limited to 1 megabyte size and a backup of 10 log files (log history)
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 
                                        1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('microblog startup')

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('microblog startup')


# importing library momentjs for timestamp, as a global variable to all templates
app.jinja_env.globals['momentjs'] = momentjs

from app import views, models

