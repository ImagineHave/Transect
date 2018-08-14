import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CSRFProtect(app)
    
    app.config.from_mapping(
            SECRET_KEY=os.environ['SECRET_KEY'],
            MONGO_URI=os.environ['MONGO_URI']
        )
    
    if test_config:
        app.config.from_mapping(test_config)
        
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
        
    # register the database commands on the app
    # we can initialise the database
    # database connections get torn down after each request
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import home
    app.register_blueprint(home.bp)
        
    from . import accounts
    app.register_blueprint(accounts.bp)
    
    from . import transactions
    app.register_blueprint(transactions.bp)
    
    return app


