from transect import create_app
import os


def test_config():
    assert not create_app().testing
    assert create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'DEBUG': True,
        'SECRET_KEY': 'someSecret5hizz',
        'MONGODB_SETTINGS': {'MONGO_URI': os.environ['MONGO_URI']}
    }).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
