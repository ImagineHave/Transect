from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField
from wtforms.validators import DataRequired
import datetime
from decimal import ROUND_HALF_UP

class AddForm(FlaskForm):
    payer = StringField('payer', [DataRequired()])
    payee = StringField('payee', [DataRequired()])
    amount = DecimalField('amount', [DataRequired()], places=2, default=0.0, rounding=ROUND_HALF_UP)
    date = DateField('date', [DataRequired()], format='%Y-%m-%d', default=datetime.date.today())
    submit = SubmitField('add')