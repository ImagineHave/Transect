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


def get_username(username=None, id=None):
    if username: 
        return get_db()['users'].find_one({"username":username})['username']
    if id:
        return get_db()['users'].find_one({"_id":ObjectId(user_id)})['username']
    return None
        

def set_user(username, password):
    get_db()['users'].insert_one({"username":username,"password":generate_password_hash(password)})
    
    
def check_password_for_user(username, password=None):
    ''' make sure you cannot match none against none '''
    if not password:
        return None
    else:
        user = get_user(username=username)
        return check_password_hash(user['password'], password)


def get_user(username=None, id=None):
    if not username and not id:
        return None
    if not id: 
        return get_db()['users'].find_one({"username":username})
    if not uesrname:
        return get_db()['users'].find_one({"_id":ObjectId(id)})


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data."""
    init_db()
    click.echo('Initialized the database.')
        
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)