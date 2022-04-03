from smart_ticket.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, FileField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[
                           DataRequired(), Length(min=2, max=30)])
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    password1 = PasswordField(label='Password', validators=[DataRequired()])
    password2 = PasswordField(label='Confirm password', validators=[
                              DataRequired(), EqualTo('password1', message="Passwords have to match")])
    submit = SubmitField(label='Submit')

    def validate_username(self, checked_username):
        user = User.query.filter_by(username=checked_username.data).first()
        if user:
            raise ValidationError(
                f"Username {checked_username.data} already exists! Please try different one")

    def validate_email(self, checked_email):
        email_address = User.query.filter_by(email=checked_email.data).first()
        if email_address:
            raise ValidationError(
                f"Email address {checked_email.data} already exists! Please try different one")


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label='Login')

class UserUpdateForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    phone_number = StringField(label='Phone number', validators=[Length(min=3, max=15)])
    profile_picture = FileField(label= "Profile picture")