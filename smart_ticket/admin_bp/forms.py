from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length


class ConfirmUserDeactivationForm(FlaskForm):
    """
    Form for setting user status to inactive
    """
    user_username = StringField(label="Please confirm the username of user you want to deactivate", validators=[DataRequired()])
    password = PasswordField(label="Please enter your password")
    confirm_user_deactivation = SubmitField(label="Confirm user deactivation")


class ConfirmUserReactivationForm(FlaskForm):
    """
    Form for setting user status back to active
    """
    user_username = StringField(label="Please confirm the username of user you want to reactivate", validators=[DataRequired()])
    password = PasswordField(label="Please enter your password")
    confirm_user_reactivation = SubmitField(label="Confirm user reactivation")


class ConfirmUserUpgradeForm(FlaskForm):
    """
    Form for upgrading user status to administrator
    """
    user_username = StringField(label="Please confirm the username of user you want to upgrade to administrator", validators=[DataRequired()])
    password = PasswordField(label="Please enter your password")
    confirm_user_upgrade = SubmitField(label="Confirm user upgrade to administrator")


class ConfirmUserDowngradeForm(FlaskForm):
    """
    Form for downgrading user status to standard user from administrator
    """
    user_username = StringField(label="Please confirm the username of user you want to downgrade from administrator", validators=[DataRequired()])
    password = PasswordField(label="Please enter your password")
    confirm_user_downgrade = SubmitField(label="Confirm user downgrade to standard user")


class ConfirmTicketDeletionForm(FlaskForm):
    """
    Form for deleting ticket from database
    """
    ticket_subject = StringField(label="Please confirm the subject of ticket you want to delete", validators=[DataRequired()])
    password = PasswordField(label="Please enter your password")
    confirm_ticket_deletion = SubmitField(label="Confirm ticket deletion")


class ConfirmTicketReopeningForm(FlaskForm):
    """
    Form for reopening a closed (solved) ticket
    """
    ticket_subject = StringField(label="Please confirm the subject of ticket you want to reopen", validators=[DataRequired()])
    reason_for_reopening = StringField(label="Please state reason for reopening the ticket", validators=[DataRequired(), Length(min=5, max=45)])
    password = PasswordField(label="Please enter your password")
    confirm_ticket_reopening = SubmitField(label="Confirm ticket reopening")

class UnresolvedTicketFilterForm(FlaskForm):
    """
    Form for selecting ordering of unresolved tickets
    """

    sort_by = SelectField(choices=[('c_time_asc', 'Creation time ascending \u2191'),
                                   ('c_time_desc', 'Creation time descending \u2193'),
                                   ('author_asc', 'Author ascending \u2191'),
                                   ('author_desc', 'Author descending \u2193'),
                                   ('subject_asc', 'Subject ascending \u2191'),
                                   ('subject_desc', 'Subject descending \u2193')],
                          label='Sort by')
    order = SubmitField(label="Apply")

class ResolvedTicketFilterForm(FlaskForm):
    """
    Form for selecting ordering of resolved tickets
    """
    sort_by = SelectField(choices=[('solve_time_asc', 'Time of solution ascending \u2191'),
                                   ('solve_time_desc', 'Time of solution descending \u2193'),
                                   ('c_time_asc', 'Creation time ascending \u2191'),
                                   ('c_time_desc', 'Creation time descending \u2193'),
                                   ('solver_asc', 'Solver ascending \u2191'),
                                   ('solver_desc', 'Solver descending \u2193'),
                                   ('author_asc', 'Author ascending \u2191'),
                                   ('author_desc', 'Author descending \u2193'),
                                   ('subject_asc', 'Subject ascending \u2191'),
                                   ('subject_desc', 'Subject descending \u2193')],
                          label='Sort by')
    order = SubmitField(label="Apply")