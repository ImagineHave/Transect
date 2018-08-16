from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from transect.db import get_db
from transect.domain.domain import Domain


class Users(Domain):

    def __init__(self, username=None, password=None, email=None, _id=None):
        self.table_name = 'users'
        self.properties = {'username': username,
                           'password': password,
                           'email': email,
                           '_id': _id}


def does_username_exist(username):
    if username is None:
        return False
    return get_db()['users'].find_one({"username": username}) is not None


def create_user(username, password, email):
    get_db()['users'].insert_one({"username": username, "password": generate_password_hash(password), "email": email})


def get_by_username(username):
    if username:
        return get_db()['users'].find_one({"username": username})
    else:
        return None


def get_by_user_id(_id):
    if _id:
        return get_db()['users'].find_one({"_id": ObjectId(_id)})
    else:
        return None


def get_user(username=None, _id=None):
    if username:
        return get_by_username(username)
    if _id:
        return get_by_user_id(_id)
    return None


def get_username_from_user_id(_id):
    user = get_by_user_id(_id)
    if user:
        return user['username']
    else:
        return None


def get_user_id_from_username(username):
    user = get_by_username(username)
    if user:
        return str(user['_id'])
    else:
        return None


def does_password_match_user(username, password=None):
    user = get_user(username=username)
    if not password or not user:
        return None
    else:
        return check_password_hash(user['password'], password)


def get_user_id(user):
    return str(ObjectId(user['_id']))