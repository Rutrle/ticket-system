from smart_ticket import app, db
from flask import redirect, render_template, request, flash, session, url_for
from flask_login import current_user, login_required


@app.route('/')
def index_():
    #testing view, to be deleted
    return render_template('base.html')

@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/about')
def about_page():
    return render_template('about.html')
