from flask import Blueprint

bp = Blueprint('accounts', __name__, url_prefix='/feeder')


@bp.route('/')
def index():
    return 'accounts'
    

@bp.route('/put', methods=['POST'])
def put():
    return 'Hello, World!'
    

@bp.route('/get', methods=['GET'])
def get():
    return 'Hello, World!'
