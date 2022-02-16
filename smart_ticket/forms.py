from smart_ticket.models import User, Ticket
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, SubmitField, validators
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

class RegisterForm(FlaskForm):
    username = StringField(label = 'Username', validators=[DataRequired(), Length(min=2  , max=30)])
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    password1 = PasswordField(label = 'Password', validators=[DataRequired()])
    password2 = PasswordField(label = 'Confirm password', validators=[DataRequired(),EqualTo('password1', message="Passwords have to match")])
    submit = SubmitField(label='Submit')

    def validate_username(self, checked_username):
        user = User.query.filter_by(username = checked_username.data).first()
        if user:
            raise ValidationError(f"Username {checked_username.data} already exists! Please try different one")   


    def validate_email(self, checked_email):
        email_address = User.query.filter_by(email=checked_email.data).first()
        if email_address:
            raise ValidationError(f"Email address {checked_email.data} already exists! Please try different one")

class LoginForm(FlaskForm):
    username = StringField(label = "Username")
    password = PasswordField(label = "Password")
    submit = SubmitField(label = 'Login')


class OpenTicketForm(FlaskForm):
    subject = StringField(label = 'Subject')
    issue_text = TextAreaField(label='Problem description')
    submit = SubmitField(label = 'Submit ticket')

class NewTicketLogMessage(FlaskForm):
    message_text = TextAreaField(label="Update", validators=[DataRequired(), Length(min=5  , max=1500)])
    submit = SubmitField(label = 'Submit update')

class CloseTicketLogMessage(FlaskForm):
    message_text = TextAreaField(label="Problem solution/answer")
    submit = SubmitField(label = 'Close ticket')