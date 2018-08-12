from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    email = StringField('email', [DataRequired("email address required."), Email("email address required.")])
    username = StringField('username', validators=[DataRequired("username required.")])
    password = PasswordField('password', [
        DataRequired("password required."),
        EqualTo('confirm', message='passwords must match.')
    ])
    confirm = PasswordField('confirm password')
    submit = SubmitField('register')