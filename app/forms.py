from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from .models import User
import urllib2
import json

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            self.nickname.errors.append(gettext('This nickname has invalid characters. Please use letters, numbers, dots and underscores only.'))
            return False
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append(gettext('This nickname is already in use. Please choose another one.'))
            return False
        return True

class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])

    def checkRecaptcha(response, secretkey):
        url = 'https://www.google.com/recaptcha/api/siteverify?'
        url = url + 'secret=' +secretkey
        url = url + '&response=' +response
        try:
            jsonobj = json.loads(urllib2.urlopen(url).read())
            if jsonobj['success']:
                return True
            else:
                return False
        except Exception as e:
            print e
            return False