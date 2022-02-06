from smart_ticket.models import User, Ticket
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, SubmitField, validators

class RegisterForm(FlaskForm):
    username = StringField(label = 'Username')
    email = EmailField(label='Email')
    password1 = PasswordField(label = 'Password')
    password2 = PasswordField(label = 'Confirm password')
    submit = SubmitField(label='Submit')