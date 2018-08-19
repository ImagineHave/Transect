import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect


def create_app(test_config=None):
    """create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)
    CSRFProtect(app)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping({
            'TESTING': True,
            'SECRET_KEY': os.environ['SECRET_KEY'],
            'MONGODB_SETTINGS': {'MONGO_URI': os.environ['MONGO_URI']}
        })

    """ a simple page that says hello """
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from transect.service import auth
    app.register_blueprint(auth.bp)

    from transect.service import home
    app.register_blueprint(home.bp)

    from transect.service import accounts
    app.register_blueprint(accounts.bp)

    from transect.service import transactions
    app.register_blueprint(transactions.bp)
    
    return app


