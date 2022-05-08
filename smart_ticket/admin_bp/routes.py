from flask import Blueprint, Response, render_template, redirect, flash, url_for, request
from smart_ticket import db
from smart_ticket.models import User, Ticket, TicketLogMessage, UserRole, admin_required
from flask_login import current_user, login_required
from smart_ticket.admin_bp.forms import ConfirmUserDeactivationForm, ConfirmUserReactivationForm, ConfirmTicketDeletionForm, ConfirmTicketReopeningForm, ConfirmUserUpgradeForm, ConfirmUserDowngradeForm, ResolvedTicketFilterForm, UnresolvedTicketFilterForm
from smart_ticket.ticket_bp.routes import solve_ticket
from smart_ticket.ticket_bp.forms import ConfirmTicketSolutionForm
from smart_ticket.email.send_email import send_deactivation_email, send_reactivation_email, send_ticket_reopened_email, send_upgrade_to_administrator_email, send_downgrade_to_user_email
from sqlalchemy.sql import text

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')


@admin_bp.route('', methods=['GET'])
@login_required
@admin_required
def admin_page() -> Response:
    """
    Simple page with links to different administrator tools
    """
    return render_template("admin_bp/administrator_tools.html")


@admin_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def user_administration_page() -> Response:
    '''
    Page for displaying all users and allowing to activate/deactivate them and allowing
    changing their user role between administrator and standard user
    '''
    active_users_page = request.args.get('active_users_page', 1, type=int)
    inactive_users_page = request.args.get('inactive_users_page', 1, type=int)

    active_users = db.session.query(User).filter(User.is_active == True).order_by(
        'creation_time').paginate(page=active_users_page, per_page=5)
    inactive_users = db.session.query(User).filter(User.is_active == False).order_by(
        'creation_time').paginate(page=inactive_users_page, per_page=5)

    forms = {'user_deactivation_form': ConfirmUserDeactivationForm(),
             'user_reactivation_form': ConfirmUserReactivationForm(),
             'user_upgrade_form': ConfirmUserUpgradeForm(),
             'user_downgrade_form': ConfirmUserDowngradeForm()
             }

    return render_template("admin_bp/user_administration.html", active_users=active_users, inactive_users=inactive_users, **forms)


def deactivate_user(user: User) -> None:
    """
    deactivate user account of given 'user'
    """
    user.is_active = False
    user.currently_solving.clear()
    db.session.add(user)
    db.session.commit()


def reactivate_user(user: User) -> None:
    """
    activate user account of given 'user'
    """
    user.is_active = True
    db.session.add(user)
    db.session.commit()


@admin_bp.route('/users/<int:user_id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate_user_page(user_id: int) -> Response:
    """
    route for handling POST requests for deactivating users of given 'user_id'
    """
    user_deactivation_form = ConfirmUserDeactivationForm()

    if user_deactivation_form.validate_on_submit():

        user_to_deactivate = User.query.filter_by(id=user_id).first()

        password_correct = current_user.check_attempted_password(user_deactivation_form.password.data)
        user_username_correct = user_to_deactivate.username == user_deactivation_form.user_username.data

        if user_to_deactivate == current_user:
            flash(f"You can't deactivate your own account! Ask different administrator if you want to really do it", category="danger")
        elif password_correct and user_username_correct:
            deactivate_user(user_to_deactivate)
            send_deactivation_email(user_to_deactivate.email, user_to_deactivate.username)
            flash(f"Account of user {user_to_deactivate.username} was succesfully deactivated!", category="success")

        else:
            flash(f'There was an error with deactivating a user {user_to_deactivate.username},\
                please check if you entered valid username and password', category='danger')

    elif user_deactivation_form.errors != {}:
        for err_msg in user_deactivation_form.errors.values():
            flash(
                f'There was an error with deactivating a user: {err_msg[0]}', category='danger')
    return redirect(url_for("admin_bp.user_administration_page"))


@admin_bp.route('/users/<int:user_id>/reactivate', methods=['POST'])
@login_required
@admin_required
def reactivate_user_page(user_id: int) -> Response:
    """
    route for handling POST requests for reactivating account of user of given 'user_id'
    """
    user_reactivation_form = ConfirmUserReactivationForm()

    if user_reactivation_form.validate_on_submit():
        user_to_reactivate = User.query.filter_by(id=user_id).first()

        password_correct = current_user.check_attempted_password(user_reactivation_form.password.data)
        user_username_correct = user_to_reactivate.username == user_reactivation_form.user_username.data

        if password_correct and user_username_correct:
            reactivate_user(user_to_reactivate)
            send_reactivation_email(user_to_reactivate.email, user_to_reactivate.username)

            flash(f"Account of user {user_to_reactivate.username} was succesfully reactivated!", category="success")

        else:
            flash(f'There was an error with reactivating a user {user_to_reactivate.username},\
                please check if you entered valid username and password', category='danger')

    elif user_reactivation_form.errors != {}:
        for err_msg in user_reactivation_form.errors.values():
            flash(f'There was an error with reactivating a user: {err_msg[0]}', category='danger')

    return redirect(url_for("admin_bp.user_administration_page"))


def set_role_to_administrator(user: User) -> None:
    """
    sets given 'user' user role to administrator 
    """
    administrator_role = UserRole.query.filter_by(name="admin").first()
    user.user_role = administrator_role
    db.session.add(user)
    db.session.commit()


@admin_bp.route('/users/<int:user_id>/upgrade', methods=['POST'])
@login_required
@admin_required
def upgrade_to_administrator_page(user_id: int) -> Response:
    """
    route for handling POST request for upgrading user of 'user_id' user role to administrator
    """
    user_upgrade_form = ConfirmUserUpgradeForm()

    if user_upgrade_form.validate_on_submit():
        user_to_upgrade = User.query.filter_by(id=user_id).first()
        password_correct = current_user.check_attempted_password(user_upgrade_form.password.data)
        user_username_correct = user_to_upgrade.username == user_upgrade_form.user_username.data
        if password_correct and user_username_correct:

            set_role_to_administrator(user_to_upgrade)
            send_upgrade_to_administrator_email(user_to_upgrade.email, user_to_upgrade.username)
            flash(f"Account of user {user_to_upgrade.username} was succesfully upgraded to administrator!", category="success")
        else:
            flash(f'Either your password or upgraded user username was incorrect', category='danger')

    elif user_upgrade_form.errors != {}:
        for err_msg in user_upgrade_form.errors.values():
            flash(f'There was an error with upgrading user to administrator: {err_msg[0]}', category='danger')

    return redirect(url_for("admin_bp.user_administration_page"))


def set_role_to_user(user: User) -> None:
    """
    sets 'user' user role to standard user
    """
    user_role = UserRole.query.filter_by(name="user").first()
    user.user_role = user_role
    db.session.add(user)
    db.session.commit()


@admin_bp.route('/users/<int:user_id>/downgrade', methods=['POST'])
@login_required
@admin_required
def downgrade_to_user_page(user_id: int) -> Response:
    """
    route for handling POST request for downgrading user of 'user_id' role to standard user
    """
    user_downgrade_form = ConfirmUserDowngradeForm()

    if user_downgrade_form.validate_on_submit():
        user_to_downgrade = User.query.filter_by(id=user_id).first()
        password_correct = current_user.check_attempted_password(
            user_downgrade_form.password.data)
        user_username_correct = user_to_downgrade.username == user_downgrade_form.user_username.data

        if user_to_downgrade == current_user:
            flash(f"You can't revoke your own admin rights! Ask different administrator if you want to really do it", category="danger")
        elif password_correct and user_username_correct:

            set_role_to_user(user_to_downgrade)
            send_downgrade_to_user_email(
                user_to_downgrade.email, user_to_downgrade.username)
            flash(
                f"Account of user {user_to_downgrade.username} was succesfully downgraded to standard user!", category="success")
        else:
            flash(
                f'Either your password or downgraded user username was incorrect', category='danger')

    elif user_downgrade_form.errors != {}:
        for err_msg in user_downgrade_form.errors.values():
            flash(
                f'There was an error with downgrading user to standard user: {err_msg[0]}', category='danger')

    return redirect(url_for("admin_bp.user_administration_page"))


@admin_bp.route('/tickets', methods=['GET', 'POST'])
@login_required
@admin_required
def ticket_administration_page() -> Response:
    """
    Page for displaying all tickets and allowing to solve, reopen or completely delete them.    
    """
    unresolved_tickets_page = request.args.get('unresolved_page', 1, type=int)
    resolved_tickets_page = request.args.get('resolved_page', 1, type=int)
    tickets_per_page = 5

    order_unresolved_ticket_form = UnresolvedTicketFilterForm()
    order_resolved_ticket_form = ResolvedTicketFilterForm()

    forms = {
        'confirm_solution_form': ConfirmTicketSolutionForm(),
        'ticket_deletion_form': ConfirmTicketDeletionForm(),
        'ticket_reopening_form': ConfirmTicketReopeningForm()
    }

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

    if order_unresolved_ticket_form.validate_on_submit():
        unresolved_tickets_page = 1 #to prevent 404 when not enough data is present
        order_unresolved = order_unresolved_ticket_form.sort_by.data
        order_resolved = request.args.get('order_resolved', default=None, type=str)

    elif order_resolved_ticket_form.validate_on_submit():
        resolved_tickets_page = 1 #to prevent 404 when not enough data is present
        order_unresolved = request.args.get('order_unresolved', default=None, type=str)
        order_resolved = order_resolved_ticket_form.sort_by.data

    else:
        order_resolved = request.args.get('order_resolved', default=None, type=str)
        order_unresolved = request.args.get('order_unresolved', default=None, type=str)

    if order_resolved is None:
        order_resolved = 'c_time_asc'

    if order_unresolved is None:
        order_unresolved = 'c_time_asc'

    order_resolved_by_text = sort_dict[order_resolved]
    order_unresolved_by_text = sort_dict[order_unresolved]

    if order_resolved == 'solver_asc' or order_resolved == 'solver_desc':
        user_to_outerjoin = Ticket.solver
    else:
        user_to_outerjoin = Ticket.author  

    resolved_tickets = db.session.query(Ticket).filter(Ticket.is_solved == True)\
                .outerjoin(user_to_outerjoin).order_by(text(order_resolved_by_text)).paginate(page=resolved_tickets_page, per_page=tickets_per_page)
    
    unresolved_tickets = db.session.query(Ticket).filter(Ticket.is_solved == False)\
            .outerjoin(Ticket.author).order_by(text(order_unresolved_by_text)).paginate(page=unresolved_tickets_page, per_page=tickets_per_page)    
    
    return render_template("admin_bp/ticket_administration.html", unresolved_tickets=unresolved_tickets, resolved_tickets=resolved_tickets, **forms, order_resolved_ticket_form=order_resolved_ticket_form, order_unresolved_ticket_form=order_unresolved_ticket_form, order_resolved=order_resolved, order_unresolved=order_unresolved)


@admin_bp.route('/tickets/<int:ticket_id>/solve', methods=['POST'])
@login_required
@admin_required
def solve_ticket_page(ticket_id: int) -> Response:
    """
    route for handling POST request to set status of ticket of 'ticket_id' to solved
    """
    confirm_solution_form = ConfirmTicketSolutionForm()
    ticket_to_solve = Ticket.query.get_or_404(ticket_id)

    if confirm_solution_form.validate():
        solve_ticket(ticket_id, confirm_solution_form.solution_text.data)

    return redirect(url_for('admin_bp.ticket_administration_page'))


@admin_bp.route('/tickets/<int:ticket_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_ticket_page(ticket_id: int) -> Response:
    """
    route for handling POST request for deleting ticket of 'ticket_id'
    """
    ticket_deletion_form = ConfirmTicketDeletionForm()
    if ticket_deletion_form.validate_on_submit():
        ticket_to_delete = Ticket.query.get_or_404(ticket_id)

        db.session.delete(ticket_to_delete)
        db.session.commit()
        flash(f"ticket {ticket_to_delete} was succesfully deleted!", category="success")

    return redirect(url_for('admin_bp.ticket_administration_page'))


@admin_bp.route('/tickets/<int:ticket_id>/reopen', methods=['POST'])
@login_required
@admin_required
def reopen_ticket_page(ticket_id: int) -> Response:
    """
    route for handling POST request for reopening ticket of given 'ticket_id'
    """
    ticket_reopening_form = ConfirmTicketReopeningForm()
    if ticket_reopening_form.validate_on_submit():
        ticket_to_reopen = Ticket.query.get_or_404(ticket_id)
        reason_for_reopening = ticket_reopening_form.reason_for_reopening.data
        ticket_to_reopen.solver = None
        ticket_to_reopen.solved_on = None
        ticket_to_reopen.is_solved = False

        reopenning_message = TicketLogMessage(
            author_id=current_user.id, ticket_id=ticket_to_reopen.id, message_text=reason_for_reopening, message_category="reopened")

        db.session.add(reopenning_message)
        db.session.add(ticket_to_reopen)
        db.session.commit()

        interested_users = User.query.filter(
            User.current_watchlist.any(id=ticket_id)).all()

        for user in interested_users:
            send_ticket_reopened_email(user.email, ticket_to_reopen, current_user.username, current_user.id, reason_for_reopening)

        flash(f"ticket {ticket_to_reopen} was succesfully reopened!", category="success")

    return redirect(url_for('admin_bp.ticket_administration_page'))
