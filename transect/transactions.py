from flask import Blueprint, jsonify, request
from .db import get_db

bp = Blueprint('transactions', __name__, url_prefix='/feeder')

# a simple page that says feeder
@bp.route('/')
def index():
    return 'transactions'
    
# put a transaction into the database
@bp.route('/put', methods=['POST'])
def put():
    '''put in a transaction'''
    dataDict = request.get_json()
    db = get_db()
    db.fields.insert(dataDict)  
    return ('', 204)
    
# get a transaction from the database
@bp.route('/get', methods=['GET'])
def get():
    '''get a transaction'''
    print("herro")
    return 'load'