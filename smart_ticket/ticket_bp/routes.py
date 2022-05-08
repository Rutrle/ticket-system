from flask import Blueprint, Response, Markup, render_template, redirect, render_template, request, flash, url_for
from smart_ticket import db
from smart_ticket.email.send_email import send_ticket_solved_email, send_ticket_updated_email
from smart_ticket.models import Ticket, TicketLogMessage, User
from smart_ticket.ticket_bp.forms import OpenTicketForm, TicketFilterForm, NewTicketLogMessageForm, AssignTicket2SelfForm, UnassignTicket2SelfForm, AddToWatchlistForm, RemoveFromWatchlistForm, ConfirmTicketSolutionForm, ArchiveTicketFilterForm
from flask_login import current_user, login_required
from sqlalchemy.sql import text

ticket_bp = Blueprint('ticket_bp', __name__, template_folder='templates')


@ticket_bp.route('/submit', methods=['GET', 'POST'])
def create_ticket_page() -> Response:
    """
    Page for creating new Tickets
    """
    form = OpenTicketForm()

    if form.validate_on_submit():
        new_ticket = Ticket(
            subject=form.subject.data.capitalize(),
            issue_description=form.issue_text.data,
        )

        if current_user.is_authenticated:
            new_ticket.author_id = current_user.id

        db.session.add(new_ticket)
        db.session.commit()
        creation_log_msg = TicketLogMessage(
            ticket_id=new_ticket.id, message_text="Ticket opened", message_category="sys_message")

        db.session.add(creation_log_msg)
        db.session.commit()

        flash(Markup(f"ticket submitted succesfully, you can check it here:\
             <a href='{url_for('ticket_bp.ticket_detail_page', ticket_id =new_ticket.id)}'>{new_ticket}</a>"), category="success")

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error in submiting a ticket: {err_msg[0]}', category='danger')

    return render_template('ticket_bp/create_ticket.html', form=form)


@ticket_bp.route('/list', methods=['GET', 'POST'])
@login_required
def ticket_list_page() -> Response:
    """
    Page for displaying unresolved tickets with different possiblities for filtering and ordering them
    """
    filter_form = TicketFilterForm()

    page = request.args.get('page', 1, type=int)
    tickets_per_page = 5

    sort_dict = {'c_time_asc': 'ticket_creation_time',
                 'c_time_desc': 'ticket_creation_time desc',
                 'author_asc': 'user.username',
                 'author_desc': 'user.username desc',
                 'subject_asc': 'ticket.subject',
                 'subject_desc': 'ticket.subject desc',
                 }

    if filter_form.validate_on_submit():
        page = 1 #to prevent 404 when not enough data is present
        filter = filter_form.filter_by.data
        order = filter_form.sort_by.data
    else:
        filter = request.args.get('sort_by', default=None, type=str)
        order = request.args.get('order_by', default=None, type=str)
        if filter is None:
            filter = 'all_active'
            order = 'c_time_asc'

    order_by_text = sort_dict[order]

    if filter == 'all_active':
        shown_tickets = db.session.query(Ticket).filter(Ticket.is_solved == False)\
            .outerjoin(Ticket.author).order_by(text(order_by_text)).paginate(page=page, per_page=tickets_per_page)

    elif filter == 'user_watchlist':
        shown_tickets = db.session.query(Ticket).filter(Ticket.is_solved == False, Ticket.currently_on_watchlist.contains(current_user))\
            .outerjoin(Ticket.author).order_by(text(order_by_text)).paginate(page=page, per_page=tickets_per_page)

    elif filter == 'user_is_solving':
        shown_tickets = db.session.query(Ticket).filter(Ticket.is_solved == False, Ticket.current_solvers.contains(current_user))\
            .outerjoin(Ticket.author).order_by(text(order_by_text)).paginate(page=page, per_page=tickets_per_page)

    return render_template('ticket_bp/ticket_list.html', tickets=shown_tickets, filter_form=filter_form, order=order, filter=filter)


@ticket_bp.route('/<int:ticket_id>')
@login_required
def ticket_detail_page(ticket_id: int) -> Response:
    """
    Page for displaying details about given ticket
    """

    ticket = Ticket.query.get_or_404(ticket_id)
    msg_log = TicketLogMessage.query.filter_by(
        ticket_id=ticket.id).order_by(TicketLogMessage.creation_time)
    currently_solving_users = User.query.filter(
        User.currently_solving.any(id=ticket_id)).all()

    forms ={
        'new_log_msg_form' : NewTicketLogMessageForm(),
        'assign_2_self_form' : AssignTicket2SelfForm(),
        'unassign_from_self_form' : UnassignTicket2SelfForm(),
        'add_to_watchlist_form' : AddToWatchlistForm(),
        'remove_from_watchlist_form' : RemoveFromWatchlistForm(),
        'confirm_solution_form' : ConfirmTicketSolutionForm()
    }

    return render_template('ticket_bp/ticket_detail.html', ticket=ticket, msg_log=msg_log, currently_solving_users=currently_solving_users, **forms)


@ticket_bp.route('/<int:ticket_id>/submit_new_log_ticket', methods=['POST'])
@login_required
def submit_new_log_ticket(ticket_id: int) -> Response:
    """
    route for handling POST request for creating a new message in log of given ticket, informing 
    interested users about it by e-mail and then redirecting user back to ticket_detail_page
    """
    new_log_msg_form = NewTicketLogMessageForm()

    if new_log_msg_form.validate_on_submit():
        update_text = new_log_msg_form.message_text.data

        new_log_message = TicketLogMessage(
            author_id=current_user.id,
            ticket_id=ticket_id,
            message_text=update_text,
            message_category="update"
        )

        ticket = Ticket.query.get_or_404(ticket_id)
        currently_solving_users = User.query.filter(User.currently_solving.any(id=ticket_id)).all()
        currently_on_watchlist = User.query.filter(User.current_watchlist.any(id=ticket_id)).all()
        interested_users = set(currently_solving_users + currently_on_watchlist)

        db.session.add(new_log_message)
        db.session.commit()

        for user in interested_users:
            send_ticket_updated_email(user.email, ticket, current_user.username, current_user.id, update_text)

    return redirect(url_for('ticket_bp.ticket_detail_page', ticket_id=ticket_id))


@ticket_bp.route('/<int:ticket_id>/unassign_from_self', methods=['POST'])
@login_required
def unassign_from_self(ticket_id: int) -> Response:
    """
    route for handling POST request for removing current user from current solvers
    of given ticket and then redirecting him back to ticket_detail_page
    """
    unassign_from_self_form = UnassignTicket2SelfForm()
    ticket = Ticket.query.get_or_404(ticket_id)

    if unassign_from_self_form.validate_on_submit():
        if current_user not in ticket.current_solvers:
            flash(f'You are not assigned to ticket {ticket.subject}', category='danger')
        else:
            ticket.current_solvers.remove(current_user)
            new_log_message = TicketLogMessage(
                author_id=current_user.id,
                ticket_id=ticket_id,
                message_text=f'User {current_user.username} is no longer solving this issue',
                message_category="sys_message"
            )
            db.session.add(new_log_message)
            db.session.add(ticket)
            db.session.commit()

            flash(f'You are no longer assigned to ticket {ticket.subject}', category='warning')

    return redirect(url_for('ticket_bp.ticket_detail_page', ticket_id=ticket_id))


@ticket_bp.route('/<int:ticket_id>/assign_2_self', methods=['POST'])
@login_required
def assign_2_self(ticket_id: int) -> Response:
    """
    route for handling POST request for assigning current user as one of the current solvers
    of given ticket and then redirecting him back to ticket_detail_page
    """
    assign_2_self_form = AssignTicket2SelfForm()
    ticket = Ticket.query.get_or_404(ticket_id)
    if assign_2_self_form.validate_on_submit():
        if current_user in ticket.current_solvers:
            flash(
                f'You are already assigned to ticket {ticket.subject}', category='warning')

        else:
            ticket.current_solvers.append(current_user)
            new_log_message = TicketLogMessage(
                author_id=current_user.id,
                ticket_id=ticket_id,
                message_text=f'User {current_user.username} started solving this issue',
                message_category="sys_message"
            )

            db.session.add(new_log_message)
            db.session.add(ticket)
            db.session.commit()

            flash(f'You have been succesfully assigned to ticket {ticket.subject}', category='success')

        if assign_2_self_form.errors != {}:
            for err_msg in assign_2_self_form.errors.values():
                flash(f'There was an error: {err_msg[0]}', category='danger')

    return redirect(url_for('ticket_bp.ticket_detail_page', ticket_id=ticket_id))


def solve_ticket(ticket_id: int, solution_text: str) -> None:
    """
    Sets ticket of 'ticket_id' status to solved, current user as its solver and informs interested users about it by e-mail
    """
    ticket_to_solve = Ticket.query.get_or_404(ticket_id)

    if ticket_to_solve.is_solved == False:

        currently_solving_users = User.query.filter(User.currently_solving.any(id=ticket_id)).all()
        currently_on_watchlist = User.query.filter(User.current_watchlist.any(id=ticket_id)).all()
        interested_users = set(currently_solving_users + currently_on_watchlist)

        ticket_to_solve.solve_ticket(current_user, solution_text)

        for user in interested_users:
            send_ticket_solved_email(user.email, ticket_to_solve, current_user.username, current_user.id, solution_text)

        flash(f"{ticket_to_solve} solved!", category='success')

    else:
        flash(f"{ticket_to_solve}  is already solved!", category='danger')


@ticket_bp.route('/<int:ticket_id>/solve', methods=['POST'])
@login_required
def solve_ticket_page(ticket_id: int) -> Response:
    """
    route for setting status of ticket of given 'ticket_id' to solved and
    then redirecting user back to ticket_detail_page
    """
    confirm_solution_form = ConfirmTicketSolutionForm()

    if confirm_solution_form.validate():
        solve_ticket(ticket_id, confirm_solution_form.solution_text.data)

    return redirect(url_for('ticket_bp.ticket_detail_page', ticket_id=ticket_id))


@ticket_bp.route('/<int:ticket_id>/add_2_watchlist', methods=['POST'])
@login_required
def add_to_watchlist(ticket_id: int) -> Response:
    """
    route for handling POST requests for adding ticket of 'ticket_id' to current user watchlist
    and then redirecting him back to ticket_detail_page
    """
    user = current_user
    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket not in user.current_watchlist:
        user.current_watchlist.append(ticket)
        db.session.add(user)
        db.session.commit()

        flash(f"{ticket} was added to your watchlist", category='success')
    else:
        flash(f"{ticket} is already on your watchlist", category='danger')

    return redirect(url_for('ticket_bp.ticket_detail_page', ticket_id=ticket_id))


@ticket_bp.route('/<int:ticket_id>/remove_from_watchlist', methods=['POST'])
@login_required
def remove_from_watchlist(ticket_id: int) -> Response:
    """
    route for handling POST requests for removing ticket of 'ticket_id' from current user watchlist
    and then redirecting him back to ticket_detail_page
    """
    user = current_user
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket in user.current_watchlist:
        user.current_watchlist.remove(ticket)
        db.session.add(user)
        db.session.commit()

        flash(f"{ticket} was removed from your watchlist", category='warning')
    else:
        flash(
            f"{ticket} is not on your watchlist, it can't be removed from it", category='danger')
    return redirect(url_for('ticket_bp.ticket_detail_page', ticket_id=ticket_id))


@ticket_bp.route('/archive', methods=['GET', 'POST'])
@login_required
def archive_page() -> Response:
    """
    Page for displaying resolved tickets with different possiblities for filtering and ordering them
    """
    filter_form = ArchiveTicketFilterForm()
    page = request.args.get('page', 1, type=int)
    tickets_per_page = 5

    sort_dict = {'solve_time_asc': 'ticket_solved_on',
                 'solve_time_desc': 'ticket_solved_on desc',
                 'solver_asc': 'user.username',
                 'solver_desc': 'user.username desc',
                 'c_time_asc': 'ticket_creation_time',
                 'c_time_desc': 'ticket_creation_time desc',
                 'author_asc': 'user.username',
                 'author_desc': 'user.username desc',
                 'subject_asc': 'ticket.subject',
                 'subject_desc': 'ticket.subject desc',
                 }

    if filter_form.validate_on_submit():
        page = 1 #to prevent 404 when not enough data is present
        filter = filter_form.filter_by.data
        order = filter_form.sort_by.data
    else:
        filter = request.args.get('sort_by', default=None, type=str)
        order = request.args.get('order_by', default=None, type=str)
        if filter is None:
            filter = 'all_solved'
            order = 'solve_time_asc'

    order_by_text = sort_dict[order]

    if order == 'solver_asc' or order == 'solver_desc':
        user_to_outerjoin = Ticket.solver
    else:
        user_to_outerjoin = Ticket.author

    if filter == 'all_solved':
        tickets = db.session.query(Ticket).filter(Ticket.is_solved == True)\
            .outerjoin(user_to_outerjoin).order_by(text(order_by_text)).paginate(page=page, per_page=tickets_per_page)

    elif filter == 'user_watchlist':
        tickets = db.session.query(Ticket).filter(Ticket.is_solved == True, Ticket.currently_on_watchlist.contains(current_user))\
            .outerjoin(user_to_outerjoin).order_by(text(order_by_text)).paginate(page=page, per_page=tickets_per_page)

    elif filter == 'user_has_solved':
        tickets = db.session.query(Ticket).filter(Ticket.is_solved == True, Ticket.solver == current_user)\
            .outerjoin(user_to_outerjoin).order_by(text(order_by_text)).paginate(page=page, per_page=tickets_per_page)

    return render_template('ticket_bp/archive.html', tickets=tickets, form=filter_form, filter=filter, order=order)
