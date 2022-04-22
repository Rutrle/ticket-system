from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class ConfirmUserDeactivationForm(FlaskForm):
    user_id = StringField(label="Deactivated user id", validators=[DataRequired()])
    user_username = StringField(label="Please confirm the username of user you want to deactivate", validators=[DataRequired()])
    password = PasswordField(label="Please enter your password")
    confirm_user_deactivation = SubmitField(label="Confirm user deactivation")

class ConfirmUserReactivationForm(FlaskForm):
    user_id = StringField(label="Reactivate user id", validators=[DataRequired()])
    user_username = StringField(label="Please confirm the username of user you want to reactivate", validators=[DataRequired()])
    password = PasswordField(label="Please enter your password")
    confirm_user_reactivation = SubmitField(label="Confirm user reactivation")