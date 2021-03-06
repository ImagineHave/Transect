import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired


class EditForm(FlaskForm):
    account_name = StringField('account name', [InputRequired()])
    account_opened_date = DateField('start date', [InputRequired()], format='%Y-%m-%d', default=datetime.date.today())
    submit = SubmitField('edit')
