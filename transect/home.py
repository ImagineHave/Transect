import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('home/home.html')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.username is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view