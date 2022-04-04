from smart_ticket.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, FileField, TelField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

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

class UserContactsUpdateForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    phone_number = TelField(label='Phone number', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField(label='Update contacts')

    def validate_phone_number(self, checked_number: TelField):
        input_number = checked_number.data
        try:
            int("".join(input_number.split())) # to remove whitespaces
        except ValueError:
            raise ValidationError('Invalid phone number. You must enter a number')

        try:
            parsed_input_number = phonenumbers.parse(input_number)
            if not (phonenumbers.is_valid_number(parsed_input_number)):
                raise ValidationError('Invalid phone number. Maybe you have forgotten country prefix code?')
        except NumberParseException:
            raise ValidationError('Invalid phone number. Maybe you have forgotten country prefix code?')

class UserProfilePictureForm(FlaskForm):
    profile_picture = FileField(label= "Profile picture")
    submit = SubmitField(label='Upload new profile picture')

class UserPasswordUpdateForm(FlaskForm):
    old_password = PasswordField(label='Old password', validators=[DataRequired()])
    password1 = PasswordField(label='Password', validators=[DataRequired()])
    password2 = PasswordField(label='Confirm password', validators=[DataRequired(), EqualTo('password1', message="Passwords have to match")])
    submit = SubmitField(label='Change password')