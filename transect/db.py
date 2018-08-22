from mongoengine import connect
import click
from flask import current_app, g
from flask.cli import with_appcontext
import re
import time


def get_client():
    """get MongoClient."""
    print('...getting client...')
    if not hasattr(g, 'db_client'):
        regex = re.compile(r'^mongodb\:\/\/(?P<username>[_\w]+):(?P<password>[\w]+)@(?P<host>[\.\w]+):(?P<port>\d+)/(?P<database>[_\w]+)$')

        mongolab_url = current_app.config['MONGODB_SETTINGS']['MONGO_URI']

        match = regex.search(mongolab_url)
        data = match.groupdict()

        print(data)

        db = data['database']
        host = current_app.config['MONGODB_SETTINGS']['MONGO_URI']

        for _ in range(30):
            try:
                print("Attempting to connect to " + db + " @ " + host)
                g.db_client = connect(alias='default', db=db, host=host)
                return g.db_client
            except Exception as exc:
                print("Error connecting to mongo, will retry in 1 sec: %r", exc)
                time.sleep(1)
            else:
                print("Connected...")
                break
        else:
            print("Unable to connect to "+db+" @ " + host)

    return g.db_client


def get_db():
    """get DB"""
    print('getting database...')
    if not hasattr(g, 'db'):
        print('...start client connection...')
        g.db = get_client().get_database()
    return g.db


def close_db(e=None):
    """close connection"""
    db_client = g.pop('db_client', None)
    if db_client is not None:
        db_client.close()


def init_db():
    """wipe the database"""
    print('initialising')
    db = get_db()
    collections = db.collection_names(include_system_collections=False)
    for collection in collections:
        db[collection].drop()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    print('initialise db')
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)