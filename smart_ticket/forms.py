from smart_ticket.models import User, Ticket
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, SubmitField, SelectField
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
    username = StringField(label = "Username",validators=[DataRequired()])
    password = PasswordField(label = "Password",validators=[DataRequired()])
    submit = SubmitField(label = 'Login')


class OpenTicketForm(FlaskForm):
    subject = StringField(label = 'Subject',validators=[DataRequired(), Length(min=5  , max=45)])
    issue_text = TextAreaField(label='Problem description', validators=[DataRequired(), Length(min=0  , max=2500)])
    submit = SubmitField(label = 'Submit ticket')

class NewTicketLogMessage(FlaskForm):
    message_text = TextAreaField(label="Update", validators=[DataRequired(), Length(min=5  , max=1500)])
    submit_new_log_ticket = SubmitField(label = 'Submit update')

class AssignTicket2Self(FlaskForm):
    assign_2_self = SubmitField(label = 'Start solving')

class UnassignTicket2Self(FlaskForm):
    unassign_from_self = SubmitField(label = 'Stop solving')

class AddToWatchlist(FlaskForm):
    add_to_watchlist = SubmitField(label = 'Add to watchlist')

class RemoveFromWatchlist(FlaskForm):
    remove_from_watchlist = SubmitField(label = 'Remove from watchlist')

class TicketFilter(FlaskForm):
    filter_by = SelectField(choices=[('all_active','All active issues'),
                                    ('user_watchlist','On my watchlist'),
                                    ('user_is_solving','Being solved by me')],
                                     label='Choose Filter')
    sort_by =SelectField(choices=[('c_time_asc','Creation time ascending \u2191'),
                                    ('c_time_desc','Creation time descending \u2193'),
                                    ('author_asc','Author ascending \u2191'),
                                    ('author_desc','Author descending \u2193'),
                                    ('subject_asc','Subject ascending \u2191'),
                                    ('subject_desc','Subject descending \u2193')],
                                    label='Sort by')
    search = SubmitField(label = "Apply")

class ArchiveTicketFilter(FlaskForm):
    filter_by = SelectField(choices=[('all_solved','All resolved issues'),
                                    ('user_watchlist','On my watchlist'),
                                    ('user_has_solved','Solved by me')],
                                     label='Choose Filter')
    sort_by =SelectField(choices=[('solve_time_asc','Time of solution ascending \u2191'),
                                    ('solve_time_desc','Time of solution descending \u2193'),
                                    ('c_time_asc','Creation time ascending \u2191'),
                                    ('c_time_desc','Creation time descending \u2193'),
                                    ('solver_asc','Solver ascending \u2191'),
                                    ('solver_desc','Solver descending \u2193'),
                                    ('author_asc','Author ascending \u2191'),
                                    ('author_desc','Author descending \u2193'),
                                    ('subject_asc','Subject ascending \u2191'),
                                    ('subject_desc','Subject descending \u2193')],
                                    label='Sort by')
    search = SubmitField(label = "Apply")