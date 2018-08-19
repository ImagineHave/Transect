import pytest
import os
from transect import create_app
from transect.db import get_db, init_db
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId


@pytest.fixture
def app():

    app = create_app({'TESTING': True,
                      'WTF_CSRF_ENABLED': False,
                      'DEBUG': True,
                      'SECRET_KEY': 'someSecret5hizz',
                      'MONGODB_SETTINGS': {'MONGO_URI': os.environ['MONGO_URI']}
                      })
    
    with app.app_context():
        init_db()
    
    with app.app_context():
        get_db()['users'].insert_one({"username": 'test', "password": generate_password_hash('test'),
                                      "email": "e@ma.il"})
        get_db()['users'].insert_one({"username": 'test1', "password": generate_password_hash('test1'),
                                      "email": "e2@ma.il"})
    
    yield app
    
    
@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, data=None):
        if data is None:
            data = {'username': 'test', 'password': 'test'}
        return self._client.post(
            '/auth/login',
            data=data,
            follow_redirects=True
        )

    def logout(self):
        return self._client.get(
            '/auth/logout',
            follow_redirects=True
        )

    def register(self, data):
        return self._client.post(
            '/auth/register',
            data=data,
            follow_redirects=True
        )
        
    def post_and_redirect(self, url, data=None):
        return self._client.post(
            url, 
            data=data,
            follow_redirects=True
        )
        
    def post(self, url, data=None):
        return self._client.post(
            url, 
            data=data,
        )
        
    def get_and_redirect(self, url, data=None):
        return self._client.get(
            url, 
            data=data, 
            follow_redirects=True
        )
        
    def get(self, url, data=None):
        return self._client.get(
            url, 
            data=data,
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)


class TestUser(object):
    def __init__(self, app):
        self.app = app
        
    def get_user_id(self, username='test'):
        with self.app.app_context():
            return str(get_db()['users'].find_one({"username": username})['_id'])
            
    def get_username(self, username='test'):
        with self.app.app_context():
            return get_db()['users'].find_one({"username": username})['username']
            
    def get_user_from_username(self, username='test'):
        with self.app.app_context():
            return get_db()['user'].find_one({"username": username})
            
    def get_user_from_user_id(self, user_id):
        with self.app.app_context():
            return get_db()['user'].find_one({"username": ObjectId(user_id)})


@pytest.fixture
def test_user(app):
    return TestUser(app)


