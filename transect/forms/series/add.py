import datetime
from decimal import ROUND_HALF_UP
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, DateTimeField, SelectField
from wtforms.validators import InputRequired
from transect.domain.frequencies import get_list


class AddForm(FlaskForm):
    payer = StringField('payer', [InputRequired()])
    payee = StringField('payee', [InputRequired()])
    amount = DecimalField('amount', [InputRequired()], places=2, default=0.0, rounding=ROUND_HALF_UP)
    start_date = DateTimeField('date', [InputRequired()], format='%Y-%m-%d', default=datetime.date.today())
    end_date = DateTimeField('date', [InputRequired()], format='%Y-%m-%d', default=datetime.date.today())
    frequency = SelectField(label='label', choices=get_list())
    submit = SubmitField('add')
