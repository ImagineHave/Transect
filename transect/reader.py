from flask import Blueprint

bp = Blueprint('reader', __name__, url_prefix='/reader')

# a simple page that says hello
@bp.route('/')
def hello():
    return 'reader!'
    
# a simple page that says hello
@bp.route('/quote')
def quote():
    return 'quote!'