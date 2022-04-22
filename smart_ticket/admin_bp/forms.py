from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class ConfirmUserDeactivationForm(FlaskForm):
    user_username = StringField(label="Please confirm the username of user you want to deactivate", validators=[DataRequired()])
    password = PasswordField(label="Please enter your password")
    confirm_user_deactivation = SubmitField(label="Confirm user deactivation")

class ConfirmUserReactivationForm(FlaskForm):
    user_username = StringField(label="Please confirm the username of user you want to reactivate", validators=[DataRequired()])
    password = PasswordField(label="Please enter your password")
    confirm_user_reactivation = SubmitField(label="Confirm user reactivation")

class ConfirmTicketDeletionForm(FlaskForm):
    ticket_subject = StringField(label="Please confirm the subject of ticket you want to delete", validators=[DataRequired()])
    password = PasswordField(label="Please enter your password")
    confirm_ticket_deletion = SubmitField(label="Confirm ticket deletion")