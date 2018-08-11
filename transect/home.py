import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('home/home.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    print user_id

    if user_id is None:
        g.username = None
    else:
        g.username = get_username(id=user_id)
        
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth/login.html'))
    
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.username is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view