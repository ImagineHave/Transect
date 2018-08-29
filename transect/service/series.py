from flask import (
    Blueprint, g, redirect, render_template, url_for, session, request
)

from transect.domain.series import insert_series, get_series_by_username, get_series_by_id, delete_series
from transect.forms.series.add import AddForm
from transect.forms.series.edit import EditForm
from transect.service.auth import login_required
from transect.domain.frequencies import get_by_label
from werkzeug.exceptions import abort

bp = Blueprint('series', __name__, url_prefix='/series')


def get_account(p, a):
    if p is None or len(p) == 0:
        return a
    else:
        return p


@bp.route('/add', methods=('POST', 'GET'))
@login_required
def add():
    form = AddForm()

    if form.validate_on_submit():

        insert_series(
                name=form.name.data,
                username=g.username,
                payer=get_account(form.payer.data, form.payer_account.data),
                payee=get_account(form.payee.data, form.payee_account.data),
                amount=form.amount.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                frequency=get_by_label(form.frequency.data)
        )
        return redirect(url_for('series.all_series'))

    return render_template('series/add.html', form=form)


@bp.route('/list', methods=('POST', 'GET'))
@login_required
def all_series():
    series = list(get_series_by_username(g.username))
    return render_template('series/all.html', series=series)


def get_series(_id):
    series = get_series_by_id(_id)

    if series is None:
        abort(404, "Series doesn't exist.")

    if series.user.get_id() != session.get('user_id'):
        abort(403)

    return series


@bp.route('/<_id>/edit', methods=('POST', 'GET'))
@login_required
def edit(_id):
    series = get_series(_id)
    form = EditForm()
    '''put the transaction into the form'''
    form.process(formdata=request.form, obj=series, )

    if form.validate_on_submit():

        delete_series(_id)
        insert_series(
                name=form.name.data,
                username=g.username,
                payer=get_account(form.payer.data, form.payer_account.data),
                payee=get_account(form.payee.data, form.payee_account.data),
                amount=form.amount.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                frequency=get_by_label(form.frequency.data)
        )
        return redirect(url_for('series.all_series'))

    return render_template('series/edit.html', series=series, form=form)


@bp.route('/<_id>/delete', methods=('POST',))
@login_required
def delete(_id):
    get_series(_id)
    delete_series(_id)
    return redirect(url_for('series.all_series'))
