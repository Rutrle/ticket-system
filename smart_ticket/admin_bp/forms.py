from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ConfirmUserDeactivationForm(FlaskForm):
    user_username = StringField(label="Deactivated user username", validators=[DataRequired()])
    confirm_user_deactivation = SubmitField(label="Confirm user deactivation")
