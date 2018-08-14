import pymongo
import click
from flask import current_app, g
from flask.cli import with_appcontext
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash


def get_client():
    """get MongoClient."""
    if not hasattr(g, 'db_client'):
        g.db_client = pymongo.MongoClient(current_app.config['MONGO_URI'])
    return g.db_client


def get_db():
    """get DB"""
    if not hasattr(g, 'db'):
        g.db = get_client().get_database()
    return g.db


def close_db(e=None):
    """close connection"""
    db_client = g.pop('db_client', None)
    if db_client is not None:
        db_client.close()


def init_db():
    """wipe the database"""
    db = get_db()
    collections = db.collection_names(include_system_collections=False)
    for collection in collections:
        db[collection].drop()


def does_username_exist(username):
    if username is None:
        return False
    return get_db()['users'].find_one({"username": username}) is not None


def validate_user_password(username, password):
    return does_username_exist(username) and does_password_match_user(username, password)


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
    if not password:
        return None
    else:
        user = get_user(username=username)
        return check_password_hash(user['password'], password)


def get_user_id(user):
    return str(ObjectId(user['_id']))


def get_transactions_for_username(username=None):
    if username:
        user_id = get_user_id_from_username(username)
        return get_db()['transactions'].find({"user_id": user_id})
    else:
        return None


def get_transactions_for_user_id(user_id=None):
    if user_id:
        return get_db()['transactions'].find({"user_id": user_id})
    else:
        return None


def get_transaction_from_transaction_id(_id):
    return get_db()['transactions'].find_one({"_id": ObjectId(_id)})


def insert_transaction(transaction):
    return get_db()['transactions'].insert_one(transaction)


def update_transaction(_id, transaction):
    return get_db()['transactions'].update({"_id": ObjectId(_id)}, transaction)


def delete_transaction(_id):
    get_db()['transactions'].remove({"_id": ObjectId(_id)})


def get_transaction_id(transaction):
    return str(get_db()['transactions'].find_one(transaction)['_id'])


def get_transaction(transaction):
    return get_db()['transactions'].find_one(transaction)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
