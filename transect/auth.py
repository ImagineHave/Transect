import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from transect.db import ( 
    get_user, set_user, get_username, get_userid, check_password_for_user
)

from transect.forms.auth.login import LoginForm
from transect.forms.auth.register import RegisterForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('POST','GET'))
def register():
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif get_username(username=username):
            error = 'User {} is already registered.'.format(username)
        if error is None:
            set_user(username, password)
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', title='register', form=form)
 
    
@bp.route('/login', methods=('POST','GET'))
def login():
    
    form = LoginForm(request.form)
    
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        error = None

        if not get_username(username=username) and not check_password_for_user(username,password):
            error='invalid details.'
        
        if error is None:
            session.clear()
            session['user_id'] = get_userid(username=username)
            return redirect(url_for('home.index'))
            
        flash(error)
            
    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.username = None
    else:
        g.username = get_username(id=user_id)
        
        
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