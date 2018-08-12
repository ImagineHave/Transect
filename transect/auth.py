import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from transect.db import ( 
    get_user, createUser, getUsernameFromUserid, getUseridFromUsername, validateUserPassword
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
        email = request.form['email']

        print(username)
        print(password)
        print(email)

        if getUseridFromUsername(username=username) is None:
            createUser(username, password, email)
            return redirect(url_for('auth.login'))

        flash('username already taken')

    return render_template('auth/register.html', title='register', form=form)
 
    
@bp.route('/login', methods=('POST','GET'))
def login():
    
    form = LoginForm(request.form)

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        
        if validateUserPassword(username,password):
            session['userid'] = getUseridFromUsername(username)
            return redirect(url_for('home.index'))
            
        flash('invalid logon details.')
            
    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    userid = session.get('userid')
    if userid is None:
        g.username = None
    else:
        g.username = getUsernameFromUserid(userid)
        
        
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