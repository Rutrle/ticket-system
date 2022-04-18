from flask import Blueprint, render_template, redirect, flash, url_for
from smart_ticket import db
from smart_ticket.models import User, admin_required
from flask_login import current_user, login_required


admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')


@admin_bp.route('')
@login_required
@admin_required
def admin_page():
    users = db.session.query(User).order_by('creation_time')

    return render_template("admin_bp/admin_tools.html", users=users)
   