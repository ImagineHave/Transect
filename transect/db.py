from mongoengine import connect
import click
from flask import current_app, g
from flask.cli import with_appcontext
import re


def get_client():
    """get MongoClient."""
    if not hasattr(g, 'db_client'):
        regex = re.compile(r'^mongodb\:\/\/(?P<username>[_\w]+):(?P<password>[\w]+)@(?P<host>[\.\w]+):(?P<port>\d+)/(?P<database>[_\w]+)$')

        mongolab_url = current_app.config['MONGODB_SETTINGS']['MONGO_URI']

        match = regex.search(mongolab_url)
        data = match.groupdict()

        g.db_client = connect('default',
                              data['database'],
                              host=data['host'],
                              port=int(data['port']),
                              username=data['username'],
                              password=data['password'])
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
