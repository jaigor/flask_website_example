#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_picture(self):
        # no picture user
        u = User(social_id='twitter_user', 
                    nickname='twitter_user', 
                    email='twitter@mail.com',
                    picture=None)
        pic = User.default_picture(u.picture)
        expected = 'http://www.gravatar.com/avatar/?d=mm'
        assert pic[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        u = User(social_id='john_id', nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        assert nickname != 'john'
        u = User(social_id='susan_id', nickname=nickname, email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        assert nickname2 != 'john'
        assert nickname2 != nickname

if __name__ == '__main__':
    unittest.main()