from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired
from flask_ckeditor import CKEditorField


class OpenTicketForm(FlaskForm):
    """
    Form for creating a new ticket
    """

    subject = StringField(label='Subject', validators=[DataRequired(), Length(min=5, max=45)])
    issue_text = TextAreaField(label='Problem description', validators=[DataRequired(), Length(min=0, max=2500)])
    submit = SubmitField(label='Submit ticket')


class TicketFilterForm(FlaskForm):
    """
    Form for selecting filter and ordering of unresolved tickets
    """

    filter_by = SelectField(choices=[('all_active', 'All active issues'),
                                     ('user_watchlist', 'On my watchlist'),
                                     ('user_is_solving', 'Being solved by me')],
                            label='Choose Filter')
    sort_by = SelectField(choices=[('c_time_asc', 'Creation time ascending \u2191'),
                                   ('c_time_desc', 'Creation time descending \u2193'),
                                   ('author_asc', 'Author ascending \u2191'),
                                   ('author_desc', 'Author descending \u2193'),
                                   ('subject_asc', 'Subject ascending \u2191'),
                                   ('subject_desc', 'Subject descending \u2193')],
                          label='Sort by')
    search = SubmitField(label="Apply")



class NewTicketLogMessageForm(FlaskForm):
    """
    Form for creating new ticket log message
    """

    message_text = TextAreaField(label="Update", validators=[DataRequired(), Length(min=5, max=1500)])
    submit_new_log_ticket = SubmitField(label='Submit update')


class AssignTicket2SelfForm(FlaskForm):
    """
    Form for assigning current user as one of the current solvers of the ticket
    """

    assign_2_self = SubmitField(label='Start solving')


class UnassignTicket2SelfForm(FlaskForm):
    """
    Form for unassigning current user from current solvers of the ticket
    """

    unassign_from_self = SubmitField(label='Stop solving')


class AddToWatchlistForm(FlaskForm):
    """
    Form for adding ticket to current user watchlist
    """

    add_to_watchlist = SubmitField(label='Add to watchlist')


class RemoveFromWatchlistForm(FlaskForm):
    """
    Form for removing ticket from current user watchlist
    """

    remove_from_watchlist = SubmitField(label='Remove from watchlist')


class ArchiveTicketFilterForm(FlaskForm):
    """
    Form for selecting filter and ordering of resolved tickets in archive
    """

    filter_by = SelectField(choices=[('all_solved', 'All resolved issues'),
                                     ('user_watchlist', 'On my watchlist'),
                                     ('user_has_solved', 'Solved by me')],
                            label='Choose Filter')
    sort_by = SelectField(choices=[('solve_time_asc', 'Time of solution ascending \u2191'),
                                   ('solve_time_desc',
                                    'Time of solution descending \u2193'),
                                   ('c_time_asc', 'Creation time ascending \u2191'),
                                   ('c_time_desc', 'Creation time descending \u2193'),
                                   ('solver_asc', 'Solver ascending \u2191'),
                                   ('solver_desc', 'Solver descending \u2193'),
                                   ('author_asc', 'Author ascending \u2191'),
                                   ('author_desc', 'Author descending \u2193'),
                                   ('subject_asc', 'Subject ascending \u2191'),
                                   ('subject_desc', 'Subject descending \u2193')],
                          label='Sort by')
    search = SubmitField(label="Apply")


class ConfirmTicketSolutionForm(FlaskForm):
    """
    Form for solving ticket
    """
    solution_text = TextAreaField(label="Describe ticket solution", validators=[DataRequired(), Length(min=5, max=1500)])
    solve_ticket = SubmitField(label="Confirm Solution")
