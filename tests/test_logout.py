import pytest
from flask import g, session
from transect.db import get_db


def test_logout(client, auth, testUser):
    with client:
        response = auth.login()
        assert response.status_code == 200
        assert b'home' in response.data
        assert b'login' not in response.data
        assert b'register' not in response.data
        assert session['userid'] == testUser.getUserid()
        assert g.username == 'test'
        response = auth.logout()
        assert b'home' not in response.data
        assert b'login' in response.data
        assert b'register' in response.data
        assert 'userid' not in session
        assert g.username != 'test'