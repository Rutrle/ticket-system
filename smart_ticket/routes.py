from smart_ticket import app, db
from flask import redirect, render_template, request, flash, session, url_for
from smart_ticket.forms import RegisterForm, LoginForm, OpenTicketForm, NewTicketLogMessage, AssignTicket2Self, UnassignTicket2Self
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

    if form.validate_on_submit():
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

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_attempted_password(form.password.data):
                login_user(user)
                flash("You have succesfully logged in!", category='success')
                return redirect(url_for('home_page'))   ###### temporary, needs to change!
        
        flash('Wrong Username or password! Please try again.', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('You have logged out. Thanks for visiting!', category='info')
    return redirect(url_for('home_page'))

@app.route('/user_detail/<int:id>')
@login_required
def user_detail_page(id:int):
    user = User.query.get_or_404(id)

    return render_template('user_detail.html', user=user)


@app.route('/submit_ticket', methods=['GET','POST'])
def create_ticket_page():
    form = OpenTicketForm()

    if form.validate_on_submit():
        new_ticket = Ticket(
            subject = form.subject.data,
            issue_description=form.issue_text.data,
        )

        if current_user.is_authenticated:
            new_ticket.author_id = current_user.id

        db.session.add(new_ticket)
        db.session.commit()
        creation_log_msg = TicketLogMessage(ticket_id = new_ticket.id, message_text = "Ticket opened")
        
        db.session.add(creation_log_msg)
        db.session.commit()
               
        flash(f"ticket submitted succesfully", category="success") 
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
    msg_log = TicketLogMessage.query.filter_by(ticket_id = ticket.id).order_by(TicketLogMessage.creation_time)
    currently_solving_users = User.query.filter(User.currently_solving.any(id =current_ticket_id)).all()


    new_log_msg_form = NewTicketLogMessage()
    assign_2_self_form = AssignTicket2Self()
    unassign_from_self_form =UnassignTicket2Self()

    if request.method == 'POST':
        if 'submit_new_log_ticket' in request.form and new_log_msg_form.validate():

                new_log_message = TicketLogMessage(
                    author_id =  current_user.id,
                    ticket_id = current_ticket_id,
                    message_text = new_log_msg_form.message_text.data
                )

                db.session.add(new_log_message)
                db.session.commit()

        elif 'assign_2_self' in request.form and assign_2_self_form.validate():
            if current_user in  ticket.current_solvers:
                flash(f'You are already assigned to ticket {ticket.subject}', category='warning')

            else:
                ticket.current_solvers.append(current_user)
                new_log_message = TicketLogMessage(
                    author_id =  current_user.id,
                    ticket_id = current_ticket_id,
                    message_text = f'User {current_user.username} started solving this issue'
                )

                db.session.add(new_log_message)
                db.session.add(ticket)
                db.session.commit()
                currently_solving_users = User.query.filter(User.currently_solving.any(id =current_ticket_id)).all()

                flash(f'You have been succesfully assigned to ticket {ticket.subject}', category='success')

        if assign_2_self_form.errors !={}:
            for err_msg in assign_2_self_form.errors.values():
                flash(f'There was an error: {err_msg[0]}', category='danger')

        elif 'unassign_from_self' in request.form and unassign_from_self_form.validate():
            if current_user not in  ticket.current_solvers:
                flash(f'You are not assigned to ticket {ticket.subject}', category='danger')
            else:
                ticket.current_solvers.remove(current_user) ################################################## maybe try/except - handling of user sending the request twice?
                new_log_message = TicketLogMessage(
                        author_id =  current_user.id,
                        ticket_id = current_ticket_id,
                        message_text = f'User {current_user.username} is no longer solving this issue'
                    )
                db.session.add(new_log_message)
                db.session.add(ticket)
                db.session.commit()
                currently_solving_users = User.query.filter(User.currently_solving.any(id =current_ticket_id)).all()
                flash(f'You are no longer assigned to ticket {ticket.subject}', category='warning')

    return render_template('ticket_detail.html', ticket=ticket, msg_log=msg_log, form =new_log_msg_form,assign_2_self_form=assign_2_self_form,unassign_from_self_form=unassign_from_self_form, currently_solving_users = currently_solving_users)


@app.template_filter('format_time')
def format_time(timestamp):
    return timestamp.strftime("%m/%d/%Y, %H:%M")