from mongoengine import connect
import click
from flask import current_app, g
from flask.cli import with_appcontext
import re
import time


def get_client():
    """get MongoClient."""
    if not hasattr(g, 'db_client'):
        regex = re.compile(r'^mongodb\:\/\/(?P<username>[_\w]+):(?P<password>[\w]+)@(?P<host>[\.\w]+):(?P<port>\d+)/(?P<database>[_\w]+)$')

        mongolab_url = current_app.config['MONGODB_SETTINGS']['MONGO_URI']

        match = regex.search(mongolab_url)
        data = match.groupdict()

        print(data)

        for _ in range(30):
            try:
                print("Attempting to connect to %s at %s...", data['database'],
                      current_app.config['MONGODB_SETTINGS']['MONGO_URI'])
                g.db_client = connect(db=data['database'], host=current_app.config['MONGODB_SETTINGS']['MONGO_URI'])
            except Exception as exc:
                print("Error connecting to mongo, will retry in 1 sec: %r", exc)
                time.sleep(1)
            else:
                print("Connected...")
                break
        else:
            print("Unable to connect to %s at %s: %r", data['database'], current_app.config['MONGODB_SETTINGS']['MONGO_URI'], exc)
            raise exc

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


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
