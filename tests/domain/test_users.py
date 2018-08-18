from transect.db import get_db
from transect.domain.users import create_user, get_by_username, get_by_user_id, get_user, get_username_from_user_id, \
    get_user_id_from_username, does_password_match_user, does_username_exist


def test_create_user(app):
    with app.app_context():
        create_user('a', 'a', 'a')
        assert get_db()['users'].find_one({'username': 'a'}) is not None


def test_get_by_username(app):
    with app.app_context():
        assert get_by_username('test') is not None


def test_get_by_user_id(app):
    with app.app_context():
        user = get_db()['users'].find_one({'username': 'test'})
        get_by_user_id(str(user['_id']))


def test_get_user(app):
    with app.app_context():
        user = get_db()['users'].find_one({'username': 'test'})
        user_id = str(user['_id'])
        assert user['username'] == get_user(username='test').username
        assert user['username'] == get_user(_id=user_id).username
        assert user['username'] == get_user(_id=None, username='test').username
        assert user['username'] == get_user(username=None, _id=user_id).username
        assert user['username'] == get_user(username='test', _id=user_id).username
        assert get_user(_id=None, username=None) is None


def test_get_username_from_id(app, test_user):
    with app.app_context():
        user_id = test_user.get_user_id()
        assert get_username_from_user_id(user_id) == test_user.get_username()
        not_id = test_user.get_user_id()
        not_id = not_id[-1:] + not_id[1:-1] + not_id[:1]
        assert get_username_from_user_id(not_id) is not test_user.get_username()
        assert get_username_from_user_id(None) is not test_user.get_username()


def test_get_user_id_from_username(app, test_user):
    with app.app_context():
        assert get_user_id_from_username('test') == test_user.get_user_id()
        assert get_user_id_from_username('test1') is not test_user.get_user_id()
        assert get_user_id_from_username(None) is not test_user.get_user_id()


def test_check_password_for_user(app):
    with app.app_context():
        assert does_password_match_user('test', 'test')
        assert does_password_match_user('test') is None
        assert does_password_match_user('test', 'notpasswrd') is False


def test_does_username_exist(app):
    with app.app_context():
        assert does_username_exist('test')
        assert not does_username_exist('as98fsd987045h0hd89f98h45b')
        assert not does_username_exist(None)


