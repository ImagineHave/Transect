import functools

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)

from transect.domain.users import get_user_id_from_username, create_user, get_username_from_user_id
from transect.forms.auth.login import LoginForm
from transect.forms.auth.register import RegisterForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('POST', 'GET'))
def register():
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        create_user(username, password, email)
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='register', form=form)
 
    
@bp.route('/login', methods=('POST', 'GET'))
def login():
    
    form = LoginForm(request.form)

    if form.validate_on_submit():
        username = request.form['username']
        session['user_id'] = get_user_id_from_username(username)
        return redirect(url_for('home.index'))

    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.username = None
    else:
        g.username = get_username_from_user_id(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
    
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.username is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
