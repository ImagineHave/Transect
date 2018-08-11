import pytest
import pymongo
from werkzeug.security import check_password_hash, generate_password_hash
from transect.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()