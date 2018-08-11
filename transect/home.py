import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, 
)

from werkzeug.exceptions import abort
from transect.auth import login_required

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
@login_required
def index():
    return render_template('home/home.html')