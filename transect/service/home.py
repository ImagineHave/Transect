from flask import (
    Blueprint, render_template,
)
from transect.service.auth import login_required

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
@login_required
def index():
    return render_template('home/home.html')
