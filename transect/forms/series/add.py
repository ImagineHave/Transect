import datetime
from decimal import ROUND_HALF_UP
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired
from transect.domain.frequencies import get_as_list_of_tuples
from transect.domain.accounts import get_accounts_as_list_of_tuples


def has_payer(form, field):
    if len(form.payer_account.data) == 0 and len(field.payer.data) == 0:
        raise ValidationError('payer required.')


def has_payee(form, field):
    if len(form.payee_account.data) == 0 and len(field.payee.data) == 0:
        raise ValidationError('payee required.')


class AddForm(FlaskForm):
    name = StringField('series name', [InputRequired()])
    payer = StringField('payer')
    payer_account = SelectField(label='pay from account', choices=get_accounts_as_list_of_tuples(), default='other')
    payee = StringField('payee')
    payee_account = SelectField(label='pay to account', choices=get_accounts_as_list_of_tuples(), default='other')
    amount = DecimalField('amount', [InputRequired()], places=2, default=0.0, rounding=ROUND_HALF_UP)
    start_date = DateField('start date', [InputRequired()], format='%Y-%m-%d', default=datetime.date.today())
    end_date = DateField('end date', [InputRequired()], format='%Y-%m-%d', default=datetime.date.today())
    frequency = SelectField(label='frequency', choices=get_as_list_of_tuples())
    submit = SubmitField('add')
