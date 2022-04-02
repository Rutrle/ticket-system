from flask import Blueprint, render_template, redirect, render_template, request, flash, url_for
from smart_ticket import db
from smart_ticket.models import Ticket, TicketLogMessage, User
from smart_ticket.ticket_bp.forms import OpenTicketForm, TicketFilter, NewTicketLogMessage, AssignTicket2Self, UnassignTicket2Self, AddToWatchlist, RemoveFromWatchlist, ConfirmTicketSolution, ArchiveTicketFilter
from flask_login import current_user, login_required
from sqlalchemy.sql import text

ticket_bp = Blueprint('ticket_bp', __name__, template_folder='templates')


@ticket_bp.route('/submit', methods=['GET', 'POST'])
def create_ticket_page():
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

        flash(f"ticket submitted succesfully", category="success")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There was an error in submiting a ticket: {err_msg[0]}', category='danger')

    return render_template('ticket_bp/create_ticket.html', form=form)


@ticket_bp.route('/list', methods=['GET', 'POST'])
@login_required
def ticket_list_page():
    filter_form = TicketFilter()

    sort_dict = {'c_time_asc': 'ticket_creation_time',
                 'c_time_desc': 'ticket_creation_time desc',
                 'author_asc': 'user.username',
                 'author_desc': 'user.username desc',
                 'subject_asc': 'ticket.subject',
                 'subject_desc': 'ticket.subject desc',
                 }
    order_by_text = sort_dict['c_time_asc']

    if request.method == 'GET':
        shown_tickets = db.session.query(Ticket).filter(
            Ticket.is_solved == False).outerjoin(Ticket.author).order_by(text(order_by_text))

    if filter_form.validate_on_submit():
        order_by_text = sort_dict[filter_form.sort_by.data]
        if filter_form.filter_by.data == 'all_active':
            shown_tickets = db.session.query(Ticket).filter(Ticket.is_solved == False)\
                .outerjoin(Ticket.author).order_by(text(order_by_text))

        elif filter_form.filter_by.data == 'user_watchlist':
            shown_tickets = db.session.query(Ticket).filter(Ticket.is_solved == False, Ticket.currently_on_watchlist.contains(current_user))\
                .outerjoin(Ticket.author).order_by(text(order_by_text))

        elif filter_form.filter_by.data == 'user_is_solving':
            shown_tickets = db.session.query(Ticket).filter(Ticket.is_solved == False, Ticket.current_solvers.contains(current_user))\
                .outerjoin(Ticket.author).order_by(text(order_by_text))

    return render_template('ticket_bp/ticket_list.html', tickets=shown_tickets, filter_form=filter_form)


@ticket_bp.route('/<int:current_ticket_id>')
@login_required
def ticket_detail_page(current_ticket_id: int):

    ticket = Ticket.query.get_or_404(current_ticket_id)
    msg_log = TicketLogMessage.query.filter_by(
        ticket_id=ticket.id).order_by(TicketLogMessage.creation_time)
    currently_solving_users = User.query.filter(
        User.currently_solving.any(id=current_ticket_id)).all()

    new_log_msg_form = NewTicketLogMessage()
    assign_2_self_form = AssignTicket2Self()
    unassign_from_self_form = UnassignTicket2Self()
    add_to_watchlist_form = AddToWatchlist()
    remove_from_watchlist_form = RemoveFromWatchlist()
    confirm_solution_form = ConfirmTicketSolution()

    return render_template('ticket_bp/ticket_detail.html', ticket=ticket, msg_log=msg_log, form=new_log_msg_form, assign_2_self_form=assign_2_self_form, unassign_from_self_form=unassign_from_self_form, currently_solving_users=currently_solving_users, add_to_watchlist_form=add_to_watchlist_form, remove_from_watchlist_form=remove_from_watchlist_form, confirm_solution_form=confirm_solution_form)


@ticket_bp.route('/<int:current_ticket_id>/submit_new_log_ticket', methods=['POST'])
@login_required
def submit_new_log_ticket(current_ticket_id: int):
    new_log_msg_form = NewTicketLogMessage()

    if new_log_msg_form.validate_on_submit():

        new_log_message = TicketLogMessage(
            author_id=current_user.id,
            ticket_id=current_ticket_id,
            message_text=new_log_msg_form.message_text.data,
            message_category="update"
        )

        db.session.add(new_log_message)
        db.session.commit()

    return redirect(url_for('ticket_bp.ticket_detail_page', current_ticket_id=current_ticket_id))


@ticket_bp.route('/<int:current_ticket_id>/unassign_from_self', methods=['POST'])
@login_required
def unassign_from_self(current_ticket_id: int):
    unassign_from_self_form = UnassignTicket2Self()
    ticket = Ticket.query.get_or_404(current_ticket_id)

    if unassign_from_self_form.validate_on_submit():
        if current_user not in ticket.current_solvers:
            flash(
                f'You are not assigned to ticket {ticket.subject}', category='danger')
        else:
            ticket.current_solvers.remove(current_user)
            new_log_message = TicketLogMessage(
                author_id=current_user.id,
                ticket_id=current_ticket_id,
                message_text=f'User {current_user.username} is no longer solving this issue',
                message_category="sys_message"
            )
            db.session.add(new_log_message)
            db.session.add(ticket)
            db.session.commit()

            flash(f'You are no longer assigned to ticket {ticket.subject}', category='warning')

    return redirect(url_for('ticket_bp.ticket_detail_page', current_ticket_id=current_ticket_id))


@ticket_bp.route('/<int:current_ticket_id>/assign_2_self', methods=['POST'])
@login_required
def assign_2_self(current_ticket_id: int):
    assign_2_self_form = AssignTicket2Self()
    ticket = Ticket.query.get_or_404(current_ticket_id)
    if assign_2_self_form.validate_on_submit():
        if current_user in ticket.current_solvers:
                flash(f'You are already assigned to ticket {ticket.subject}', category='warning')

        else:
                ticket.current_solvers.append(current_user)
                new_log_message = TicketLogMessage(
                    author_id=current_user.id,
                    ticket_id=current_ticket_id,
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

    return redirect(url_for('ticket_bp.ticket_detail_page', current_ticket_id=current_ticket_id))


@ticket_bp.route('/<int:current_ticket_id>/solve', methods=['POST'])
@login_required
def solve_ticket(current_ticket_id: int):
    confirm_solution_form = ConfirmTicketSolution()
    print(confirm_solution_form.data)
    if confirm_solution_form.validate():
        ticket_to_solve = Ticket.query.get_or_404(current_ticket_id)

        if ticket_to_solve.is_solved == False:
            ticket_to_solve.solve_ticket(
                current_user, confirm_solution_form.solution_text.data)
            flash(f"{ticket_to_solve} solved!", category='success')

        else:
            flash(f"{ticket_to_solve}  is already solved!", category='danger')

    return redirect(url_for('ticket_bp.ticket_detail_page', current_ticket_id=current_ticket_id))


@ticket_bp.route('/<int:current_ticket_id>/add_2_watchlist', methods=['POST'])
@login_required
def add_to_watchlist(current_ticket_id: int):
    user = current_user
    ticket = Ticket.query.get_or_404(current_ticket_id)

    if ticket not in user.current_watchlist:
        user.current_watchlist.append(ticket)
        db.session.add(user)
        db.session.commit()

        flash(f"{ticket} was added to your watchlist", category='success')
    else:
        flash(f"{ticket} is already on your watchlist", category='danger')

    return redirect(url_for('ticket_bp.ticket_detail_page', current_ticket_id=current_ticket_id))


@ticket_bp.route('/<int:current_ticket_id>/remove_from_watchlist', methods=['POST'])
@login_required
def remove_from_watchlist(current_ticket_id: int):
    user = current_user
    ticket = Ticket.query.get_or_404(current_ticket_id)
    if ticket in user.current_watchlist:
        user.current_watchlist.remove(ticket)
        db.session.add(user)
        db.session.commit()

        flash(f"{ticket} was removed from your watchlist", category='warning')
    else:
        flash(
            f"{ticket} is not on your watchlist, it can't be removed from it", category='danger')
    return redirect(url_for('ticket_bp.ticket_detail_page', current_ticket_id=current_ticket_id))


@ticket_bp.route('/archive', methods=['GET', 'POST'])
@login_required
def archive_page():
    filter_form = ArchiveTicketFilter()

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

    if filter_form.sort_by.data == 'solver_asc' or filter_form.sort_by.data == 'solver_desc':
        user_to_outerjoin = Ticket.solver
    else:
        user_to_outerjoin = Ticket.author

    if request.method == 'GET':
        order_by_text = sort_dict['solve_time_asc']
        tickets = db.session.query(Ticket).filter(Ticket.is_solved == True).outerjoin(
            user_to_outerjoin).order_by(text(order_by_text))

    if filter_form.validate_on_submit():
        order_by_text = sort_dict[filter_form.sort_by.data]

        if filter_form.filter_by.data == 'all_solved':
            tickets = db.session.query(Ticket).filter(Ticket.is_solved == True)\
                .outerjoin(user_to_outerjoin).order_by(text(order_by_text))

        elif filter_form.filter_by.data == 'user_watchlist':
            tickets = db.session.query(Ticket).filter(Ticket.is_solved == True, Ticket.currently_on_watchlist.contains(current_user))\
                .outerjoin(user_to_outerjoin).order_by(text(order_by_text))

        elif filter_form.filter_by.data == 'user_has_solved':
            tickets = db.session.query(Ticket).filter(Ticket.is_solved == True, Ticket.solver == current_user)\
                .outerjoin(user_to_outerjoin).order_by(text(order_by_text))

    return render_template('ticket_bp/archive.html', tickets=tickets, form=filter_form)
