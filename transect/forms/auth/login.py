from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError

from transect.domain.users import validate_user_password, does_username_exist, does_password_match_user


def has_valid_login_details(username, password):
    if not validate_user_password(username, password):
        raise ValidationError('invalid logon details.')


class LoginForm(FlaskForm):
    username = StringField('username', [validators.InputRequired()])
    password = PasswordField('password', [validators.InputRequired()])
    submit = SubmitField('login')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if not does_username_exist(self.username.data):
            self.username.errors.append('Unknown username')
            return False

        if not does_password_match_user(self.username.data, self.password.data):
            self.password.errors.append('Invalid password')
            return False

        return True
