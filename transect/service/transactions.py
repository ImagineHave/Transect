import io
import csv
import pymongo

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)

from transect.domain.transactions import get_transactions_for_username, insert_transaction, \
    get_transaction_from_transaction_id, update_transaction, delete_transaction
from transect.forms.transactions.add import AddForm
from transect.forms.transactions.edit import EditForm
from werkzeug.exceptions import abort
from transect.service.auth import login_required

bp = Blueprint('transactions', __name__, url_prefix='/transactions')


# list all transactions
@bp.route('/all')
@login_required
def all_transactions():
    transactions = get_transactions_for_username(g.username)
    transactions = list(transactions.order_by('date_due'))
    return render_template('transactions/all.html', transactions=transactions)
    

@bp.route('/add', methods=('POST', 'GET'))
@login_required
def add():
    
    form = AddForm()
    
    if form.validate_on_submit():
        user_id = session.get('user_id')
        date = request.form['date']
        payer = request.form['payer']
        amount = request.form['amount']
        payee = request.form['payee']
        transaction = {"user_id": user_id, "date": date, "payer": payer, "amount": amount, "payee": payee}
        insert_transaction(transaction)
        return redirect(url_for('transactions.all_transactions'))
    
    return render_template('transactions/add.html', form=form)
    

def get_transaction(_id):
    transaction = get_transaction_from_transaction_id(_id)

    if transaction is None:
        abort(404, "Transaction doesn't exist.")

    if transaction.user.get_id() != session.get('user_id'):
        abort(403)    
        
    return transaction


@bp.route('/<_id>/edit', methods=('POST', 'GET'))
@login_required
def edit(_id):
    
    transaction = get_transaction(_id)
    form = EditForm()

    print(form.errors)
    print(form.validate_on_submit())
    print(form.date.data)

    if form.validate_on_submit():
        update_transaction(_id,
                           payer=form.payer.data,
                           payee=form.payee.data,
                           amount=form.amount.data,
                           date_due=form.date.data)
        return redirect(url_for('transactions.all_transactions'))

    data = {'payer': transaction.payer,
            'payee': transaction.payee,
            'date': transaction.date_due.strftime('%Y-%m-%d'),
            'amount': transaction.amount}

    print(data)

    return render_template('transactions/edit.html', transaction=data, form=form)
    
    
@bp.route('/<_id>/delete', methods=('POST',))
@login_required
def delete(_id):
    get_transaction(_id)
    delete_transaction(_id)
    return redirect(url_for('transactions.all_transactions'))
    

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@bp.route('/bulk', methods=('POST',))
@login_required
def bulk():
    if request.method == 'POST':
        file = request.files['bulkTransactions']
        print(file)
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        stream.seek(0)
        result = transform(stream.read())
        
    return render_template('transactions/bulk.html')
