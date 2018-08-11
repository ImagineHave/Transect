import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from transect.db import ( 
    get_transactions_for_user, insert_transaction
)


bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# list all transactions
@bp.route('/all')
def all():
    transactionsCursor = get_transactions_for_user(username=g.username)
    transactions = list(transactionsCursor)
    return render_template('transactions/all.html', transactions=transactions)
    

@bp.route('/add', methods=('POST','GET'))
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
    
    
    
    