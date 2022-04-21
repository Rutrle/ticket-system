from flask import Blueprint, render_template, redirect, flash, url_for
from smart_ticket import db
from smart_ticket.models import User, admin_required
from flask_login import current_user, login_required
from smart_ticket.admin_bp.forms import ConfirmUserDeactivationForm

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')


@admin_bp.route('')
@login_required
@admin_required
def admin_page():
    active_users = db.session.query(User).filter(User.is_active == True).order_by('creation_time')
    inactive_users = db.session.query(User).filter(User.is_active == False).order_by('creation_time')
    user_deactivation_form = ConfirmUserDeactivationForm()

    return render_template("admin_bp/admin_tools.html", active_users=active_users, inactive_users=inactive_users, user_deactivation_form = user_deactivation_form)
   