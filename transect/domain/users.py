from werkzeug import security
from mongoengine import StringField, DateTimeField, Document
import datetime


class Users(Document):
    username = StringField(max_length=200, required=True)
    password = StringField(max_length=200, required=True)
    email = StringField(required=True)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

    def get_id(self):
        return str(self.id)


def does_username_exist(username):
    return Users.objects(username=username).count() == 1


def generate_password_hash(password=None):
    return security.generate_password_hash(password)


def insert_user(data):
    data['password'] = security.generate_password_hash(data['password'])
    user = Users(**data)
    user.save()


def get_by_username(username):
    return Users.objects(username=username).first()


def get_by_user_id(_id):
    return Users.objects(id=_id).first()


def get_user(username=None, _id=None):
    if username:
        return get_by_username(username)
    if _id:
        return get_by_user_id(_id)
    return None


def get_username_from_user_id(_id):
    if _id is not None:
        user = get_by_user_id(_id)
        if user is not None:
            return user.username


def get_user_id_from_username(username):
    user = get_by_username(username)
    if user:
        return user.get_id()
    else:
        return None


def does_password_match_user(username, password=None):
    user = get_user(username=username)
    if not password or not user:
        return None
    else:
        return security.check_password_hash(user.password, password)

