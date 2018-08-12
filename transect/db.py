import pymongo
import click
from flask import current_app, g
from flask.cli import with_appcontext
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

def getClient():
    """get MongoClient."""
    if not hasattr(g, 'db_client'):
        g.db_client = pymongo.MongoClient(current_app.config['MONGO_URI'])
    return g.db_client
    
    
def get_db():
    """get DB"""
    if not hasattr(g, 'db'):
        g.db = getClient().get_default_database()
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

def doesUsernameExist(username):
    if username == None:
        return False
    return get_db()['users'].find_one({"username":username}) is not None


def validateUserPassword(username, password):
    return doesUsernameExist(username) and doesPasswordMatchUser(username, password)


def set_user(username, password):
    get_db()['users'].insert_one({"username":username,"password":generate_password_hash(password)})
    

def getByUsername(username):
    return get_db()['users'].find_one({"username":username})
    
    
def getByUserId(id):
    return get_db()['users'].find_one({"_id":ObjectId(id)})


def get_user(username=None, id=None):
    if username: 
        return getByUsername(username)
    if id:
        return getByUserId(id)
    return None
    
    
def get_username(username=None, id=None):
    user=get_user(username=username,id=id)
    if user:
        return user['username']
    else:
        return None


def get_userid(username=None, id=None):
    user=get_user(username=username,id=id)
    if user:
        return str(user['_id'])
    else:
        return None


def doesPasswordMatchUser(username, password=None):
    ''' make sure you cannot match none against none '''
    if not password:
        return None
    else:
        user = get_user(username=username)
        return check_password_hash(user['password'], password)


def getUserId(user):
    return str(ObjectId(user['_id']))


def get_transactions_for_user(username=None, userid=None):
    user=get_user(username=username,id=userid)
    if user:
        userid = getUserId(user)
        return get_db()['transactions'].find({"userid":userid})
    else:
        return None


def get_transaction(id):
    return get_db()['transactions'].find_one({"_id":ObjectId(id)})


def insert_transaction(transaction):
    return get_db()['transactions'].insert_one(transaction)


def update_transaction(id, transaction):
    return get_db()['transactions'].update({"_id":ObjectId(id)}, transaction)
    

def delete_transaction(id):
    get_db()['transactions'].remove({"_id":ObjectId(id)})
    
    
def getTransactionId(transaction):
    return str(get_db()['transactions'].find_one(transaction)['_id'])


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data."""
    init_db()
    click.echo('Initialized the database.')
        
        
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)