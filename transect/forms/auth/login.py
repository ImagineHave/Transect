from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators

class LoginForm(FlaskForm):
    username = StringField('username', [validators.InputRequired()])
    password = PasswordField('password', [validators.InputRequired()])
    submit = SubmitField('login')