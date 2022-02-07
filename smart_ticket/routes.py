from smart_ticket import app, db
from flask import render_template, request
from smart_ticket.forms import RegisterForm
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
    if request.method == 'POST':
        print(form.username)
        new_user = User(
            username = form.username.data,
            creation_time = datetime.now(),
            email=form.email.data,
            password = form.password1.data
        )
        db.session.add(new_user)
        db.session.commit()


    return render_template('registration.html', form=form)
