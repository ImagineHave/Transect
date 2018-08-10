from flask import Blueprint, jsonify, request
from .db import get_db

bp = Blueprint('feeder', __name__, url_prefix='/feeder')

# a simple page that says feeder
@bp.route('/')
def hello():
    return 'feeder'
    
# a simple page that says feeder
@bp.route('/upload', methods=['POST'])
def upload():
    '''lets make a standard file to upload'''
    
    dataDict = request.get_json()
    db = get_db()
    db.fields.insert(dataDict)  
    
    return ('', 204)
    
# a simple page that says feeder
@bp.route('/load', methods=['GET'])
def load():
    '''load the bible into the database'''
    print("herro")
    return 'load'