from flask import Blueprint, jsonify, request
from .db import get_db

bp = Blueprint('accounts', __name__, url_prefix='/feeder')

# a simple page that says feeder
@bp.route('/')
def index():
    return 'accounts'
    
# put an account into the database
@bp.route('/put', methods=['POST'])
def put():
    '''put in an account'''
    dataDict = request.get_json()
    db = get_db()
    db.fields.insert(dataDict)  
    return ('', 204)
    
# get an account from the database
@bp.route('/get', methods=['GET'])
def get():
    '''get an account'''
    print("herro")
    return 'load'