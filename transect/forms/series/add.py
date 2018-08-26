import datetime
from decimal import ROUND_HALF_UP
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired
from transect.domain.frequencies import get_as_list_of_tuples


class AddForm(FlaskForm):
    name = StringField('series name', [InputRequired()])
    payer = StringField('payer', [InputRequired()])
    payee = StringField('payee', [InputRequired()])
    amount = DecimalField('amount', [InputRequired()], places=2, default=0.0, rounding=ROUND_HALF_UP)
    start_date = DateField('start date', [InputRequired()], format='%Y-%m-%d', default=datetime.date.today())
    end_date = DateField('end date', [InputRequired()], format='%Y-%m-%d', default=datetime.date.today())
    frequency = SelectField(label='label', choices=get_as_list_of_tuples())
    submit = SubmitField('add')
