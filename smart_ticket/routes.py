from smart_ticket import app, db
from flask import render_template, request, flash
from smart_ticket.forms import RegisterForm, OpenTicketForm
from smart_ticket.models import User, Ticket
from datetime import datetime

@app.route('/')
def index():
    #testing view, to be deleted
    return render_template('base.html')

@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/register', methods=['GET','POST'])
def registration_page():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        new_user = User(
            username = form.username.data,
            creation_time = datetime.now(),
            email=form.email.data,
            password = form.password1.data
        )
        db.session.add(new_user)
        db.session.commit()

    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'There was an error in User creation: {err_msg[0]}', category='danger')

    return render_template('registration.html', form=form)

@app.route('/submit_ticket', methods=['GET','POST'])
def create_ticket_page():
    form = OpenTicketForm()
    if request.method == 'POST' and form.validate():
        new_ticket = Ticket(
            subject = form.subject.data,
            creation_time = datetime.now(),
            issue_description=form.issue_text.data,
            is_solved =  False
        )
        db.session.add(new_ticket)
        db.session.commit()
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'There was an error in User creation: {err_msg[0]}', category='danger')

    return render_template('create_ticket.html', form=form)