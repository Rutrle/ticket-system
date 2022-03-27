from flask_login import login_required
from smart_ticket import app
from flask import render_template
from smart_ticket.models import admin_required



@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/about')
def about_page():
    return render_template('about.html')

#temporary placement
from flask_login import current_user, login_required
@app.route('/admin')
@login_required
@admin_required
def admin_page():
    return "this is secret admin page"