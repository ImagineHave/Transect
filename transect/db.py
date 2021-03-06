from mongoengine import connect
import click
from flask import current_app, g
from flask.cli import with_appcontext
from transect.domain.frequencies import create_standard_frequencies
from transect.domain.accounts import create_standard_test_accounts


def get_client():
    """get MongoClient."""
    if not hasattr(g, 'db_client'):
        host = current_app.config['MONGODB_SETTINGS']['MONGO_URI']
        g.db_client = connect(host=host)

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
    create_standard_frequencies()
    create_standard_test_accounts()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    with app.app_context():
        get_db()


def init_test_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    with app.app_context():
        get_db()
        init_db()
