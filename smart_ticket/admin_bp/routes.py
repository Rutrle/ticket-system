from flask import Blueprint, render_template, redirect, flash, url_for
from smart_ticket import db
from smart_ticket.models import User, Ticket, admin_required
from flask_login import current_user, login_required
from smart_ticket.admin_bp.forms import ConfirmUserDeactivationForm, ConfirmUserReactivationForm
from smart_ticket.ticket_bp.routes import solve_ticket
from smart_ticket.ticket_bp.forms import ConfirmTicketSolution

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')

def reactivate_user(user):
    user.is_active = True
    db.session.add(user)
    db.session.commit()


@admin_bp.route('', methods=['GET'])
@login_required
@admin_required
def admin_page():
    return render_template("admin_bp/administrator_tools.html")

@admin_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def user_administration():
    active_users = db.session.query(User).filter(User.is_active == True).order_by('creation_time')
    inactive_users = db.session.query(User).filter(User.is_active == False).order_by('creation_time')
    user_deactivation_form = ConfirmUserDeactivationForm()
    user_reactivation_form = ConfirmUserReactivationForm()

    return render_template("admin_bp/user_administration.html", active_users=active_users, inactive_users=inactive_users, user_deactivation_form = user_deactivation_form, user_reactivation_form=user_reactivation_form)

def deactivate_user(user):
    user.is_active = False
    user.currently_solving.clear()

    db.session.add(user)
    db.session.commit()   

@admin_bp.route('/users/<int:user_id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate_user_page(user_id:int):
    user_deactivation_form = ConfirmUserDeactivationForm()
    if user_deactivation_form.validate_on_submit():
        user_to_deactivate = User.query.filter_by(id=user_id).first()
        password_correct = current_user.check_attempted_password(user_deactivation_form.password.data)
        user_username_correct = user_to_deactivate.username == user_deactivation_form.user_username.data
        if password_correct and user_username_correct:
            deactivate_user(user_to_deactivate)
            flash(f"Account of user {user_to_deactivate.username} was succesfully deactivated!", category="success")

        else:
            flash(f'There was an error with deactivating a user {user_to_deactivate.username}, please check if you entered valid username and password', category='danger')

    elif user_deactivation_form.errors != {}:
        for err_msg in user_deactivation_form.errors.values():
            flash(f'There was an error with deactivating a user: {err_msg[0]}', category='danger')
    return redirect(url_for("admin_bp.user_administration"))

@admin_bp.route('/users/<int:user_id>/reactivate', methods=['POST'])
@login_required
@admin_required
def reactivate_user_page(user_id:int):
    user_reactivation_form = ConfirmUserReactivationForm()

    if user_reactivation_form.validate_on_submit():
        user_to_reactivate = User.query.filter_by(id=user_id).first()
        password_correct = current_user.check_attempted_password(user_reactivation_form.password.data)
        user_username_correct = user_to_reactivate.username == user_reactivation_form.user_username.data
        if password_correct and user_username_correct:
            reactivate_user(user_to_reactivate)
            flash(f"Account of user {user_to_reactivate.username} was succesfully reactivated!", category="success")    

    elif user_reactivation_form.errors != {}:
        for err_msg in user_reactivation_form.errors.values():
            flash(f'There was an error with reactivating a user: {err_msg[0]}', category='danger')  
    
    return redirect(url_for("admin_bp.user_administration"))


@admin_bp.route('/tickets', methods=['GET'])
@login_required
@admin_required
def ticket_administration():
    unresolved_tickets = db.session.query(Ticket).filter(Ticket.is_solved == False).outerjoin(Ticket.author).all()
    resolved_tickets = db.session.query(Ticket).filter(Ticket.is_solved == True).outerjoin(Ticket.author).all()

    confirm_solution_form = ConfirmTicketSolution()

    return render_template("admin_bp/ticket_administration.html", unresolved_tickets=unresolved_tickets, resolved_tickets=resolved_tickets, confirm_solution_form=confirm_solution_form)

@admin_bp.route('/tickets/<int:ticket_id>/solve', methods=['POST'])
@login_required
def solve_ticket_page(ticket_id):
    confirm_solution_form = ConfirmTicketSolution()

    if confirm_solution_form.validate():
        solve_ticket(ticket_id, confirm_solution_form.solution_text.data)

    return redirect(url_for('admin_bp.ticket_administration'))