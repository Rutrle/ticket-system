from smart_ticket import app, db
from flask import redirect, render_template, request, flash, session, url_for
from smart_ticket.forms import RegisterForm, LoginForm, OpenTicketForm, NewTicketLogMessage
from smart_ticket.models import User, Ticket, TicketLogMessage
from flask_login import current_user, login_user, logout_user, login_required

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

@app.route('/register', methods=['GET','POST'])
def registration_page():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        new_user = User(
            username = form.username.data,
            email=form.email.data,
            password = form.password1.data
        )
        db.session.add(new_user)
        db.session.commit()

    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'There was an error in User creation: {err_msg[0]}', category='danger')

    return render_template('registration.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_attempted_password(form.password.data):
                login_user(user)
                flash("You have succesfully logged in!", category='success')
                return redirect(url_for('home_page'))   ###### temporary, needs to change!
        else:
            flash('Wrong Username or password! Please try again.', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('You have logged out. Thanks for visiting!', category='info')
    return redirect(url_for('home_page'))


@app.route('/submit_ticket', methods=['GET','POST'])
def create_ticket_page():
    form = OpenTicketForm()
    if request.method == 'POST' and form.validate():
        
        new_ticket = Ticket(
            subject = form.subject.data,
            issue_description=form.issue_text.data,
        )

        if current_user.is_authenticated:
            new_ticket.author_id = current_user.id

        db.session.add(new_ticket)
        db.session.commit()
        creation_log_msg = TicketLogMessage(ticket_id = new_ticket.id, message_text = "Ticket opened")
        flash(f"ticket submitted succesfully", category="success")
        db.session.add(creation_log_msg)
        db.session.commit()        
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'There was an error in submiting a ticket: {err_msg[0]}', category='danger')

    return render_template('create_ticket.html', form=form)

@app.route('/ticket_list')
@login_required
def ticket_list_page():
    unresolved_tickets = Ticket.query.filter_by(is_solved = False).order_by(Ticket.creation_time)

    return render_template('ticket_list.html', tickets = unresolved_tickets)

@app.route('/ticket/<int:current_ticket_id>', methods=['GET','POST'])
@login_required
def ticket_detail_page(current_ticket_id:int):

    ticket = Ticket.query.get_or_404(current_ticket_id)
    msg_log = TicketLogMessage.query.filter_by(ticket_id = ticket.id) #.order_by(creation_time)

    form = NewTicketLogMessage()

    if request.method == 'POST':
        new_log_message = TicketLogMessage(
            author_id =  current_user.id,
            ticket_id = current_ticket_id,
            message_text = form.message_text.data
        )

        db.session.add(new_log_message)
        db.session.commit()


    return render_template('ticket_detail.html', ticket=ticket, msg_log=msg_log, form =form)


@app.template_filter('format_time')
def format_time(timestamp):
    return timestamp.strftime("%m/%d/%Y, %H:%M")