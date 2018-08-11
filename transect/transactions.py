import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from transect.db import ( 
    get_transactions_for_user, insert_transaction, get_transaction, update_transaction, delete_transaction
)

from werkzeug.exceptions import abort
from transect.auth import login_required

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# list all transactions
@bp.route('/all')
@login_required
def all():
    transactionsCursor = get_transactions_for_user(username=g.username)
    transactions = list(transactionsCursor)
    return render_template('transactions/all.html', transactions=transactions)
    

@bp.route('/add', methods=('POST','GET'))
@login_required
def add():
    if request.method == 'POST':
        userid = session.get('user_id')
        date = request.form['date']
        payer = request.form['payer']
        amount = request.form['amount']
        payee = request.form['payee']
        transaction = {"userid":userid, "date":date, "payer":payer, "amount":amount, "payee":payee}
        insert_transaction(transaction)
        return redirect(url_for('transactions.all'))
    return render_template('transactions/add.html')
    
    

def getTransaction(id):
    transaction = get_transaction(id)
    
    if transaction is None:
        abort(404, "Transaction doesn't exist.")
        
    if transaction['userid'] != session.get('user_id'):
        abort(403)    
        
    return transaction
    
@bp.route('/<id>/edit', methods=('POST','GET'))
@login_required
def edit(id):
    
    transaction = getTransaction(id)
    
    if request.method == 'POST':
        userid = session.get('user_id')
        
        print(request.form)
        
        date = request.form['date']
        payer = request.form['payer']
        amount = request.form['amount']
        payee = request.form['payee']
        transaction = {"userid":userid, "date":date, "payer":payer, "amount":amount, "payee":payee}
        update_transaction(id, transaction)
        return redirect(url_for('transactions.all'))

    return render_template('transactions/edit.html', transaction=transaction)   
    
    
@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    getTransaction(id)
    delete_transaction(id)
    return redirect(url_for('transactions.all'))    
    
    
    