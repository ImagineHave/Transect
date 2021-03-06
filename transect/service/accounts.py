from flask import (
    Blueprint, g, redirect, render_template, url_for, session, request
)

from transect.domain.accounts import (
    insert_account, get_accounts_by_username, get_account_by_id, delete_account, update_account
)
from transect.domain import transactions
from transect.domain import series
from transect.forms.accounts.add import AddForm
from transect.forms.accounts.edit import EditForm
from transect.service.auth import login_required
from werkzeug.exceptions import abort
import copy

bp = Blueprint('accounts', __name__, url_prefix='/accounts')


@bp.route('/all')
@login_required
def all_accounts():
    accounts = list(get_accounts_by_username(g.username))
    return render_template('accounts/all.html', accounts=accounts)


@bp.route('/add', methods=('POST', 'GET'))
@login_required
def add():
    form = AddForm()

    if form.validate_on_submit():
        data = {
            'username': g.username,
            'account_name': form.account_name.data,
            'account_opened_date': form.account_opened_date.data,
        }
        insert_account(data)
        return redirect(url_for('accounts.all_accounts'))

    return render_template('accounts/add.html', form=form)


def get_account(_id):
    account = get_account_by_id(_id)

    if account is None:
        abort(404, "account doesn't exist.")

    if account.user.get_id() != session.get('user_id'):
        abort(403)

    return account


@bp.route('/<_id>/edit', methods=('POST', 'GET'))
@login_required
def edit(_id):
    account = get_account(_id)
    form = EditForm()
    '''put the transaction into the form'''
    form.process(formdata=request.form, obj=account)

    if form.validate_on_submit():

        from_data = {'username': g.username, 'payer': account.account_name}
        to_data = {'username': g.username, 'payer': form.account_name.data}
        series.bulk_update(copy.deepcopy(from_data), copy.deepcopy(to_data))
        transactions.bulk_update(copy.deepcopy(from_data), copy.deepcopy(to_data))

        from_data = {'username': g.username, 'payee': account.account_name}
        to_data = {'username': g.username, 'payee': form.account_name.data}
        series.bulk_update(copy.deepcopy(from_data), copy.deepcopy(to_data))
        transactions.bulk_update(copy.deepcopy(from_data), copy.deepcopy(to_data))

        data = {
            'username': g.username,
            'account_name': form.account_name.data,
            'account_opened_date': form.account_opened_date.data,
        }
        update_account(_id, data)
        return redirect(url_for('accounts.all_accounts'))

    return render_template('accounts/edit.html', account=account, form=form)


@bp.route('/<_id>/delete', methods=('POST',))
@login_required
def delete(_id):
    get_account(_id)
    delete_account(_id)
    return redirect(url_for('accounts.all_accounts'))
