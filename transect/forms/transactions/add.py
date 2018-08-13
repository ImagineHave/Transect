from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField
from wtforms.validators import DataRequired
import datetime

class AddForm(FlaskForm):
    payer = StringField('payer', [DataRequired()])
    payee = StringField('payee', [DataRequired()])
    amount = DecimalField('amount', [DataRequired()])
    date = DateField('date', [DataRequired()], format='%Y-%m-%d', default=datetime.date.today())
    submit = SubmitField('add')