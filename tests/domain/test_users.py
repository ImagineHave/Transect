from transect.domain.users import (
    insert_user, get_by_username, get_by_user_id, get_user, get_username_from_user_id, get_user_id_from_username,
    does_password_match_user, does_username_exist, Users
)
from tests.conftest import (
    PASSWORD1, USERNAME1, USERNAME2,
)


def test_insert_user(app):
    with app.app_context():
        data = {
            'username': 'a',
            'password': 'a',
            'email': 'a'
        }
        insert_user(data)
        assert Users.objects(**data).first() is not None


def test_get_by_username(app):
    with app.app_context():
        assert get_by_username(USERNAME1) is not None


def test_get_by_user_id(app):
    with app.app_context():
        user = Users.objects(username=USERNAME1).first()
        get_by_user_id(user.get_id())


def test_get_user(app):
    with app.app_context():
        user = Users.objects(username=USERNAME1).first()
        user_id = user.get_id()
        assert USERNAME1 == get_user(username=USERNAME1).username
        assert USERNAME1 == get_user(_id=user_id).username
        assert USERNAME1 == get_user(_id=None, username=USERNAME1).username
        assert USERNAME1 == get_user(username=None, _id=user_id).username
        assert USERNAME1 == get_user(username=USERNAME1, _id=user_id).username
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
        assert get_user_id_from_username(USERNAME1) == test_user.get_user_id()
        assert get_user_id_from_username(USERNAME2) is not test_user.get_user_id()
        assert get_user_id_from_username(None) is not test_user.get_user_id()


def test_check_password_for_user(app):
    with app.app_context():
        assert does_password_match_user(USERNAME1, PASSWORD1)
        assert does_password_match_user(USERNAME1) is None
        assert does_password_match_user(USERNAME1, 'notpasswrd') is False


def test_does_username_exist(app):
    with app.app_context():
        assert does_username_exist(USERNAME1)
        assert not does_username_exist('as98fsd987045h0hd89f98h45b')
        assert not does_username_exist(None)


