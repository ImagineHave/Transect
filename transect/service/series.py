from flask import (
    Blueprint, g, redirect, render_template, url_for
)

from transect.domain.series import insert_series
from transect.forms.series.add import AddForm
from transect.service.auth import login_required

bp = Blueprint('series', __name__, url_prefix='/series')


@bp.route('/add', methods=('POST', 'GET'))
@login_required
def add():
    form = AddForm()

    if form.validate_on_submit():
        insert_series(username=g.username,
                      payer=form.payer.data,
                      payee=form.payee.data,
                      amount=form.amount.data,
                      start_date=form.date.data,
                      frequency=form.frequency.data)
        return redirect(url_for('series.add'))

    return render_template('series/add.html', form=form)
