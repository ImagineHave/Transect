import os
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db


@pytest.fixture
def app():
    
    app = create_app({'TESTING': True})
    
    with app.app_context():
        init_db()
        
    yield app
    
    
@pytest.fixture
def client(app):
    return app.test_client()
    
@pytest.fixture
def runner(app):
    return app.test_cli_runner()